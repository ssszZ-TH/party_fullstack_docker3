DO $$
DECLARE
    r RECORD;          -- Record to store table information
    max_id BIGINT;     -- Variable to store MAX(id) of the table
    seq_name TEXT;     -- Name of the sequence associated with the id column
    curr_val BIGINT;   -- Variable to store current sequence value
BEGIN
    -- Loop through all tables in the 'public' schema that have an 'id' column using a sequence (SERIAL)
    FOR r IN 
        SELECT 
            t.table_name,
            c.column_default
        FROM information_schema.tables t
        JOIN information_schema.columns c 
            ON t.table_name = c.table_name 
            AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public'  -- Restrict to 'public' schema
          AND c.column_name = 'id'       -- Only columns named 'id'
          AND c.column_default LIKE 'nextval%'  -- Only columns using a sequence
          AND t.table_type = 'BASE TABLE'  -- Only base tables
    LOOP
        BEGIN
            -- Get the maximum id value from the table, default to 0 if the table is empty
            EXECUTE format('SELECT COALESCE(MAX(id), 0) FROM %I', r.table_name) INTO max_id;

            -- Extract the sequence name from the column_default (e.g., nextval('table_name_id_seq'::regclass))
            seq_name := substring(r.column_default FROM 'nextval\(''([^'']+)''');

            -- Reset the sequence based on the table's data
            IF max_id = 0 THEN
                -- If the table is empty, set the sequence to start at 1
                EXECUTE format('SELECT setval(%L, 1, false)', seq_name);
                RAISE NOTICE 'Table: %, No data, Sequence reset to start at: 1', r.table_name;
            ELSE
                -- If the table has data, set the sequence to MAX(id) + 1
                EXECUTE format('SELECT setval(%L, %s, false)', seq_name, max_id + 1);
                RAISE NOTICE 'Table: %, Max ID: %, Sequence reset to start at: %', 
                    r.table_name, max_id, max_id + 1;
            END IF;

            -- Verify the sequence reset by checking the current value
            BEGIN
                EXECUTE format('SELECT last_value FROM %s', seq_name) INTO curr_val;
                RAISE NOTICE 'Table: %, Sequence current value after reset: %', 
                    r.table_name, curr_val;
            EXCEPTION
                WHEN OTHERS THEN
                    RAISE NOTICE 'Table: %, Failed to verify sequence: %', r.table_name, SQLERRM;
            END;

        EXCEPTION
            WHEN OTHERS THEN
                -- Log error and continue with the next table
                RAISE NOTICE 'Error processing table %: %', r.table_name, SQLERRM;
                CONTINUE;
        END;
    END LOOP;

    -- Handle cases where no tables with sequences are found
    IF NOT FOUND THEN
        RAISE NOTICE 'No tables with SERIAL id columns found in schema public';
    END IF;
END $$;
DO $$
DECLARE
    r RECORD;          -- ตัวแปรสำหรับเก็บข้อมูลตาราง
    max_id BIGINT;     -- ตัวแปรสำหรับเก็บ MAX(id)
    seq_name TEXT;     -- ชื่อของ sequence
BEGIN
    -- Loop ผ่านทุกตารางที่มี column 'id' และใช้ sequence (SERIAL)
    FOR r IN 
        SELECT 
            t.table_name,
            c.column_default
        FROM information_schema.tables t
        JOIN information_schema.columns c 
            ON t.table_name = c.table_name 
            AND t.table_schema = c.table_schema
        WHERE t.table_schema = 'public'  -- เปลี่ยนเป็น schema ของคุณถ้าไม่ใช่ 'public'
          AND c.column_name = 'id'       -- เฉพาะ column ชื่อ 'id'
          AND c.column_default LIKE 'nextval%'  -- เฉพาะ column ที่ใช้ sequence
          AND t.table_type = 'BASE TABLE'
    LOOP
        -- หาค่า MAX(id) จากตาราง
        EXECUTE format('SELECT COALESCE(MAX(id), 0) FROM %I', r.table_name) INTO max_id;

        -- ดึงชื่อ sequence จาก column_default (เช่น nextval('table_name_id_seq'::regclass))
        seq_name := substring(r.column_default FROM 'nextval\(''([^'']+)''')::regclass;

        -- รีเซ็ต sequence เป็น MAX(id) + 1 หรือ 1 ถ้าว่าง
        IF max_id = 0 THEN
            EXECUTE format('SELECT setval(%L, 1)', seq_name);
            RAISE NOTICE 'Table: %, No data, Sequence reset to: 1', r.table_name;
        ELSE
            EXECUTE format('SELECT setval(%L, %s)', seq_name, max_id + 1);
            RAISE NOTICE 'Table: %, Max ID: %, Sequence reset to: %', 
                r.table_name, max_id, max_id + 1;
        END IF;
    END LOOP;
END $$;
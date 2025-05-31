# การอธิบายหลักการทำงานของสคริปต์ PL/pgSQL สำหรับรีเซ็ต Sequence

## วัตถุประสงค์
สคริปต์ PL/pgSQL นี้มีจุดประสงค์เพื่อรีเซ็ตค่า sequence ที่ใช้กับคอลัมน์ `id` (ที่มีประเภท `SERIAL`) ในทุกตารางภายใน schema `public` โดยตั้งค่าให้ sequence เริ่มต้นที่:
- `1` หากตารางไม่มีข้อมูล
- `MAX(id) + 1` หากตารางมีข้อมูล

สคริปต์นี้ได้รับการแก้ไขเพื่อแก้ปัญหาการที่ sequence ข้ามค่า (เช่น ได้ `id = 2` หรือ `id = 4` เมื่อทำการ `INSERT`) โดยใช้พารามิเตอร์ `is_called = false` ใน `setval` และเพิ่มการตรวจสอบเพื่อความถูกต้อง

## สคริปต์ PL/pgSQL
```sql
DO $$
DECLARE
    r RECORD;          -- Record to store table information
    max_id BIGINT;     -- Variable to store MAX(id) of the table
    seq_name TEXT;     -- Name of the sequence associated with the id column
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
        WHERE t.table_schema = 'public'  -- Restrict to 'public' schema (change if needed)
          AND c.column_name = 'id'       -- Only columns named 'id'
          AND c.column_default LIKE 'nextval%'  -- Only columns using a sequence
          AND t.table_type = 'BASE TABLE'  -- Only base tables
    LOOP
        -- Get the maximum id value from the table, default to 0 if the table is empty
        EXECUTE format('SELECT COALESCE(MAX(id), 0) FROM %I', r.table_name) INTO max_id;

        -- Extract the sequence name from the column_default (e.g., nextval('table_name_id_seq'::regclass))
        seq_name := substring(r.column_default FROM 'nextval\(''([^'']+)''')::regclass;

        -- Reset the sequence based on the table's data
        IF max_id = 0 THEN
            -- If the table is empty, set the sequence to start at 1
            -- Use is_called = false to ensure the next call to nextval returns 1
            EXECUTE format('SELECT setval(%L, 1, false)', seq_name);
            RAISE NOTICE 'Table: %, No data, Sequence reset to start at: 1', r.table_name;
        ELSE
            -- If the table has data, set the sequence to MAX(id)
            -- Use is_called = false to ensure the next call to nextval returns MAX(id) + 1
            EXECUTE format('SELECT setval(%L, %s, false)', seq_name, max_id);
            RAISE NOTICE 'Table: %, Max ID: %, Sequence reset to start at: %', 
                r.table_name, max_id, max_id + 1;
        END IF;

        -- Verify the sequence reset by checking the current value
        EXECUTE format('SELECT last_value FROM %I', seq_name) INTO max_id;
        RAISE NOTICE 'Table: %, Sequence current value after reset: %', r.table_name, max_id;
    END LOOP;

    -- Handle cases where no tables with sequences are found
    IF NOT FOUND THEN
        RAISE NOTICE 'No tables with SERIAL id columns found in schema public';
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        -- Catch and report any errors during execution
        RAISE NOTICE 'Error processing table %: %', r.table_name, SQLERRM;
END $$;
```

## การอธิบายทีละบรรทัด

### บรรทัด 1: `DO $$`
- **คำอธิบาย**: เริ่มต้นบล็อก PL/pgSQL แบบ anonymous (ไม่ต้องสร้างเป็นฟังก์ชัน) โดยใช้ `DO` เพื่อรันโค้ดทันที
- **หลักการ**: `$$` เป็น delimiter สำหรับบล็อก PL/pgSQL ช่วยให้โค้ดภายในสามารถมีเครื่องหมาย `;` หรือ `'` โดยไม่ทำให้เกิดข้อผิดพลาด
- **ตัวอย่างการทำงาน**: บอก PostgreSQL ว่านี่คือบล็อกโค้ดที่ต้องประมวลผลครั้งเดียว

### บรรทัด 2-5: การประกาศตัวแปร
```sql
DECLARE
    r RECORD;          -- Record to store table information
    max_id BIGINT;     -- Variable to store MAX(id) of the table
    seq_name TEXT;     -- Name of the sequence associated with the id column
```
- **คำอธิบาย**:
  - `r RECORD`: ตัวแปรประเภท `RECORD` ใช้เก็บข้อมูลจาก query ที่คืนผลลัพธ์ เช่น ชื่อตาราง (`table_name`) และค่า `column_default`
  - `max_id BIGINT`: ตัวแปรสำหรับเก็บค่า `MAX(id)` จากตาราง ใช้ `BIGINT` เพื่อรองรับค่า `id` ขนาดใหญ่ที่อาจเกิดจาก `SERIAL`
  - `seq_name TEXT`: ตัวแปรสำหรับเก็บชื่อ sequence ที่เชื่อมโยงกับคอลัมน์ `id` (เช่น `gender_type_id_seq`)
- **หลักการ**: การประกาศตัวแปรเป็นขั้นตอนแรกเพื่อให้สามารถเก็บข้อมูลชั่วคราวระหว่างการประมวลผล
- **ตัวอย่างการทำงาน**: ถ้ามีตาราง `gender_type` ตัวแปร `r` อาจเก็บ `{table_name: 'gender_type', column_default: 'nextval(''gender_type_id_seq''::regclass)'}`

### บรรทัด 6: `BEGIN`
- **คำอธิบาย**: เริ่มต้นส่วนของโค้ดที่เป็น logic การทำงานของ PL/pgSQL
- **หลักการ**: แยกส่วนการประกาศตัวแปร (`DECLARE`) ออกจากส่วนการประมวลผล
- **ตัวอย่างการทำงาน**: บอกว่าโค้ดต่อไปนี้เป็นส่วนที่รันจริง

### บรรทัด 7-17: ลูปผ่านตารางที่มี `SERIAL`
```sql
FOR r IN 
    SELECT 
        t.table_name,
        c.column_default
    FROM information_schema.tables t
    JOIN information_schema.columns c 
        ON t.table_name = c.table_name 
        AND t.table_schema = c.table_schema
    WHERE t.table_schema = 'public'  -- Restrict to 'public' schema (change if needed)
      AND c.column_name = 'id'       -- Only columns named 'id'
      AND c.column_default LIKE 'nextval%'  -- Only columns using a sequence
      AND t.table_type = 'BASE TABLE'  -- Only base tables
LOOP
```
- **คำอธิบาย**:
  - `FOR r IN ... LOOP`: สร้างลูปเพื่อวนผ่านผลลัพธ์ของ query โดยเก็บแต่ละแถวในตัวแปร `r`
  - Query ค้นหาตารางที่มีคอลัมน์ `id` ที่ใช้ `SERIAL` โดย:
    - `information_schema.tables`: ดึงข้อมูลตารางใน database
    - `information_schema.columns`: ดึงข้อมูลคอลัมน์ของตาราง
    - `JOIN ... ON`: เชื่อมตารางและคอลัมน์โดยใช้ `table_name` และ `table_schema`
    - `WHERE`:
      - `t.table_schema = 'public'`: จำกัดเฉพาะ schema `public` (สามารถเปลี่ยนได้ถ้าใช้ schema อื่น)
      - `c.column_name = 'id'`: เฉพาะคอลัมน์ชื่อ `id`
      - `c.column_default LIKE 'nextval%'`: เฉพาะคอลัมน์ที่ใช้ sequence (เช่น `nextval('table_name_id_seq'::regclass)`)
      - `t.table_type = 'BASE TABLE'`: เฉพาะตารางจริง (ไม่รวม view หรือ temporary table)
- **หลักการ**: ใช้ `information_schema` เพื่อดึง metadata ของ database ทำให้สคริปต์สามารถค้นหาตารางที่มี `SERIAL` ได้อัตโนมัติ
- **ตัวอย่างการทำงาน**: หากมีตาราง `gender_type` และ `person` ที่มี `id SERIAL` ลูปนี้จะคืน:
  - `{table_name: 'gender_type', column_default: 'nextval(''gender_type_id_seq''::regclass)'`
  - `{table_name: 'person', column_default: 'nextval(''person_id_seq''::regclass)'`

### บรรทัด 19-20: หาค่า `MAX(id)`
```sql
EXECUTE format('SELECT COALESCE(MAX(id), 0) FROM %I', r.table_name) INTO max_id;
```
- **คำอธิบาย**:
  - `EXECUTE`: รัน query แบบ dynamic โดยใช้ `format` เพื่อสร้างคำสั่ง SQL
  - `format('SELECT COALESCE(MAX(id), 0) FROM %I', r.table_name)`: สร้าง query เช่น `SELECT COALESCE(MAX(id), 0) FROM gender_type`
  - `COALESCE(MAX(id), 0)`: หาค่า `id` สูงสุดในตาราง ถ้าตารางว่าง (`MAX(id)` เป็น `NULL`) จะคืนค่า 0
  - `INTO max_id`: เก็บผลลัพธ์ในตัวแปร `max_id`
- **หลักการ**: หาค่า `id` สูงสุดเพื่อใช้ตั้งค่า sequence ให้สอดคล้องกับข้อมูลที่มีอยู่
- **ตัวอย่างการทำงาน**:
  - ถ้า `gender_type` ว่าง: `max_id = 0`
  - ถ้า `gender_type` มี `id = 1, 2`: `max_id = 2`

### บรรทัด 22-23: ดึงชื่อ sequence
```sql
seq_name := substring(r.column_default FROM 'nextval\(''([^'']+)''')::regclass;
```
- **คำอธิบาย**:
  - `substring(... FROM 'nextval\(''([^'']+)''')`: ใช้ regular expression เพื่อแยกชื่อ sequence จาก `column_default` เช่น จาก `nextval('gender_type_id_seq'::regclass)` ได้ `gender_type_id_seq`
  - `::regclass`: แปลงชื่อ sequence เป็น object identifier เพื่อให้ PostgreSQL ตรวจสอบว่า sequence มีอยู่จริง
  - เก็บผลลัพธ์ใน `seq_name`
- **หลักการ**: ดึงชื่อ sequence ที่เชื่อมโยงกับคอลัมน์ `id` เพื่อใช้ในการตั้งค่า
- **ตัวอย่างการทำงาน**: สำหรับ `column_default = 'nextval(''gender_type_id_seq''::regclass)'` ได้ `seq_name = 'gender_type_id_seq'`

### บรรทัด 25-36: รีเซ็ต sequence
```sql
IF max_id = 0 THEN
    -- If the table is empty, set the sequence to start at 1
    -- Use is_called = false to ensure the next call to nextval returns 1
    EXECUTE format('SELECT setval(%L, 1, false)', seq_name);
    RAISE NOTICE 'Table: %, No data, Sequence reset to start at: 1', r.table_name;
ELSE
    -- If the table has data, set the sequence to MAX(id)
    -- Use is_called = false to ensure the next call to nextval returns MAX(id) + 1
    EXECUTE format('SELECT setval(%L, %s, false)', seq_name, max_id);
    RAISE NOTICE 'Table: %, Max ID: %, Sequence reset to start at: %', 
        r.table_name, max_id, max_id + 1;
END IF;
```
- **คำอธิบาย**:
  - `IF max_id = 0 THEN`: ตรวจสอบว่าตารางว่างหรือไม่ (ไม่มี `id` หรือ `MAX(id) = 0`)
    - `EXECUTE format('SELECT setval(%L, 1, false)', seq_name)`: ตั้ง sequence ให้เริ่มที่ 1 โดย:
      - `%L`: ใช้สำหรับ string literal (ชื่อ sequence)
      - `setval(seq_name, 1, false)`: ตั้งค่า sequence เป็น 1 และ `is_called = false` เพื่อให้ `nextval` ครั้งถัดไปคืนค่า 1
    - `RAISE NOTICE`: แจ้งว่า sequence ถูกรีเซ็ตเป็น 1 สำหรับตารางที่ว่าง
  - `ELSE`: ถ้าตารางมีข้อมูล (`max_id > 0`)
    - `EXECUTE format('SELECT setval(%L, %s, false)', seq_name, max_id)`: ตั้ง sequence เป็น `MAX(id)` โดย:
      - `%s`: ใช้สำหรับตัวเลข (`max_id`)
      - `setval(seq_name, max_id, false)`: ตั้งค่า sequence เป็น `MAX(id)` และ `is_called = false` เพื่อให้ `nextval` ครั้งถัดไปคืนค่า `MAX(id) + 1`
    - `RAISE NOTICE`: แจ้งค่า `MAX(id)` และค่าเริ่มต้นใหม่ของ sequence (`MAX(id) + 1`)
- **หลักการ**:
  - `is_called = false` เป็นกุญแจสำคัญ แก้ปัญหาการข้ามค่า (เช่น ได้ `id = 2` แทน `id = 1`) โดยทำให้ `nextval` เริ่มที่ค่า `value` ที่ตั้งไว้
  - แยกกรณีตารางว่างและมีข้อมูลเพื่อตั้งค่า sequence อย่างเหมาะสม
- **ตัวอย่างการทำงาน**:
  - ถ้า `gender_type` ว่าง: ตั้ง `gender_type_id_seq` เป็น 1, `INSERT` ถัดไปได้ `id = 1`
  - ถ้า `gender_type` มี `MAX(id) = 2`: ตั้ง `gender_type_id_seq` เป็น 2, `INSERT` ถัดไปได้ `id = 3`

### บรรทัด 38-39: ตรวจสอบการรีเซ็ต
```sql
EXECUTE format('SELECT last_value FROM %I', seq_name) INTO max_id;
RAISE NOTICE 'Table: %, Sequence current value after reset: %', r.table_name, max_id;
```
- **คำอธิบาย**:
  - `EXECUTE format('SELECT last_value FROM %I', seq_name)`: ดึงค่า `last_value` ปัจจุบันของ sequence เพื่อยืนยันการตั้งค่า
  - `INTO max_id`: เก็บค่า `last_value` ใน `max_id`
  - `RAISE NOTICE`: แจ้งค่า `last_value` เพื่อให้ผู้ใช้เห็นว่า sequence ถูกรีเซ็ตถูกต้อง
- **หลักการ**: การตรวจสอบช่วย debug และยืนยันว่า sequence พร้อมสำหรับการ `INSERT` ถัดไป
- **ตัวอย่างการทำงาน**: ถ้าตั้ง `gender_type_id_seq` เป็น 1 จะได้:
  - `NOTICE: Table: gender_type, Sequence current value after reset: 1`

### บรรทัด 40: `END LOOP;`
- **คำอธิบาย**: ปิดลูป `FOR` หลังจากประมวลผลทุกตารางที่มี `SERIAL`
- **หลักการ**: วนลูปจนครบทุกตารางที่ตรงเงื่อนไข
- **ตัวอย่างการทำงาน**: ถ้ามี 2 ตาราง (`gender_type`, `person`) ลูปจะรัน 2 รอบ

### บรรทัด 42-44: ตรวจสอบกรณีไม่มีตาราง
```sql
IF NOT FOUND THEN
    RAISE NOTICE 'No tables with SERIAL id columns found in schema public';
END IF;
```
- **คำอธิบาย**:
  - `IF NOT FOUND`: ตรวจสอบว่าลูป `FOR` ไม่พบตารางใดที่ตรงเงื่อนไข (เช่น ไม่มีตารางที่มี `id SERIAL`)
  - `RAISE NOTICE`: แจ้งเตือนว่าไม่มีตารางที่ใช้ `SERIAL` ใน schema `public`
- **หลักการ**: ป้องกันสคริปต์เงียบเมื่อไม่มีตารางที่ต้องประมวลผล
- **ตัวอย่างการทำงาน**: ถ้า schema `public` ไม่มีตารางที่มี `id SERIAL` จะได้:
  - `NOTICE: No tables with SERIAL id columns found in schema public`

### บรรทัด 46-48: การจัดการข้อผิดพลาด
```sql
EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE 'Error processing table %: %', r.table_name, SQLERRM;
```
- **คำอธิบาย**:
  - `EXCEPTION`: จับข้อผิดพลาดที่อาจเกิดขึ้นระหว่างรันสคริปต์
  - `WHEN OTHERS`: จับข้อผิดพลาดทุกประเภท
  - `RAISE NOTICE`: แจ้งชื่อตารางและข้อความข้อผิดพลาด (`SQLERRM`) เพื่อช่วย debug
- **หลักการ**: ทำให้สคริปต์แข็งแกร่งโดยไม่ล้มเหลวทั้งหมดหากตารางหรือ sequence มีปัญหา
- **ตัวอย่างการทำงาน**: ถ้า sequence `gender_type_id_seq` ถูกลบ จะได้:
  - `NOTICE: Error processing table gender_type: relation "gender_type_id_seq" does not exist`

### บรรทัด 49: `END $$;`
- **คำอธิบาย**: ปิดบล็อก PL/pgSQL
- **หลักการ**: สิ้นสุดการประมวลผลและคืนผลลัพธ์
- **ตัวอย่างการทำงาน**: PostgreSQL เสร็จสิ้นการรันสคริปต์

## การแก้ไขปัญหาเดิม
สคริปต์เดิมมีปัญหาที่ `INSERT` ลงตาราง `gender_type` ได้ `id = 2` และ `id = 4` แทน `id = 1` หรือ `id = 2` สาเหตุคือ:
- การใช้ `setval` โดยไม่ระบุ `is_called` ทำให้ default เป็น `is_called = true` ส่งผลให้ `nextval` ข้ามค่าแรก (เช่น ตั้งที่ 1 แต่ได้ 2)
- สคริปต์ใหม่แก้โดยใช้ `setval(..., false)` เพื่อให้ `nextval` เริ่มที่ค่า `value` (เช่น 1 หรือ `MAX(id)`)
- เพิ่มการตรวจสอบ `last_value` เพื่อยืนยันการตั้งค่า

## ตัวอย่างผลลัพธ์
สมมติตาราง `gender_type` ว่าง:
- รันสคริปต์:
  ```
  NOTICE: Table: gender_type, No data, Sequence reset to start at: 1
  NOTICE: Table: gender_type, Sequence current value after reset: 1
  ```
- `INSERT INTO gender_type (description) VALUES ('Male');` → ได้ `id = 1`
- เพิ่มข้อมูลและรันซ้ำ:
  - `MAX(id) = 1`
  - รันสคริปต์:
    ```
    NOTICE: Table: gender_type, Max ID: 1, Sequence reset to start at: 2
    NOTICE: Table: gender_type, Sequence current value after reset: 1
    ```
  - `INSERT INTO gender_type (description) VALUES ('Female');` → ได้ `id = 2`

## ข้อควรระวัง
- **Schema**: ถ้าตารางอยู่ใน schema อื่น ต้องเปลี่ยน `t.table_schema = 'public'` เป็น schema ที่ต้องการ
- **Transaction**: ตรวจสอบว่าไม่มี transaction อื่นเรียก `nextval` ขณะรันสคริปต์
- **การล็อก**: ถ้าตารางถูกล็อก อาจต้องรอ transaction อื่นจบก่อน
- **การตรวจสอบ**: ใช้ `SELECT * FROM table_name_id_seq;` เพื่อดูสถานะ sequence

## สรุป
สคริปต์นี้รีเซ็ต sequence ของคอลัมน์ `id` ในตารางที่มี `SERIAL` โดยใช้ `information_schema` ค้นหาตาราง, หา `MAX(id)`, และตั้งค่า sequence ด้วย `setval` พร้อม `is_called = false` เพื่อป้องกันการข้ามค่า การตรวจสอบและจัดการข้อผิดพลาดทำให้สคริปต์แข็งแกร่งและเหมาะสำหรับการจัดการ database
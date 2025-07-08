# รายการเอกสารประกอบซอฟต์แวร์

1. **คำนำ (Introduction)**  
   - ภาพรวมซอฟต์แวร์ PartySync  
   - วัตถุประสงค์และขอบเขตการใช้งาน  
   - คุณสมบัติหลักและประโยชน์ 

2. **สถาปัตยกรรมและเทคโนโลยี**  
   - เทคโนโลยีที่ใช้: React, Material-UI, SQL, Docker  
   - สถาปัตยกรรม: FullStack, CloudNative  
   - การจัดการความปลอดภัย: JWT Authentication  

3. **ER Diagram**  
   - แผนภาพ Entity-Relationship แบบ Crowfoot  
   - อธิบายความสัมพันธ์ระหว่างตาราง เช่น party, person, organization  

4. **Table Schema Description**  
   - รายละเอียดตาราง: ชื่อตาราง, ชื่อคอลัมน์, ชนิดข้อมูล (เช่น INT, VARCHAR(128)), คำอธิบาย, Primary Key, Foreign Key  
   - ตัวอย่าง: ตาราง `person`  
     - `id`: INT, รหัสบุคคล, Primary Key  
     - `personal_id_number`: VARCHAR(128), รหัสประจำตัวประชาชน, Candidate Key  

5. **Flowchart**  
   - แผนภาพขั้นตอนการทำงานของระบบ  
   - ลำดับการทำงานของ CRUD และการยืนยันตัวตนด้วย JWT  

6. **User Flow Diagram**  
   - แผนภาพการใช้งานของผู้ใช้ (User Journey)  
   - แสดงการกระทำและลำดับหน้าที่ผู้ใช้พบ เช่น Party List → Party Create/Edit  

7. **รายการหน้า Frontend**  
   - รายการหน้าจอ: Party List, Person Info Create/Edit, Relationship List, Communication Create/Edit  

8. **การติดตั้งและใช้งาน**  
   - ขั้นตอนติดตั้ง:  
     - ติดตั้ง Git, Docker Desktop  
     - รัน `git clone` และ `docker compose up -d --build`  

9. **ข้อจำกัดและแนวทางพัฒนา**  
   - ข้อจำกัดของระบบปัจจุบัน  
   - แผนพัฒนาต่อในอนาคต 

# ครูสั่ง

   - er diagram
   - schema
   - use case
   - state diagram
   - sequence diagram
   - activity diagram
// ไฟล์นี้เป็น Modal สำหรับจัดการข้อมูลบุคคล (Person) ในระบบ
// ใช้สำหรับสร้าง (create), อัพเดท (update), หรือดูข้อมูล (read) โดยแสดงฟอร์มที่มีฟิลด์ต่าง ๆ
import React, { useState, useEffect } from "react";
import { Modal, Box, TextField, Typography, Stack } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateField } from "@mui/x-date-pickers/DateField";
import dayjs from "dayjs";
import SaveButton from "../buttons/SaveButton";

// อินเทอร์เฟซกำหนดโครงสร้างข้อมูลสำหรับฟอร์ม
// สอดคล้องกับ payload ที่ส่งไปยัง API endpoint `/v1/person`
interface FormData {
  id: number | null; // รหัสบุคคล (null สำหรับการสร้างใหม่)
  socialsecuritynumber: string; // หมายเลขประกันสังคม
  birthdate: string; // วันเกิด (รูปแบบ yyyy-mm-dd)
  mothermaidenname: string; // นามสกุลเดิมของมารดา
  totalyearworkexperience: number; // จำนวนปีประสบการณ์ทำงาน
  comment: string; // ความคิดเห็นเพิ่มเติม
}

// สไตล์สำหรับ Modal เพื่อให้แสดงตรงกลางหน้าจอ
// ใช้ Box จาก MUI เพื่อกำหนดขนาดและลักษณะ
const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400, // ความกว้างคงที่
  bgcolor: "background.paper", // พื้นหลังสีขาว
  boxShadow: 24, // เงาเพื่อความสวยงาม
  p: 4, // padding ภายใน
};

// อินเทอร์เฟซสำหรับ props ที่ component นี้รับ
interface ModalProps {
  open: boolean; // ควบคุมการเปิด/ปิด Modal
  onClose: () => void; // ฟังก์ชันเมื่อปิด Modal
  initialDetail: FormData; // ข้อมูลเริ่มต้นสำหรับฟอร์ม (จาก API หรือค่าเริ่มต้น)
  onSubmit: (updatedPerson: FormData) => void; // ฟังก์ชันเมื่อ submit ฟอร์ม (ส่งข้อมูลไปยัง parent)
  openModalFor: string; // โหมดของ Modal ("create", "update", "read")
}

// Component หลักสำหรับแสดง Modal
export default function PersonModal({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
}: ModalProps) {
  // State สำหรับเก็บข้อมูลฟอร์ม
  // ค่าเริ่มต้นเป็น object ว่างเพื่อป้องกัน undefined
  const [formData, setFormData] = useState<FormData>({
    id: null,
    socialsecuritynumber: "",
    birthdate: "",
    mothermaidenname: "",
    totalyearworkexperience: 0,
    comment: "",
  });

  // useEffect สำหรับอัพเดท formData เมื่อ initialDetail เปลี่ยน
  // ใช้เมื่อ Modal ถูกเปิดในโหมด update/read หรือเมื่อ parent ส่งข้อมูลใหม่
  useEffect(() => {
    console.log("PersonModal: form initial detail = ", initialDetail); // Log เพื่อ debug ข้อมูลเริ่มต้น
    setFormData(initialDetail); // อัพเดท state ด้วยข้อมูลจาก props
  }, [initialDetail]);

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ TextField
  // รองรับ input ทุกประเภทยกเว้น DateField
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === "totalyearworkexperience" ? Number(value) : value, // แปลงค่าเป็น number สำหรับ totalyearworkexperience
    });
  };

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ DateField (birthdate)
  // แปลงวันที่จาก dayjs เป็น string รูปแบบ yyyy-mm-dd
  const handleDateChange = (name: string, value: dayjs.Dayjs | null) => {
    const dateValue = value ? value.format("YYYY-MM-DD") : ""; // ถ้าไม่มีค่าให้เป็น string ว่าง
    setFormData({ ...formData, [name]: dateValue });
  };

  // ฟังก์ชันเมื่อกดปุ่ม Save
  // ทำการ validate และส่งข้อมูลไปยัง parent
  const handleSubmit = () => {
    if (!formData.birthdate) {
      alert("Birth Date is required"); // ตรวจสอบว่า birthdate ไม่ว่าง
      return;
    }
    onSubmit(formData); // ส่งข้อมูลฟอร์มไปยัง parent (PersonPage.tsx)
    // onClose ไม่เรียกที่นี่ เพราะ parent จะจัดการปิด Modal หลัง API call สำเร็จ
  };

  // useEffect สำหรับ log ค่า openModalFor
  // ช่วย debug ว่า Modal ถูกเปิดในโหมดใด
  useEffect(() => {
    console.log("PersonModal: openModalFor = ", openModalFor);
  }, [openModalFor]);

  // JSX สำหรับ UI ของ Modal
  return (
    // LocalizationProvider ใช้สำหรับ DateField เพื่อจัดการวันที่ด้วย dayjs
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Modal open={open} onClose={onClose}>
        <Box sx={style}>
          {/* หัวข้อของ Modal */}
          <Typography variant="h6" component="h2">
            Person Details
          </Typography>
          {/* ฟิลด์สำหรับหมายเลขประกันสังคม */}
          <TextField
            label="Social Security Number"
            name="socialsecuritynumber"
            value={formData.socialsecuritynumber}
            onChange={handleChange}
            fullWidth // ขยายให้เต็มความกว้าง
            margin="normal" // ระยะห่างตาม MUI standard
            disabled={openModalFor === "read"} // ปิดการแก้ไขในโหมด read
          />
          {/* ฟิลด์สำหรับวันเกิด ใช้ DateField เพื่อ UI ที่ดีและควบคุมรูปแบบวันที่ */}
          <DateField
            label="Birth Date"
            name="birthdate"
            value={formData.birthdate ? dayjs(formData.birthdate) : null} // แปลง string เป็น dayjs object
            onChange={(newValue) => handleDateChange("birthdate", newValue)} // ใช้ handleDateChange
            format="YYYY-MM-DD" // บังคับ UI แสดง yyyy-mm-dd
            fullWidth
            margin="normal"
            sx={{ mb: 2 }} // เพิ่ม margin ด้านล่างเพื่อความสวยงาม
            disabled={openModalFor === "read"}
            required // บ่งชี้ว่าฟิลด์นี้จำเป็น
          />
          {/* ฟิลด์สำหรับนามสกุลเดิมของมารดา */}
          <TextField
            label="Mother's Maiden Name"
            name="mothermaidenname"
            value={formData.mothermaidenname}
            onChange={handleChange}
            fullWidth
            margin="normal"
            disabled={openModalFor === "read"}
          />
          {/* ฟิลด์สำหรับจำนวนปีประสบการณ์ทำงาน */}
          <TextField
            label="Total Years Work Experience"
            name="totalyearworkexperience"
            type="number" // จำกัดให้กรอกตัวเลขเท่านั้น
            value={formData.totalyearworkexperience}
            onChange={handleChange}
            fullWidth
            margin="normal"
            disabled={openModalFor === "read"}
          />
          {/* ฟิลด์สำหรับความคิดเห็น ใช้ multiline เพื่อให้กรอกได้หลายบรรทัด */}
          <TextField
            label="Comment"
            name="comment"
            value={formData.comment}
            onChange={handleChange}
            fullWidth
            margin="normal"
            multiline
            rows={3} // แสดง 3 บรรทัด
            disabled={openModalFor === "read"}
          />
          {/* แสดงปุ่ม Save เฉพาะในโหมด create และ update */}
          {openModalFor !== "read" && (
            <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
              <SaveButton onClick={handleSubmit} /> {/* ปุ่ม Save จาก component แยก */}
            </Stack>
          )}
        </Box>
      </Modal>
    </LocalizationProvider>
  );
}
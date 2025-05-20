// ไฟล์นี้เป็น Modal สำหรับจัดการข้อมูลลักษณะทางกายภาพ (Physical Characteristic)
// ใช้สำหรับสร้าง (create), อัพเดท (update), หรือดูข้อมูล (read) โดยแสดงฟอร์มที่มีวันที่, ค่า, และ dropdown
import React, { useState, useEffect } from "react";
import {
  Modal,
  Box,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Stack,
  TextField,
} from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateField } from "@mui/x-date-pickers/DateField";
import dayjs from "dayjs";
import SaveButton from "./buttons/SaveButton";

// อินเทอร์เฟซกำหนดโครงสร้างข้อมูลสำหรับฟอร์ม
// สอดคล้องกับ payload ที่ส่งไปยัง API endpoint `/v1/physicalcharacteristic`
interface typeOfFormData {
  id: number | null; // รหัสลักษณะทางกายภาพ (null สำหรับการสร้างใหม่)
  fromdate: string; // วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)
  thrudate: string; // วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD, ว่างได้)
  val: number; // ค่าลักษณะทางกายภาพ (เช่น ความสูง, น้ำหนัก)
  person_id: number | ""; // รหัสบุคคล (foreign key อ้างถึงตาราง person)
  physicalcharacteristictype_id: number | ""; // รหัสประเภทลักษณะ (foreign key อ้างถึงตาราง physicalcharacteristictype)
}

// สไตล์สำหรับ Modal เพื่อให้แสดงตรงกลางหน้าจอ
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

// อินเทอร์เฟซสำหรับข้อมูลใน dropdown
interface typeOfDD {
  id: number; // รหัสของตัวเลือก
  text: string; // ข้อความที่แสดงใน dropdown
}

// อินเทอร์เฟซสำหรับ props ที่ component นี้รับ
interface typeofModalProps {
  open: boolean; // ควบคุมการเปิด/ปิด Modal
  onClose: () => void; // ฟังก์ชันเมื่อปิด Modal
  initialDetail: typeOfFormData; // ข้อมูลเริ่มต้นสำหรับฟอร์ม
  onSubmit: (updatedData: typeOfFormData) => void; // ฟังก์ชันเมื่อ submit ฟอร์ม
  openModalFor: string; // โหมดของ Modal ("create", "update", "read")
  personDD: Array<typeOfDD>; // Dropdown สำหรับ Person
  physicalcharacteristictypeDD: Array<typeOfDD>; // Dropdown สำหรับ PhysicalCharacteristicType
}

// Component หลักสำหรับแสดง Modal
export default function Modal_physicalcharacteristic({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
  personDD,
  physicalcharacteristictypeDD,
}: typeofModalProps) {
  // State สำหรับเก็บข้อมูลฟอร์ม
  const [formData, setFormData] = useState<typeOfFormData>({
    id: null,
    fromdate: "",
    thrudate: "",
    val: 0,
    person_id: "", // ใช้ "" เพื่อป้องกัน MUI Select warning
    physicalcharacteristictype_id: "",
  });

  // useEffect สำหรับอัพเดท formData เมื่อ initialDetail เปลี่ยน
  useEffect(() => {
    console.log("form initial detail = ", initialDetail);
    setFormData({
      ...initialDetail,
      person_id: initialDetail.person_id === 0 ? "" : initialDetail.person_id, // แปลง 0 เป็น "" เพื่อป้องกัน warning
      physicalcharacteristictype_id:
        initialDetail.physicalcharacteristictype_id === 0
          ? ""
          : initialDetail.physicalcharacteristictype_id,
    });
  }, [initialDetail]);

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ DateField
  const handleDateChange = (name: string, value: dayjs.Dayjs | null) => {
    const dateValue = value ? value.format("YYYY-MM-DD") : ""; // แปลงเป็น YYYY-MM-DD หรือ ""
    setFormData({ ...formData, [name]: dateValue });
  };

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ TextField และ Select
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]:
        name === "val" || name === "person_id" || name === "physicalcharacteristictype_id"
          ? Number(value) || "" // แปลงเป็น number หรือ "" ถ้าเป็น dropdown หรือ val
          : value,
    });
  };

  // ฟังก์ชันจัดการการ submit ฟอร์ม
  const handleSubmit = () => {
    // Validation เพื่อป้องกันข้อมูลไม่สมบูรณ์
    if (!formData.fromdate) {
      alert("From Date is required");
      return;
    }
    if (!formData.person_id) {
      alert("Person is required");
      return;
    }
    if (!formData.physicalcharacteristictype_id) {
      alert("Physical Characteristic Type is required");
      return;
    }
    if (formData.val <= 0) {
      alert("Value must be greater than 0");
      return;
    }
    onSubmit(formData); // ส่งข้อมูลไปยัง parent
    onClose(); // ปิด Modal
  };

  // useEffect สำหรับ log โหมดของ Modal เพื่อ debug
  useEffect(() => {
    console.log("openModalFor = ", openModalFor);
  }, [openModalFor]);

  // JSX สำหรับ UI ของ Modal
  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Physical Characteristic Details
        </Typography>

        <LocalizationProvider dateAdapter={AdapterDayjs}>
          {/* ฟิลด์วันที่เริ่มต้น */}
          <DateField
            label="From Date"
            value={formData.fromdate ? dayjs(formData.fromdate) : null}
            onChange={(newValue) => handleDateChange("fromdate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
            disabled={openModalFor === "read"}
            required
          />
          {/* ฟิลด์วันที่สิ้นสุด */}
          <DateField
            label="Thru Date"
            value={formData.thrudate ? dayjs(formData.thrudate) : null}
            onChange={(newValue) => handleDateChange("thrudate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
            disabled={openModalFor === "read"}
          />
        </LocalizationProvider>

        {/* ฟิลด์สำหรับค่า (val) */}
        <TextField
          label="Value"
          name="val"
          type="number"
          value={formData.val || ""}
          onChange={handleChange}
          fullWidth
          margin="normal"
          disabled={openModalFor === "read"}
          required
        />

        {/* Dropdown สำหรับเลือกบุคคล */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="person-select-label">Person</InputLabel>
          <Select
            labelId="person-select-label"
            name="person_id"
            value={formData.person_id || ""}
            onChange={handleChange}
            disabled={openModalFor === "read"}
            required
          >
            <MenuItem value="">
              <em>Select Person</em>
            </MenuItem>
            {personDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Dropdown สำหรับเลือกประเภทลักษณะ */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="physical-characteristic-type">Physical Characteristic Type</InputLabel>
          <Select
            labelId="physical-characteristic-type"
            name="physicalcharacteristictype_id"
            value={formData.physicalcharacteristictype_id || ""}
            onChange={handleChange}
            disabled={openModalFor === "read"}
            required
          >
            <MenuItem value="">
              <em>Select Physical Characteristic Type</em>
            </MenuItem>
            {physicalcharacteristictypeDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* ปุ่ม Save สำหรับโหมด create และ update */}
        {openModalFor !== "read" && (
          <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
            <SaveButton onClick={handleSubmit} />
          </Stack>
        )}
      </Box>
    </Modal>
  );
}
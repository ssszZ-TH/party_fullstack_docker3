// ไฟล์นี้เป็น Modal สำหรับจัดการข้อมูลการจำแนกตามประเภทอุตสาหกรรม
// ใช้สำหรับสร้าง (create), อัพเดท (update), หรือดูข้อมูล (read) โดยแสดงฟอร์มที่มีวันที่และ dropdown
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
} from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateField } from "@mui/x-date-pickers/DateField";
import dayjs from "dayjs";
import SaveButton from "../buttons/SaveButton";

// อินเทอร์เฟซกำหนดโครงสร้างข้อมูลสำหรับฟอร์ม
// สอดคล้องกับ payload ที่ส่งไปยัง API endpoint `/v1/classifybyindustry`
interface typeOfFormData {
  id: number | null; // รหัสการจำแนก (null สำหรับการสร้างใหม่)
  fromdate: string; // วันที่เริ่มต้น (รูปแบบ YYYY-MM-DD)
  thrudate: string; // วันที่สิ้นสุด (รูปแบบ YYYY-MM-DD, ว่างได้)
  party_id: number | ""; // รหัส Party (จาก InformalOrganization.id หรือ LegalOrganization.id)
  party_type_id: number | ""; // รหัสประเภท Party (foreign key อ้างถึงตาราง partytype)
  industry_type_id: number | ""; // รหัสประเภทอุตสาหกรรม (foreign key อ้างถึงตาราง industrytype)
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
  type: "informal" | "legal"; // ระบุประเภทองค์กร
}

// อินเทอร์เฟซสำหรับ props ที่ component นี้รับ
interface typeofModalProps {
  open: boolean; // ควบคุมการเปิด/ปิด Modal
  onClose: () => void; // ฟังก์ชันเมื่อปิด Modal
  initialDetail: typeOfFormData; // ข้อมูลเริ่มต้นสำหรับฟอร์ม
  onSubmit: (updatedData: typeOfFormData) => void; // ฟังก์ชันเมื่อ submit ฟอร์ม
  openModalFor: string; // โหมดของ Modal ("create", "update", "read")
  organizationDD: Array<typeOfDD>; // Dropdown สำหรับ Organization (รวม Informal และ Legal)
  partyTypeDD: Array<typeOfDD>; // Dropdown สำหรับ PartyType
  industryTypeDD: Array<typeOfDD>; // Dropdown สำหรับ IndustryType
}

// Component หลักสำหรับแสดง Modal
export default function Modal_classifybyindustry({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
  organizationDD,
  partyTypeDD,
  industryTypeDD,
}: typeofModalProps) {
  // State สำหรับเก็บข้อมูลฟอร์ม
  const [formData, setFormData] = useState<typeOfFormData>({
    id: null,
    fromdate: "",
    thrudate: "",
    party_id: "",
    party_type_id: "",
    industry_type_id: "",
  });

  // useEffect สำหรับอัพเดท formData เมื่อ initialDetail เปลี่ยน
  useEffect(() => {
    console.log("form initial detail = ", initialDetail);
    setFormData({
      ...initialDetail,
      party_id: initialDetail.party_id === 0 ? "" : initialDetail.party_id, // แปลง 0 เป็น "" เพื่อป้องกัน warning
      party_type_id: initialDetail.party_type_id === 0 ? "" : initialDetail.party_type_id,
      industry_type_id: initialDetail.industry_type_id === 0 ? "" : initialDetail.industry_type_id,
    });
  }, [initialDetail]);

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ DateField
  const handleDateChange = (name: string, value: dayjs.Dayjs | null) => {
    const dateValue = value ? value.format("YYYY-MM-DD") : ""; // แปลงเป็น YYYY-MM-DD หรือ ""
    setFormData({ ...formData, [name]: dateValue });
  };

  // ฟังก์ชันจัดการการเปลี่ยนแปลงของ Select
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: Number(value) || "", // แปลงเป็น number หรือ "" สำหรับ dropdown
    });
  };

  // ฟังก์ชันจัดการการ submit ฟอร์ม
  const handleSubmit = () => {
    // Validation เพื่อป้องกันข้อมูลไม่สมบูรณ์
    if (!formData.fromdate) {
      alert("From Date is required");
      return;
    }
    if (!formData.party_id) {
      alert("Organization is WHAT");
      return;
    }
    if (!formData.party_type_id) {
      alert("Party Type is required");
      return;
    }
    if (!formData.industry_type_id) {
      alert("Industry Type is required");
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
          Industry Classification Details
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

        {/* Dropdown สำหรับเลือก Organization (รวม Informal และ Legal) */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="organization-select-label">Organization</InputLabel>
          <Select
            labelId="organization-select-label"
            name="party_id"
            value={formData.party_id || ""}
            onChange={handleChange}
            disabled={openModalFor === "read"}
            required
          >
            <MenuItem value="">
              <em>Select Organization</em>
            </MenuItem>
            {organizationDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text} ({item.type === "informal" ? "inform" : "legal"})
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Dropdown สำหรับเลือก Party Type */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="party-type-select-label">Party Type</InputLabel>
          <Select
            labelId="party-type-select-label"
            name="party_type_id"
            value={formData.party_type_id || ""}
            onChange={handleChange}
            disabled={openModalFor === "read"}
            required
          >
            <MenuItem value="">
              <em>Select Party Type</em>
            </MenuItem>
            {partyTypeDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        {/* Dropdown สำหรับเลือก Industry Type */}
        <FormControl fullWidth margin="normal">
          <InputLabel id="industry-type-select-label">Industry Type</InputLabel>
          <Select
            labelId="industry-type-select-label"
            name="industry_type_id"
            value={formData.industry_type_id || ""}
            onChange={handleChange}
            disabled={openModalFor === "read"}
            required
          >
            <MenuItem value="">
              <em>Select Industry Type</em>
            </MenuItem>
            {industryTypeDD.map((item) => (
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
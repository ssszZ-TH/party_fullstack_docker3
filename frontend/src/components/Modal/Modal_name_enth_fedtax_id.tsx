import React, { useState, useEffect } from "react";
import { Modal, Box, Button, TextField, Typography, Stack } from "@mui/material";
import SaveButton from "../buttons/SaveButton";

interface typeOfFormData {
  id: number | null;
  name_en: string;
  name_th: string;
  federal_tax_id_number: string;
}

const style = {
  position: "absolute" as "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  boxShadow: 24,
  p: 4,
};

interface typeofModalProps {
  open: boolean;
  onClose: () => void;
  initialDetail: typeOfFormData;
  onSubmit: (updatedCountry: typeOfFormData) => void;
  openModalFor: string;
}

export default function Modal_name_enth_fedtax_id({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
}: typeofModalProps) {
  const [formData, setFormData] = useState<typeOfFormData>({
    id: null,
    name_en: "",
    name_th: "",
    federal_tax_id_number: "",
  });

  // ใช้ useEffect เพื่ออัปเดต formData เมื่อ initialDetail เปลี่ยน
  useEffect(() => {
    // ตรวจสอบว่า initialDetail มีข้อมูลที่จะใช้
    console.log("form initial detail = ", initialDetail);
    setFormData(initialDetail);
  }, [initialDetail]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = () => {
    onSubmit(formData);
    onClose();
  };

  useEffect(() => {
    console.log("openModalFor = ", openModalFor);
  }, [openModalFor]);

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Details
        </Typography>
        <TextField
          label="name_en"
          name="name_en"
          value={formData.name_en}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="name_th"
          name="name_th"
          value={formData.name_th}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />
        <TextField
          label="federal_tax_id_number"
          name="federal_tax_id_number"
          value={formData.federal_tax_id_number}
          onChange={handleChange}
          fullWidth
          margin="normal"
        />

        {/* ใช้ Stack เพื่อจัดตำแหน่งปุ่ม */}
        <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
          <SaveButton onClick={handleSubmit} />
        </Stack>
      </Box>
    </Modal>
  );
}


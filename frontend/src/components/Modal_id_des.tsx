import React, { useState, useEffect } from "react";
import { Modal, Box, TextField, Typography, Stack } from "@mui/material"; // เพิ่ม Stack
import SaveButton from "../components/buttons/SaveButton";

interface typeOfFormData {
  id: number | null;
  description: string;
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

export default function MaritalStatusTypeModal({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
}: typeofModalProps) {
  const [formData, setFormData] = useState<typeOfFormData>({
    id: null,
    description: "",
  });

  useEffect(() => {
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
          label="Description"
          name="description"
          value={formData.description}
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
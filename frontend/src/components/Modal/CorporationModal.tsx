import React, { useState, useEffect } from "react";
import { Modal, Box, TextField, Typography, Stack } from "@mui/material";
import SaveButton from "../buttons/SaveButton";

interface typeOfFormData {
  id: number | null;
  name_en: string;
  name_th: string;
  federal_tax_id_number?: string;
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
  onSubmit: (updatedData: typeOfFormData) => void;
  openModalFor: string;
}

export default function CorporationModal({
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
    if (!formData.name_en) {
      alert("English Name is required");
      return;
    }
    if (!formData.name_th) {
      alert("Thai Name is required");
      return;
    }
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
          Corporation Details
        </Typography>
        <TextField
          label="English Name"
          name="name_en"
          value={formData.name_en}
          onChange={handleChange}
          fullWidth
          margin="normal"
          disabled={openModalFor === "read"}
          required
        />
        <TextField
          label="Thai Name"
          name="name_th"
          value={formData.name_th}
          onChange={handleChange}
          fullWidth
          margin="normal"
          disabled={openModalFor === "read"}
          required
        />
        <TextField
          label="Federal Tax ID Number"
          name="federal_tax_id_number"
          value={formData.federal_tax_id_number || ""}
          onChange={handleChange}
          fullWidth
          margin="normal"
          disabled={openModalFor === "read"}
        />
        {openModalFor !== "read" && (
          <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
            <SaveButton onClick={handleSubmit} />
          </Stack>
        )}
      </Box>
    </Modal>
  );
}
import React, { useState, useEffect } from "react";
import { Modal, Box, TextField, Typography, Stack, MenuItem } from "@mui/material";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { DateField } from "@mui/x-date-pickers/DateField";
import dayjs from "dayjs";
import SaveButton from "../buttons/SaveButton";

interface FormData {
  id: number | null;
  socialsecuritynumber: string;
  birthdate: string;
  mothermaidenname: string;
  totalyearworkexperience: number;
  comment: string;
  gender_type_id?: number;
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

interface ModalProps {
  open: boolean;
  onClose: () => void;
  initialDetail: FormData;
  onSubmit: (updatedPerson: FormData) => void;
  openModalFor: string;
  genderTypes: { id: number; description: string }[];
}

export default function PersonModal({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
  genderTypes,
}: ModalProps) {
  const [formData, setFormData] = useState<FormData>({
    id: null,
    socialsecuritynumber: "",
    birthdate: "",
    mothermaidenname: "",
    totalyearworkexperience: 0,
    comment: "",
    gender_type_id: 0,
  });



  useEffect(() => {
    console.log("PersonModal: form initial detail = ", initialDetail);
    setFormData(initialDetail);
  }, [initialDetail]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === "totalyearworkexperience" ? Number(value) : name === "gender_type_id" ? Number(value) : value,
    });
  };

  const handleDateChange = (name: string, value: dayjs.Dayjs | null) => {
    const dateValue = value ? value.format("YYYY-MM-DD") : "";
    setFormData({ ...formData, [name]: dateValue });
  };

  const handleSubmit = () => {
    if (!formData.birthdate) {
      alert("Birth Date is required");
      return;
    }
    onSubmit(formData);
  };

  useEffect(() => {
    console.log("PersonModal: openModalFor = ", openModalFor);
  }, [openModalFor]);

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <Modal open={open} onClose={onClose}>
        <Box sx={style}>
          <Typography variant="h6" component="h2">
            Person Details
          </Typography>
          <TextField
            label="Social Security Number"
            name="socialsecuritynumber"
            value={formData.socialsecuritynumber}
            onChange={handleChange}
            fullWidth
            margin="normal"
            disabled={openModalFor === "read"}
          />
          <DateField
            label="Birth Date"
            name="birthdate"
            value={formData.birthdate ? dayjs(formData.birthdate) : null}
            onChange={(newValue) => handleDateChange("birthdate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
            disabled={openModalFor === "read"}
            required
          />
          <TextField
            label="Mother's Maiden Name"
            name="mothermaidenname"
            value={formData.mothermaidenname}
            onChange={handleChange}
            fullWidth
            margin="normal"
            disabled={openModalFor === "read"}
          />
          <TextField
            label="Total Years Work Experience"
            name="totalyearworkexperience"
            type="number"
            value={formData.totalyearworkexperience}
            onChange={handleChange}
            fullWidth
            margin="normal"
            disabled={openModalFor === "read"}
          />
          <TextField
            select
            label="Gender"
            name="gender_type_id"
            value={formData.gender_type_id || ""}
            onChange={handleChange}
            fullWidth
            margin="normal"
            disabled={openModalFor === "read"}
          >
            <MenuItem value="">None</MenuItem>
            {genderTypes.map((gender) => (
              <MenuItem key={gender.id} value={gender.id}>
                {gender.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Comment"
            name="comment"
            value={formData.comment}
            onChange={handleChange}
            fullWidth
            margin="normal"
            multiline
            rows={3}
            disabled={openModalFor === "read"}
          />
          {openModalFor !== "read" && (
            <Stack direction="row" justifyContent="flex-end" sx={{ mt: 2 }}>
              <SaveButton onClick={handleSubmit} />
            </Stack>
          )}
        </Box>
      </Modal>
    </LocalizationProvider>
  );
}
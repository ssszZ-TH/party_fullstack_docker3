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
import SaveButton from "./buttons/SaveButton";
import { TextField } from "@mui/material";

interface FormData {
  id: number | null;
  fromdate: string;
  thrudate: string | null;
  person_id: number;
  personnametype_id: number;
  name: string;
}

interface DropdownItem {
  id: number;
  text: string;
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
  onSubmit: (updatedPersonName: FormData) => void;
  openModalFor: string;
  personDD: DropdownItem[];
  personNameTypeDD: DropdownItem[];
}

export default function PersonNameModal({
  open,
  onClose,
  initialDetail,
  onSubmit,
  openModalFor,
  personDD,
  personNameTypeDD,
}: ModalProps) {
  const [formData, setFormData] = useState<FormData>({
    id: null,
    fromdate: "",
    thrudate: null,
    person_id: 0,
    personnametype_id: 0,
    name: "",
  });

  useEffect(() => {
    console.log("PersonNameModal: form initial detail = ", initialDetail);
    setFormData(initialDetail);
  }, [initialDetail]);

  const handleDateChange = (name: string, value: dayjs.Dayjs | null) => {
    const dateValue = value ? value.format("YYYY-MM-DD") : name === "thrudate" ? null : "";
    setFormData({ ...formData, [name]: dateValue });
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | { name?: string; value: unknown }>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]:
        name === "person_id" || name === "personnametype_id"
          ? Number(value)
          : value,
    });
  };

  const handleSubmit = () => {
    if (!formData.fromdate) {
      alert("From Date is required");
      return;
    }
    if (!formData.person_id) {
      alert("Person is required");
      return;
    }
    if (!formData.personnametype_id) {
      alert("Person Name Type is required");
      return;
    }
    if (!formData.name) {
      alert("Name is required");
      return;
    }
    onSubmit(formData);
    onClose();
  };

  useEffect(() => {
    console.log("PersonNameModal: openModalFor = ", openModalFor);
  }, [openModalFor]);

  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={style}>
        <Typography variant="h6" component="h2">
          Person Name Details
        </Typography>

        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DateField
            label="From Date"
            value={formData.fromdate ? dayjs(formData.fromdate) : null}
            onChange={(newValue) => handleDateChange("fromdate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
            required
          />
          <DateField
            label="Thru Date"
            value={formData.thrudate ? dayjs(formData.thrudate) : null}
            onChange={(newValue) => handleDateChange("thrudate", newValue)}
            format="YYYY-MM-DD"
            fullWidth
            margin="normal"
            sx={{ mb: 2 }}
          />
        </LocalizationProvider>

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

        <FormControl fullWidth margin="normal">
          <InputLabel id="personnametype-select-label">Person Name Type</InputLabel>
          <Select
            labelId="personnametype-select-label"
            name="personnametype_id"
            value={formData.personnametype_id || ""}
            onChange={handleChange}
            disabled={openModalFor === "read"}
            required
          >
            <MenuItem value="">
              <em>Select Name Type</em>
            </MenuItem>
            {personNameTypeDD.map((item) => (
              <MenuItem key={item.id} value={item.id}>
                {item.text}
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <TextField
          label="Name"
          name="name"
          value={formData.name}
          onChange={handleChange}
          fullWidth
          margin="normal"
          disabled={openModalFor === "read"}
          required
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
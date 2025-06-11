import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/person";
import { list as listGenderTypes } from "../../services/gendertype";
import { list as listMaritalStatusTypes } from "../../services/maritalstatustype";
import { list as listCountries } from "../../services/country";
import {
  Box,
  Typography,
  Button,
  Alert,
  TextField,
  MenuItem,
} from "@mui/material";
import DeleteButton from "../../components/buttons/DeleteButton";
import SaveButton from "../../components/buttons/SaveButton";
import CancelButton from "../../components/buttons/CancelButton";
import CitizenshipButton from "../../components/buttons/CitizenshipButton";

interface Person {
  id: number;
  personal_id_number: string;
  birthdate?: string;
  comment: string;
  gender_type_id?: number;
  gender_description?: string;
  fname?: string;
  mname?: string;
  lname?: string;
  nickname?: string;
  marital_status_type_id?: number;
  height_val?: number;
  weight_val?: number;
  country_id?: number;
  citizenship_id?: number;
}

export default function PersonDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [person, setPerson] = useState<Person | null>(null);
  const [formData, setFormData] = useState<Person | null>(null);
  const [genderTypes, setGenderTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [maritalStatusTypes, setMaritalStatusTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [countries, setCountries] = useState<{ id: number; name_en: string; name_th: string }[]>(
    []
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        console.log("Create new person");
        setCurrentId(null);
        setFormData({
          id: 0,
          personal_id_number: "",
          birthdate: "",
          comment: "",
          gender_type_id: undefined,
          fname: "",
          mname: "",
          lname: "",
          nickname: "",
          marital_status_type_id: undefined,
          height_val: undefined,
          weight_val: undefined,
          country_id: undefined,
          citizenship_id: undefined,
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchPerson(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId]);

  useEffect(() => {
    console.log("Person data from backend", person);
  }, [person]);

  // useEffect(() => {
  //   console.log("Form data", formData);
  // }, [formData]);

  const fetchPerson = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setPerson(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch person details");
      console.error("Error fetching person:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdowns = async () => {
    try {
      const [genderData, maritalData, countryData] = await Promise.all([
        listGenderTypes(),
        listMaritalStatusTypes(),
        listCountries(),
      ]);
      setGenderTypes(genderData);
      setMaritalStatusTypes(maritalData);
      setCountries(countryData);
    } catch (error) {
      console.error("Failed to fetch dropdown data:", error);
      setError("Failed to load dropdown options");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => (prev ? { ...prev, [name]: value } : null));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) return;
    setLoading(true);
    try {
      const payload = {
        id: currentId || 0,
        personal_id_number: formData.personal_id_number,
        birthdate: formData.birthdate || undefined,
        comment: formData.comment,
        gender_type_id: formData.gender_type_id
          ? Number(formData.gender_type_id)
          : undefined,
        fname: formData.fname,
        mname: formData.mname,
        lname: formData.lname,
        nickname: formData.nickname,
        marital_status_type_id: formData.marital_status_type_id
          ? Number(formData.marital_status_type_id)
          : undefined,
        height_val: formData.height_val
          ? Number(formData.height_val)
          : undefined,
        weight_val: formData.weight_val
          ? Number(formData.weight_val)
          : undefined,
        country_id: formData.country_id
          ? Number(formData.country_id)
          : undefined,
      };
      if (payload.id === 0) {
        console.log("Created person with payload:", payload);
        await create(payload);
      } else {
        console.log("Updated person with payload:", payload);
        await update(payload);
      }
      navigate("/v1/person");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create person"
          : "Failed to update person";
      setError(errorMessage);
      console.error(`${errorMessage}:`, err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!currentId) return;
    setLoading(true);
    try {
      await deleteById({ id: currentId });
      console.log(`Deleted person with id: ${currentId}`);
      navigate("/v1/person");
    } catch (err: any) {
      setError("Failed to delete person");
      console.error("Failed to delete person:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Person Detail รายละเอียดบุคคล" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Person Detail รายละเอียดบุคคล" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Person Detail รายละเอียดบุคคล id: ${currentId}`
            : "Create Person สร้างบุคคล"
        }
      />
      <form onSubmit={handleSubmit}>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "repeat(2, 1fr)",
              md: "repeat(3, 1fr)",
            },
            gap: 2,
            mt: 2,
            px: 2,
          }}
        >
          <TextField
            label="Personal ID Number"
            name="personal_id_number"
            value={formData.personal_id_number}
            onChange={handleChange}
            fullWidth
            required
          />
          <TextField
            label="First Name"
            name="fname"
            value={formData.fname || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            label="Middle Name"
            name="mname"
            value={formData.mname || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            label="Last Name"
            name="lname"
            value={formData.lname || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            label="Nickname"
            name="nickname"
            value={formData.nickname || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            label="Birthdate"
            name="birthdate"
            type="date"
            value={formData.birthdate || ""}
            onChange={handleChange}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            select
            label="Gender"
            name="gender_type_id"
            value={formData.gender_type_id || ""}
            onChange={handleChange}
            fullWidth
          >
            {genderTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Marital Status"
            name="marital_status_type_id"
            value={formData.marital_status_type_id || ""}
            onChange={handleChange}
            fullWidth
          >
            <MenuItem value="">None</MenuItem>
            {maritalStatusTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Citizenship Country"
            name="country_id"
            value={formData.country_id || ""}
            onChange={handleChange}
            fullWidth
          >
            <MenuItem value="">None</MenuItem>
            {countries.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {`${option.name_en} (${option.name_th})`}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Height (cm)"
            name="height_val"
            type="number"
            value={formData.height_val || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            label="Weight (kg)"
            name="weight_val"
            type="number"
            value={formData.weight_val || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            label="Comment"
            name="comment"
            value={formData.comment}
            onChange={handleChange}
            fullWidth
          />
        </Box>
        <Box
          sx={{
            mt: 3,
            display: "flex",
            gap: 2,
            px: 2,
            justifyContent: "space-between",
          }}
        >
          <Box sx={{ display: "flex", gap: 2 }}>
            <CancelButton onClick={() => navigate("/v1/person")} />
            {currentId && currentId > 0 && (
              <DeleteButton onClick={handleDelete} />
            )}
          </Box>
          <Box sx={{ display: "flex", gap: 2 }}>
            {currentId && currentId > 0 && (
              <CitizenshipButton
                onClick={() =>
                  navigate(
                    `/v1/passportbycitizenshipid/${formData?.citizenship_id}`
                  )
                }
                disabled={!formData?.citizenship_id}
              />
            )}
            <SaveButton onClick={handleSubmit} />
          </Box>
        </Box>
      </form>
    </Box>
  );
}

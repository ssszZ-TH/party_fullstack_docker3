import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/corporation";
import {
  Box,
  Typography,
  Alert,
  TextField,
} from "@mui/material";
import DeleteButton from "../../components/buttons/DeleteButton";
import SaveButton from "../../components/buttons/SaveButton";
import CancelButton from "../../components/buttons/CancelButton";

interface Corporation {
  id: number;
  name_en: string;
  name_th: string;
  federal_tax_id_number?: string;
}

export default function CorporationDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [corporation, setCorporation] = useState<Corporation | null>(null);
  const [formData, setFormData] = useState<Corporation | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        setCurrentId(null);
        setFormData({
          id: 0,
          name_en: "",
          name_th: "",
          federal_tax_id_number: "",
        });
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchCorporation(parsedId);
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId]);

  const fetchCorporation = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setCorporation(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch corporation details");
      console.error("Error fetching corporation:", err);
    } finally {
      setLoading(false);
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
        name_en: formData.name_en,
        name_th: formData.name_th,
        federal_tax_id_number: formData.federal_tax_id_number || undefined,
      };
      if (payload.id === 0) {
        await create(payload);
      } else {
        await update(payload);
      }
      navigate("/v1/corporation");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create corporation"
          : "Failed to update corporation";
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
      navigate("/v1/corporation");
    } catch (err: any) {
      setError("Failed to delete corporation");
      console.error("Failed to delete corporation:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Corporation Detail รายละเอียดบริษัท" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Corporation Detail รายละเอียดบริษัท" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Corporation Detail รายละเอียดบริษัท id: ${currentId}`
            : "Create Corporation สร้างบริษัท"
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
            label="Name (English)"
            name="name_en"
            value={formData.name_en}
            onChange={handleChange}
            fullWidth
            required
          />
          <TextField
            label="Name (Thai)"
            name="name_th"
            value={formData.name_th}
            onChange={handleChange}
            fullWidth
            required
          />
          <TextField
            label="Federal Tax ID Number"
            name="federal_tax_id_number"
            value={formData.federal_tax_id_number || ""}
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
            <CancelButton onClick={() => navigate("/v1/corporation")} />
            {currentId && currentId > 0 && (
              <DeleteButton onClick={handleDelete} />
            )}
          </Box>
          <Box sx={{ display: "flex", gap: 2 }}>
            <SaveButton onClick={handleSubmit} />
          </Box>
        </Box>
      </form>
    </Box>
  );
}
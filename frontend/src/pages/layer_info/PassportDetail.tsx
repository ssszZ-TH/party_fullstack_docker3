import React, { useState, useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/passport";
import {
  Box,
  Typography,
  Alert,
  TextField,
} from "@mui/material";
import DeleteButton from "../../components/buttons/DeleteButton";
import SaveButton from "../../components/buttons/SaveButton";
import CancelButton from "../../components/buttons/CancelButton";

interface Passport {
  id: number;
  passportnumber: string;
  fromdate?: string;
  thrudate?: string;
  citizenship_id?: number;
}

export default function PassportDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [passport, setPassport] = useState<Passport | null>(null);
  const [formData, setFormData] = useState<Passport | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const citizenshipId = searchParams.get("citizenship_id");

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        setCurrentId(null);
        setFormData({
          id: 0,
          passportnumber: "",
          fromdate: "",
          thrudate: "",
          citizenship_id: citizenshipId ? Number(citizenshipId) : undefined,
        });
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchPassport(parsedId);
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId, citizenshipId]);

  const fetchPassport = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setPassport(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch passport details");
      console.error("Error fetching passport:", err);
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
        passportnumber: formData.passportnumber,
        fromdate: formData.fromdate || undefined,
        thrudate: formData.thrudate || undefined,
        citizenship_id: formData.citizenship_id
          ? Number(formData.citizenship_id)
          : undefined,
      };
      if (payload.id === 0) {
        await create(payload);
      } else {
        await update(payload);
      }
      navigate("/v1/passport");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create passport"
          : "Failed to update passport";
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
      navigate("/v1/passport");
    } catch (err: any) {
      setError("Failed to delete passport");
      console.error("Failed to delete passport:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Passport Detail รายละเอียดหนังสือเดินทาง" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Passport Detail รายละเอียดหนังสือเดินทาง" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Passport Detail รายละเอียดหนังสือเดินทาง id: ${currentId}`
            : "Create Passport สร้างหนังสือเดินทาง"
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
            label="Passport Number"
            name="passportnumber"
            value={formData.passportnumber}
            onChange={handleChange}
            fullWidth
            required
          />
          <TextField
            label="Issue Date"
            name="fromdate"
            type="date"
            value={formData.fromdate || ""}
            onChange={handleChange}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Expiry Date"
            name="thrudate"
            type="date"
            value={formData.thrudate || ""}
            onChange={handleChange}
            fullWidth
            InputLabelProps={{ shrink: true }}
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
            <CancelButton onClick={() => navigate("/v1/passport")} />
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
import React, { useState, useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/classifybyeeoc";
import { list as listEthnicity } from "../../services/ethnicity";
import {
  Box,
  Typography,
  Alert,
  TextField,
  MenuItem,
} from "@mui/material";
import DeleteButton from "../../components/buttons/DeleteButton";
import SaveButton from "../../components/buttons/SaveButton";
import CancelButton from "../../components/buttons/CancelButton";

interface Eeoc {
  id: number;
  fromdate?: string;
  thrudate?: string;
  party_id?: number;
  ethnicity_id?: number;
}

export default function EeocDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [eeoc, setEeoc] = useState<Eeoc | null>(null);
  const [formData, setFormData] = useState<Eeoc | null>(null);
  const [ethnicities, setEthnicities] = useState<
    { id: number; name_en: string; name_th: string }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const partyId = searchParams.get("party_id");

  useEffect(() => {
    const fetchDropdowns = async () => {
      try {
        const ethnicityData = await listEthnicity();
        setEthnicities(ethnicityData);
      } catch (error) {
        console.error("Failed to fetch ethnicity data:", error);
        setError("Failed to load dropdown options");
      }
    };

    if (paramId) {
      if (paramId === "new") {
        if (!partyId) {
          setError("Party ID is required to create a new EEOC");
          setLoading(false);
          return;
        }
        setCurrentId(null);
        setFormData({
          id: 0,
          fromdate: "",
          thrudate: "",
          party_id: Number(partyId),
          ethnicity_id: undefined,
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchEeoc(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId, partyId]);

  const fetchEeoc = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setEeoc(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch EEOC details");
      console.error("Error fetching EEOC:", err);
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
    if (!formData || !formData.party_id) {
      setError("Party ID is required");
      return;
    }
    setLoading(true);
    try {
      const payload = {
        id: currentId || 0,
        fromdate: formData.fromdate || undefined,
        thrudate: formData.thrudate || undefined,
        party_id: Number(formData.party_id),
        party_type_id: 2, // Default value for EEOC classification
        ethnicity_id: formData.ethnicity_id ? Number(formData.ethnicity_id) : undefined,
      };
      if (payload.id === 0) {
        await create(payload);
      } else {
        await update(payload);
      }
      navigate(`/v1/eeocbypersonid/${formData.party_id}`);
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create EEOC"
          : "Failed to update EEOC";
      setError(errorMessage);
      console.error(`${errorMessage}:`, err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!currentId || !formData?.party_id) return;
    setLoading(true);
    try {
      await deleteById({ id: currentId });
      navigate(`/v1/eeocbypersonid/${formData.party_id}`);
    } catch (err: any) {
      setError("Failed to delete EEOC");
      console.error("Failed to delete EEOC:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="EEOC Detail รายละเอียดการจำแนกเชื้อชาติ" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="EEOC Detail รายละเอียดการจำแนกเชื้อชาติ" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `EEOC Detail รายละเอียดการจำแนกเชื้อชาติ id: ${currentId}`
            : "Create EEOC สร้างการจำแนกเชื้อชาติ"
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
            select
            label="Ethnicity"
            name="ethnicity_id"
            value={formData.ethnicity_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            <MenuItem value="">Select Ethnicity</MenuItem>
            {ethnicities.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {`${option.name_en} (${option.name_th})`}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="From Date"
            name="fromdate"
            type="date"
            value={formData.fromdate || ""}
            onChange={handleChange}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Thru Date"
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
            <CancelButton onClick={() => navigate(`/v1/eeocbypersonid/${formData.party_id}`)} />
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
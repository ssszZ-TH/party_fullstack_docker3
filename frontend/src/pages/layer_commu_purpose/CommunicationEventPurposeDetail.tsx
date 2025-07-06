import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/communicationeventpurpose";
import { list as listCommunicationEvents } from "../../services/communicationevent";
import { list as listCommunicationEventPurposeTypes } from "../../services/communicationeventpurposetype";
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

interface CommunicationEventPurpose {
  id: number;
  communication_event_id: number;
  communication_event_purpose_type_id: number;
}

export default function CommunicationEventPurposeDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [communicationEventPurpose, setCommunicationEventPurpose] = useState<CommunicationEventPurpose | null>(null);
  const [formData, setFormData] = useState<CommunicationEventPurpose | null>(null);
  const [communicationEvents, setCommunicationEvents] = useState<
    { id: number; note?: string }[]
  >([]);
  const [communicationEventPurposeTypes, setCommunicationEventPurposeTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        console.log("Create new communication event purpose");
        setCurrentId(null);
        setFormData({
          id: 0,
          communication_event_id: 0,
          communication_event_purpose_type_id: 0,
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchCommunicationEventPurpose(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId]);

  const fetchCommunicationEventPurpose = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setCommunicationEventPurpose(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch communication event purpose details");
      console.error("Error fetching communication event purpose:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdowns = async () => {
    try {
      const [eventData, purposeTypeData] = await Promise.all([
        listCommunicationEvents(),
        listCommunicationEventPurposeTypes(),
      ]);
      setCommunicationEvents(eventData);
      setCommunicationEventPurposeTypes(purposeTypeData);
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
        communication_event_id: Number(formData.communication_event_id),
        communication_event_purpose_type_id: Number(formData.communication_event_purpose_type_id),
      };
      if (payload.id === 0) {
        console.log("Created communication event purpose with payload:", payload);
        await create(payload);
      } else {
        console.log("Updated communication event purpose with payload:", payload);
        await update(payload);
      }
      navigate("/v1/communicationeventpurpose");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create communication event purpose"
          : "Failed to update communication event purpose";
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
      console.log(`Deleted communication event purpose with id: ${currentId}`);
      navigate("/v1/communicationeventpurpose");
    } catch (err: any) {
      setError("Failed to delete communication event purpose");
      console.error("Failed to delete communication event purpose:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Communication Event Purpose Detail รายละเอียดวัตถุประสงค์เหตุการณ์การสื่อสาร" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Communication Event Purpose Detail รายละเอียดวัตถุประสงค์เหตุการณ์การสื่อสาร" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Communication Event Purpose Detail รายละเอียดวัตถุประสงค์เหตุการณ์การสื่อสาร id: ${currentId}`
            : "Create Communication Event Purpose สร้างวัตถุประสงค์เหตุการณ์การสื่อสาร"
        }
      />
      <form onSubmit={handleSubmit}>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "repeat(2, 1fr)",
            },
            gap: 2,
            mt: 2,
            px: 2,
          }}
        >
          <TextField
            select
            label="Communication Event"
            name="communication_event_id"
            value={formData.communication_event_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {communicationEvents.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.id} {option.note ? `(${option.note})` : ''}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Purpose Type"
            name="communication_event_purpose_type_id"
            value={formData.communication_event_purpose_type_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {communicationEventPurposeTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
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
            <CancelButton onClick={() => navigate("/v1/communicationeventpurpose")} />
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
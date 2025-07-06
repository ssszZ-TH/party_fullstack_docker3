import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/communicationevent";
import { list as listContactMechanismTypes } from "../../services/contactmechanismtype";
import { list as listCommunicationEventStatusTypes } from "../../services/communicationeventstatustype";
import { list as listPartyRelationships } from "../../services/partyrelationship";
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

interface CommunicationEvent {
  id: number;
  datetime_start: string;
  datetime_end: string;
  note?: string;
  contact_mechanism_type_id: number;
  communication_event_status_type_id: number;
  party_relationship_id: number;
}

export default function CommunicationEventDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [communicationEvent, setCommunicationEvent] = useState<CommunicationEvent | null>(null);
  const [formData, setFormData] = useState<CommunicationEvent | null>(null);
  const [contactMechanismTypes, setContactMechanismTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [communicationEventStatusTypes, setCommunicationEventStatusTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [partyRelationships, setPartyRelationships] = useState<
    { id: number; comment?: string }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        console.log("Create new communication event");
        setCurrentId(null);
        setFormData({
          id: 0,
          datetime_start: "",
          datetime_end: "",
          note: "",
          contact_mechanism_type_id: 0,
          communication_event_status_type_id: 0,
          party_relationship_id: 0,
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchCommunicationEvent(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId]);

  const fetchCommunicationEvent = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setCommunicationEvent(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch communication event details");
      console.error("Error fetching communication event:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdowns = async () => {
    try {
      const [contactMechanismTypeData, statusTypeData, partyRelationshipData] = await Promise.all([
        listContactMechanismTypes(),
        listCommunicationEventStatusTypes(),
        listPartyRelationships(),
      ]);
      setContactMechanismTypes(contactMechanismTypeData);
      setCommunicationEventStatusTypes(statusTypeData);
      setPartyRelationships(partyRelationshipData);
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
        datetime_start: formData.datetime_start,
        datetime_end: formData.datetime_end,
        note: formData.note || undefined,
        contact_mechanism_type_id: Number(formData.contact_mechanism_type_id),
        communication_event_status_type_id: Number(formData.communication_event_status_type_id),
        party_relationship_id: Number(formData.party_relationship_id),
      };
      if (payload.id === 0) {
        console.log("Created communication event with payload:", payload);
        await create(payload);
      } else {
        console.log("Updated communication event with payload:", payload);
        await update(payload);
      }
      navigate("/v1/communicationevent");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create communication event"
          : "Failed to update communication event";
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
      console.log(`Deleted communication event with id: ${currentId}`);
      navigate("/v1/communicationevent");
    } catch (err: any) {
      setError("Failed to delete communication event");
      console.error("Failed to delete communication event:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Communication Event Detail รายละเอียดเหตุการณ์การสื่อสาร" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Communication Event Detail รายละเอียดเหตุการณ์การสื่อสาร" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Communication Event Detail รายละเอียดเหตุการณ์การสื่อสาร id: ${currentId}`
            : "Create Communication Event สร้างเหตุการณ์การสื่อสาร"
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
            label="Start DateTime"
            name="datetime_start"
            type="datetime-local"
            value={formData.datetime_start || ""}
            onChange={handleChange}
            fullWidth
            required
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="End DateTime"
            name="datetime_end"
            type="datetime-local"
            value={formData.datetime_end || ""}
            onChange={handleChange}
            fullWidth
            required
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Note"
            name="note"
            value={formData.note || ""}
            onChange={handleChange}
            fullWidth
          />
          <TextField
            select
            label="Contact Mechanism Type"
            name="contact_mechanism_type_id"
            value={formData.contact_mechanism_type_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {contactMechanismTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Status Type"
            name="communication_event_status_type_id"
            value={formData.communication_event_status_type_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {communicationEventStatusTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Party Relationship"
            name="party_relationship_id"
            value={formData.party_relationship_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {partyRelationships.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.id} {option.comment ? `(${option.comment})` : ''}
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
            <CancelButton onClick={() => navigate("/v1/communicationevent")} />
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
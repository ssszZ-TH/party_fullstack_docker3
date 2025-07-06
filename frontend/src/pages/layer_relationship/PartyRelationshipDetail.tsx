import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/partyrelationship";
import { list as listPartyRoles } from "../../services/partyrole";
import { list as listPartyRelationshipTypes } from "../../services/partyrelationshiptype";
import { list as listPriorityTypes } from "../../services/prioritytype";
import { list as listPartyRelationshipStatusTypes } from "../../services/partyrelationshipstatustype";
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

interface PartyRelationship {
  id: number;
  from_date: string;
  thru_date?: string;
  comment?: string;
  from_party_role_id: number;
  to_party_role_id: number;
  party_relationship_type_id: number;
  priority_type_id: number;
  party_relationship_status_type_id?: number;
}

interface PartyRole {
  id: number;
  party_id: number;
  type: string;
  name_en?: string;
  name_th?: string;
  personal_id_number?: string;
}

export default function PartyRelationshipDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [partyRelationship, setPartyRelationship] = useState<PartyRelationship | null>(null);
  const [formData, setFormData] = useState<PartyRelationship | null>(null);
  const [partyRoles, setPartyRoles] = useState<PartyRole[]>([]);
  const [partyRelationshipTypes, setPartyRelationshipTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [priorityTypes, setPriorityTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [partyRelationshipStatusTypes, setPartyRelationshipStatusTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        console.log("Create new party relationship");
        setCurrentId(null);
        setFormData({
          id: 0,
          from_date: "",
          thru_date: "",
          comment: "",
          from_party_role_id: 0,
          to_party_role_id: 0,
          party_relationship_type_id: 0,
          priority_type_id: 0,
          party_relationship_status_type_id: 0,
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchPartyRelationship(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId]);

  const fetchPartyRelationship = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setPartyRelationship(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch party relationship details");
      console.error("Error fetching party relationship:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdowns = async () => {
    try {
      const [partyRoleData, relationshipTypeData, priorityTypeData, statusTypeData] = await Promise.all([
        listPartyRoles(),
        listPartyRelationshipTypes(),
        listPriorityTypes(),
        listPartyRelationshipStatusTypes(),
      ]);
      const uniquePartyRoles = Array.from(
        new Map(partyRoleData.map((item: PartyRole) => [item.id, item])).values()
      );
      setPartyRoles(uniquePartyRoles);
      setPartyRelationshipTypes(relationshipTypeData);
      setPriorityTypes(priorityTypeData);
      setPartyRelationshipStatusTypes(statusTypeData);
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
        from_date: formData.from_date,
        thru_date: formData.thru_date || undefined,
        comment: formData.comment || undefined,
        from_party_role_id: Number(formData.from_party_role_id),
        to_party_role_id: Number(formData.to_party_role_id),
        party_relationship_type_id: Number(formData.party_relationship_type_id),
        priority_type_id: Number(formData.priority_type_id),
        party_relationship_status_type_id: Number(formData.party_relationship_status_type_id) || undefined,
      };
      if (payload.id === 0) {
        console.log("Created party relationship with payload:", payload);
        await create(payload);
      } else {
        console.log("Updated party relationship with payload:", payload);
        await update(payload);
      }
      navigate("/v1/partyrelationship");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create party relationship"
          : "Failed to update party relationship";
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
      console.log(`Deleted party relationship with id: ${currentId}`);
      navigate("/v1/partyrelationship");
    } catch (err: any) {
      setError("Failed to delete party relationship");
      console.error("Failed to delete party relationship:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Party Relationship Detail รายละเอียดความสัมพันธ์ของปาร์ตี้" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Party Relationship Detail รายละเอียดความสัมพันธ์ของปาร์ตี้" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Party Relationship Detail รายละเอียดความสัมพันธ์ของปาร์ตี้ id: ${currentId}`
            : "Create Party Relationship สร้างความสัมพันธ์ของปาร์ตี้"
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
            label="From Party Role"
            name="from_party_role_id"
            value={formData.from_party_role_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {partyRoles.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.type === "organization"
                  ? `${option.id} (organization) ${option.name_en || ''} ${option.name_th || ''}`
                  : `${option.id} (person) ${option.personal_id_number || ''}`}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="To Party Role"
            name="to_party_role_id"
            value={formData.to_party_role_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {partyRoles.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.type === "organization"
                  ? `${option.id} (organization) ${option.name_en || ''} ${option.name_th || ''}`
                  : `${option.id} (person) ${option.personal_id_number || ''}`}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Relationship Type"
            name="party_relationship_type_id"
            value={formData.party_relationship_type_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {partyRelationshipTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Priority Type"
            name="priority_type_id"
            value={formData.priority_type_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {priorityTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Status Type"
            name="party_relationship_status_type_id"
            value={formData.party_relationship_status_type_id || ""}
            onChange={handleChange}
            fullWidth
          >
            <MenuItem value="">None</MenuItem>
            {partyRelationshipStatusTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="From Date"
            name="from_date"
            type="date"
            value={formData.from_date || ""}
            onChange={handleChange}
            fullWidth
            required
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Thru Date"
            name="thru_date"
            type="date"
            value={formData.thru_date || ""}
            onChange={handleChange}
            fullWidth
            InputLabelProps={{ shrink: true }}
          />
          <TextField
            label="Comment"
            name="comment"
            value={formData.comment || ""}
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
            <CancelButton onClick={() => navigate("/v1/partyrelationship")} />
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
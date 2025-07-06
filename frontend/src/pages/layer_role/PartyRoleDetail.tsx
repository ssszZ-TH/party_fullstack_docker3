import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById, list } from "../../services/partyrole";
import { list as listRoleTypes } from "../../services/roletype";
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

interface PartyRole {
  id: number;
  party_id: number;
  role_type_id: number;
  fromdate: string;
  thrudate?: string;
  type: string;
  name_en?: string;
  name_th?: string;
  personal_id_number?: string;
  comment?: string;
  role_type_description?: string;
}

export default function PartyRoleDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [partyRole, setPartyRole] = useState<PartyRole | null>(null);
  const [formData, setFormData] = useState<PartyRole | null>(null);
  const [parties, setParties] = useState<PartyRole[]>([]);
  const [roleTypes, setRoleTypes] = useState<
    { id: number; description: string }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (paramId) {
      if (paramId === "new") {
        console.log("Create new party role");
        setCurrentId(null);
        setFormData({
          id: 0,
          party_id: 0,
          role_type_id: 0,
          fromdate: "",
          thrudate: "",
          type: "",
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchPartyRole(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId]);

  const fetchPartyRole = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setPartyRole(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch party role details");
      console.error("Error fetching party role:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdowns = async () => {
    try {
      const [partyData, roleTypeData] = await Promise.all([
        list(), // Use partyrole list instead of listParties
        listRoleTypes(),
      ]);
      // Deduplicate parties by party_id to avoid duplicate entries
      const uniqueParties = Array.from(
        new Map(partyData.map((item: PartyRole) => [item.party_id, item])).values()
      );
      setParties(uniqueParties);
      setRoleTypes(roleTypeData);
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
        party_id: Number(formData.party_id),
        role_type_id: Number(formData.role_type_id),
        fromdate: formData.fromdate,
        thrudate: formData.thrudate || undefined,
      };
      if (payload.id === 0) {
        console.log("Created party role with payload:", payload);
        await create(payload);
      } else {
        console.log("Updated party role with payload:", payload);
        await update(payload);
      }
      navigate("/v1/partyrole");
    } catch (err: any) {
      const errorMessage =
        formData.id === 0
          ? "Failed to create party role"
          : "Failed to update party role";
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
      console.log(`Deleted party role with id: ${currentId}`);
      navigate("/v1/partyrole");
    } catch (err: any) {
      setError("Failed to delete party role");
      console.error("Failed to delete party role:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Party Role Detail รายละเอียดบทบาทของปาร์ตี้" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Party Role Detail รายละเอียดบทบาทของปาร์ตี้" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Party Role Detail รายละเอียดบทบาทของปาร์ตี้ id: ${currentId}`
            : "Create Party Role สร้างบทบาทของปาร์ตี้"
        }
      />
      <form onSubmit={handleSubmit}>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "repeat(2, 1fr)",
              md: "repeat(2, 1fr)",
            },
            gap: 2,
            mt: 2,
            px: 2,
          }}
        >
          <TextField
            select
            label="Party"
            name="party_id"
            value={formData.party_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {parties.map((option) => (
              <MenuItem key={option.party_id} value={option.party_id}>
                {option.type === "organization"
                  ? `${option.party_id} (organization) ${option.name_en || ''} ${option.name_th || ''}`
                  : `${option.party_id} (person) ${option.personal_id_number || ''}`}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            select
            label="Role Type"
            name="role_type_id"
            value={formData.role_type_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            {roleTypes.map((option) => (
              <MenuItem key={option.id} value={option.id}>
                {option.description}
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
            required
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
            <CancelButton onClick={() => navigate("/v1/partyrole")} />
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
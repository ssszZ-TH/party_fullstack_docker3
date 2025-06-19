import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { create as createCorporation } from "../../services/corporation";
import { create as createGovernmentAgency } from "../../services/governmentAgency";
import { create as createFamily } from "../../services/family";
import { create as createOtherInformalOrganization } from "../../services/other_informal_organization";
import { create as createTeam } from "../../services/team";
import {
  Box,
  Typography,
  Alert,
  TextField,
  MenuItem,
} from "@mui/material";
import SaveButton from "../../components/buttons/SaveButton";
import CancelButton from "../../components/buttons/CancelButton";

interface Organization {
  name_en: string;
  name_th: string;
  federal_tax_id_number?: string;
}

const organizationTypes = [
  { key: "corporation", name: "Corporation", service: createCorporation },
  { key: "governmentagency", name: "Government Agency", service: createGovernmentAgency },
  { key: "family", name: "Family", service: createFamily },
  { key: "otherinformalorganization", name: "Other Informal Organization", service: createOtherInformalOrganization },
  { key: "team", name: "Team", service: createTeam },
];

export default function OrganizationCreate() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<Organization>({
    name_en: "",
    name_th: "",
    federal_tax_id_number: "",
  });
  const [selectedType, setSelectedType] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleTypeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const type = e.target.value;
    setSelectedType(type);
    if (["family", "otherinformalorganization", "team"].includes(type)) {
      setFormData((prev) => ({ ...prev, federal_tax_id_number: "" }));
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedType) {
      setError("Please select an organization type");
      return;
    }
    setLoading(true);
    try {
      const selectedService = organizationTypes.find((type) => type.key === selectedType)?.service;
      if (!selectedService) throw new Error("Invalid organization type");
      const payload = {
        name_en: formData.name_en,
        name_th: formData.name_th,
        federal_tax_id_number: ["family", "otherinformalorganization", "team"].includes(selectedType)
          ? undefined
          : formData.federal_tax_id_number || undefined,
      };
      await selectedService(payload);
      navigate("/v1/organization");
    } catch (err: any) {
      setError("Failed to create organization");
      console.error("Failed to create organization:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Create Organization สร้างองค์กร" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom title="Create Organization สร้างองค์กร" />
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
            label="Organization Type"
            value={selectedType}
            onChange={handleTypeChange}
            fullWidth
            required
          >
            <MenuItem value="">Select Type</MenuItem>
            {organizationTypes.map((type) => (
              <MenuItem key={type.key} value={type.key}>
                {type.name}
              </MenuItem>
            ))}
          </TextField>
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
            disabled={["family", "otherinformalorganization", "team"].includes(selectedType)}
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
            <CancelButton onClick={() => navigate("/v1/organization")} />
          </Box>
          <Box sx={{ display: "flex", gap: 2 }}>
            <SaveButton onClick={handleSubmit} />
          </Box>
        </Box>
      </form>
    </Box>
  );
}
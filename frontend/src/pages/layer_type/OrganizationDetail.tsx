import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
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

// กำหนดประเภท organization ทั้งหมด
const organizationTypes = [
  { key: "corporation", name: "Corporation" },
  { key: "family", name: "Family" },
  { key: "governmentAgency", name: "Government Agency" },
  { key: "other_informal_organization", name: "Other Informal Org" },
  { key: "team", name: "Team" },
];

// Service mapping
const getService = async (orgType: string) => {
  switch (orgType) {
    case "corporation":
      return await import("../../services/corporation");
    case "family":
      return await import("../../services/family");
    case "governmentAgency":
      return await import("../../services/governmentAgency");
    case "other_informal_organization":
      return await import("../../services/other_informal_organization");
    case "team":
      return await import("../../services/team");
    default:
      throw new Error(`Unknown organization type: ${orgType}`);
  }
};

interface Organization {
  id: number;
  name_en: string;
  name_th: string;
  federal_tax_id_number: string;
  organization_type: string;
}

export default function OrganizationDetail() {
  const { param } = useParams<{ param: string }>();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [organization, setOrganization] = useState<Organization | null>(null);
  const [formData, setFormData] = useState<Organization | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (param) {
      if (param === "create") {
        console.log("Create new organization");
        setCurrentId(null);
        setFormData({
          id: 0,
          name_en: "",
          name_th: "",
          federal_tax_id_number: "",
          organization_type: "",
        });
        setLoading(false);
      } else {
        const parsedId = parseInt(param, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchOrganization(parsedId);
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [param]);

  const fetchOrganization = async (id: number) => {
    setLoading(true);
    try {
      // ต้องรู้ organization_type ก่อนจึงจะเรียก service ได้
      if (!formData?.organization_type) {
        // ในกรณีนี้เรายังไม่รู้ organization_type ต้องให้ผู้ใช้เลือกก่อน
        setFormData({
          id,
          name_en: "",
          name_th: "",
          federal_tax_id_number: "",
          organization_type: "",
        });
        setLoading(false);
        return;
      }

      const serviceModule = await getService(formData.organization_type);
      const response = await serviceModule.get({ id });
      setOrganization(response);
      setFormData(response);
      setError(null);
    } catch (err: any) {
      setError("Failed to fetch organization details");
      console.error("Error fetching organization:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => 
      prev ? { ...prev, [name]: value } : null
    );
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData || !formData.organization_type) return;
    
    setLoading(true);
    try {
      const serviceModule = await getService(formData.organization_type);
      const payload = {
        id: currentId || 0,
        name_en: formData.name_en,
        name_th: formData.name_th,
        federal_tax_id_number: formData.federal_tax_id_number,
      };

      if (currentId) {
        console.log("Updated organization with payload:", payload);
        await serviceModule.update(payload);
      } else {
        console.log("Created organization with payload:", payload);
        await serviceModule.create(payload);
      }
      navigate(-1); // กลับไปหน้าก่อนหน้า
    } catch (err: any) {
      const errorMessage = currentId 
        ? "Failed to update organization" 
        : "Failed to create organization";
      setError(errorMessage);
      console.error(`${errorMessage}:`, err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!currentId || !formData?.organization_type) return;
    setLoading(true);
    try {
      const serviceModule = await getService(formData.organization_type);
      await serviceModule.deleteById({ id: currentId });
      console.log(`Deleted organization with id: ${currentId}`);
      navigate(-1); // กลับไปหน้าก่อนหน้า
    } catch (err: any) {
      setError("Failed to delete organization");
      console.error("Failed to delete organization:", err);
    } finally {
      setLoading(false);
    }
  };

  // เมื่อเลือก organization type แล้ว และอยู่ในโหมด update
  useEffect(() => {
    if (currentId && formData?.organization_type) {
      fetchOrganization(currentId);
    }
  }, [formData?.organization_type]);

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Organization Detail" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Organization Detail" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Organization Detail ID: ${currentId}`
            : "Create Organization"
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
          {/* Dropdown สำหรับเลือกประเภทองค์กร */}
          <TextField
            select
            label="Organization Type"
            name="organization_type"
            value={formData.organization_type || ""}
            onChange={handleChange}
            fullWidth
            required
            disabled={!!currentId && !!organization} // ปิดการแก้ไขถ้าเป็นโหมด update และโหลดข้อมูลแล้ว
          >
            {organizationTypes.map((type) => (
              <MenuItem key={type.key} value={type.key}>
                {type.name}
              </MenuItem>
            ))}
          </TextField>

          <TextField
            label="English Name"
            name="name_en"
            value={formData.name_en || ""}
            onChange={handleChange}
            fullWidth
            required
          />

          <TextField
            label="Thai Name"
            name="name_th"
            value={formData.name_th || ""}
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
            <CancelButton onClick={() => navigate(-1)} />
            {currentId && (
              <DeleteButton 
                onClick={handleDelete} 
                disabled={!formData.organization_type}
              />
            )}
          </Box>
          <Box sx={{ display: "flex", gap: 2 }}>
            <SaveButton 
              onClick={handleSubmit} 
              disabled={!formData.organization_type}
            />
          </Box>
        </Box>
      </form>
    </Box>
  );
}
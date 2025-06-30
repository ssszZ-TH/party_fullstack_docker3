import React, { useState, useEffect } from "react";
import { useParams, useNavigate, useSearchParams } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import Loading from "../../components/Loading";
import { get, update, create, deleteById } from "../../services/classifybysize";
import { list as listEmployeeCountRange } from "../../services/employeecountrange";
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

interface Size {
  id: number;
  fromdate?: string;
  thrudate?: string;
  party_id?: number;
  employee_count_range_id?: number;
}

export default function SizeDetail() {
  const { paramId } = useParams<{ paramId: string }>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [currentId, setCurrentId] = useState<number | null>(null);
  const [formData, setFormData] = useState<Size | null>(null);
  const [employeeCountRanges, setEmployeeCountRanges] = useState<
    { id: number; description: string }[]
  >([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const organizationId = searchParams.get("organization_id");

  useEffect(() => {
    const fetchDropdowns = async () => {
      try {
        const employeeCountRangeData = await listEmployeeCountRange();
        setEmployeeCountRanges(employeeCountRangeData);
      } catch (error) {
        setError("Failed to load dropdown options");
      }
    };

    if (paramId) {
      if (paramId === "new") {
        if (!organizationId) {
          setError("Organization ID is required");
          setLoading(false);
          return;
        }
        setCurrentId(null);
        setFormData({
          id: 0,
          fromdate: "",
          thrudate: "",
          party_id: Number(organizationId),
          employee_count_range_id: undefined,
        });
        fetchDropdowns();
        setLoading(false);
      } else {
        const parsedId = parseInt(paramId, 10);
        if (!isNaN(parsedId) && parsedId > 0) {
          setCurrentId(parsedId);
          fetchSize(parsedId);
          fetchDropdowns();
        } else {
          setError("Invalid ID format");
          setLoading(false);
        }
      }
    }
  }, [paramId, organizationId]);

  const fetchSize = async (id: number) => {
    setLoading(true);
    try {
      const response = await get({ id });
      setFormData(response);
      setError(null);
    } catch (err) {
      setError("Failed to fetch size details");
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
      setError("Organization ID is required");
      return;
    }
    if (!formData.employee_count_range_id) {
      setError("Employee Count Range is required");
      return;
    }
    setLoading(true);
    try {
      const payload = {
        id: currentId || 0,
        fromdate: formData.fromdate || undefined,
        thrudate: formData.thrudate || undefined,
        party_id: Number(formData.party_id),
        employee_count_range_id: Number(formData.employee_count_range_id),
      };
      if (payload.id === 0) {
        await create(payload);
      } else {
        await update(payload);
      }
      navigate(`/v1/sizebyorganizationid/${formData.party_id}`);
    } catch (err) {
      setError(currentId ? "Failed to update size" : "Failed to create size");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!currentId || !formData?.party_id) return;
    setLoading(true);
    try {
      await deleteById({ id: currentId });
      navigate(`/v1/sizebyorganizationid/${formData.party_id}`);
    } catch (err) {
      setError("Failed to delete size");
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Size Detail รายละเอียดขนาดองค์กร" />
        <Alert severity="error">{error}</Alert>
      </Box>
    );
  if (!formData)
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Size Detail รายละเอียดขนาดองค์กร" />
        <Typography>No data available</Typography>
      </Box>
    );

  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom
        title={
          currentId
            ? `Size Detail รายละเอียดขนาดองค์กร id: ${currentId}`
            : "Create Size สร้างขนาดองค์กร"
        }
      />
      <form onSubmit={handleSubmit}>
        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: {
              xs: "1fr",
              sm: "repeatουργ,2, 1fr)",
              md: "repeat(3, 1fr)",
            },
            gap: 2,
            mt: 2,
            px: 2,
          }}
        >
          <TextField
            select
            label="Employee Count Range"
            name="employee_count_range_id"
            value={formData.employee_count_range_id || ""}
            onChange={handleChange}
            fullWidth
            required
          >
            <MenuItem value="">Select Employee Count Range</MenuItem>
            {employeeCountRanges.map((option) => (
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
            <CancelButton
              onClick={() => navigate(`/v1/sizebyorganizationid/${formData.party_id}`)}
            />
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
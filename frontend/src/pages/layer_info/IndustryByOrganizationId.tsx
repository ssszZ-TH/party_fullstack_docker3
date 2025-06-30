import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { listByOrganizationId } from "../../services/classifybyindustry";
import UpdateButton from "../../components/buttons/UpdateButton";
import AddButton from "../../components/buttons/AddButton";
import { Box } from "@mui/material";
import BusinessIcon from "@mui/icons-material/Business";

export default function IndustryByOrganizationId() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    if (!paramId) return;
    setLoading(true);
    try {
      const res = await listByOrganizationId({
        organization_id: Number(paramId),
      });
      setRows(res);
    } catch (error) {
      console.error("Failed to fetch industry data:", error);
      setRows([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [paramId]);

  const handleUpdate = (id: number) => {
    navigate(`/v1/industrydetail/${id}`);
  };

  const handleAdd = () => {
    navigate(`/v1/industrydetail/new?organization_id=${paramId}`);
  };

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    {
      field: "description",
      headerName: "Industry",
      width: 300,
    },
    { field: "naics_code", headerName: "NAICS Code", width: 150 },
    { field: "fromdate", headerName: "From Date", width: 150 },
    { field: "thrudate", headerName: "Thru Date", width: 150 },
    {
      field: "actions",
      headerName: "Actions",
      width: 100,
      sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: "flex", gap: 1 }}>
          <UpdateButton onClick={() => handleUpdate(params.row.id)} />
        </Box>
      ),
    },
  ];

  return (
    <>
      <AppBarCustom title={`Industry for Organization ID: ${paramId}`} />
      {loading ? (
        <Loading />
      ) : (
        <DataTable columns={columns} rows={rows} getRowId={(row) => row.id} />
      )}
      <AddButton onClick={handleAdd} />
    </>
  );
}

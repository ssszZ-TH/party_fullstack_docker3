import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { listByCitizenshipId, deleteById } from "../../services/passport";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";
import { Box } from "@mui/material";

export default function PassportByCitizenshipId() {
  const { paramId } = useParams<{ paramId: string }>();
  const navigate = useNavigate();

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    if (!paramId) return;
    setLoading(true);
    try {
      const res = await listByCitizenshipId({ citizenship_id: Number(paramId) });
      setRows(res);
    } catch (error) {
      console.error("Failed to fetch passport data:", error);
      setRows([]); // Clear rows on error
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [paramId]);

  const handleUpdate = (id: number) => {
    // นำทางไปยังหน้า detail ของ passport เพื่อแก้ไข
    navigate(`/v1/passport/${id}`);
  };
  
  const handleAdd = () => {
    // นำทางไปยังหน้า detail เพื่อสร้าง passport ใหม่, ส่ง citizenship_id ไปด้วย
    navigate(`/v1/passport/new?citizenship_id=${paramId}`);
  };



  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 90 },
    { field: "passportnumber", headerName: "Passport Number", width: 200 },
    { field: "fromdate", headerName: "From Date", width: 150 },
    { field: "thrudate", headerName: "Thru Date", width: 150 },
    {
      field: "actions",
      headerName: "Actions",
      width: 100,
      sortable: false,
      renderCell: (params) => (
        <Box sx={{ display: 'flex', gap: 1 }}>
          <UpdateButton onClick={() => handleUpdate(params.row.id)} />
        </Box>
      ),
    },
  ];

  return (
    <>
      <AppBarCustom title={`Passports for Citizenship ID: ${paramId}`} />
      <Box sx={{ p: 2 }}>
        <AddButton onClick={handleAdd} />
        {loading ? (
          <Loading />
        ) : (
          <Box sx={{ mt: 2 }}>
            <DataTable
              columns={columns}
              rows={rows}
              getRowId={(row) => row.id}
            />
          </Box>
        )}
      </Box>
    </>
  );
}
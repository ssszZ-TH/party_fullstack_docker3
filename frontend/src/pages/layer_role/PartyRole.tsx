import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { list } from "../../services/partyrole";
import UpdateButton from "../../components/buttons/UpdateButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

export default function PartyRole() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const columns: GridColDef[] = [
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton onClick={() => navigate(`/v1/partyrole/${params.row.id}`)} />
      ),
    },
    { field: "id", headerName: "Role ID", width: 70 },
    { field: "party_id", headerName: "Party ID", width: 100 },
    { field: "role_type_description", headerName: "Role Type", width: 150 },
    { field: "fromdate", headerName: "From Date (YYYY-MM-DD)", width: 150 },
    { field: "thrudate", headerName: "Thru Date (YYYY-MM-DD)", width: 150 },
    { field: "type", headerName: "Type", width: 100 },
    { field: "name_en", headerName: "Name (EN)", width: 150 },
    { field: "name_th", headerName: "Name (TH)", width: 150 },
    { field: "personal_id_number", headerName: "Personal ID Number", width: 150 },
    { field: "comment", headerName: "Comment", width: 200 },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPartyRoles = async () => {
    setLoading(true);
    try {
      const res = await list();
      console.log("Fetched party role data:", res);
      setRows(res);
      setError(null);
    } catch (err: any) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const handleError = (err: any) => {
    if (
      err.message === "No access token found" ||
      err.response?.status === 401
    ) {
      setError("กรุณาเข้าสู่ระบบหรือ token หมดอายุ");
      logout();
      navigate("/login");
    } else {
      setError(err.message || "ไม่สามารถโหลดข้อมูลได้");
    }
  };

  useEffect(() => {
    fetchPartyRoles();
  }, []);

  return (
    <>
      <AppBarCustom title="Party Role บทบาทของปาร์ตี้ (party = organization or person)" />
      {loading ? (
        <Loading />
      ) : error ? (
        <Alert severity="error" sx={{ m: 2 }}>
          {error}
        </Alert>
      ) : (
        <DataTable columns={columns} rows={rows} getRowId={(row) => row.id} />
      )}
      <AddButton
        onClick={() => {
          navigate("/v1/partyrole/new");
        }}
      />
    </>
  );
}
import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { list } from "../../services/partyrelationship";
import UpdateButton from "../../components/buttons/UpdateButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

export default function PartyRelationship() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const columns: GridColDef[] = [
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton onClick={() => navigate(`/v1/partyrelationship/${params.row.id}`)} />
      ),
    },
    { field: "id", headerName: "ID", width: 70 },
    { field: "from_party_role_id", headerName: "From Party Role ID", width: 150 },
    { field: "to_party_role_id", headerName: "To Party Role ID", width: 150 },
    { field: "party_relationship_type_description", headerName: "Relationship Type", width: 150 },
    { field: "priority_type_description", headerName: "Priority", width: 120 },
    { field: "party_relationship_status_type_description", headerName: "Status", width: 120 },
    { field: "from_date", headerName: "From Date (YYYY-MM-DD)", width: 150 },
    { field: "thru_date", headerName: "Thru Date (YYYY-MM-DD)", width: 150 },
    { field: "comment", headerName: "Comment", width: 200 },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPartyRelationships = async () => {
    setLoading(true);
    try {
      const res = await list();
      console.log("Fetched party relationship data:", res);
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
    fetchPartyRelationships();
  }, []);

  return (
    <>
      <AppBarCustom title="Party Role Relationship ความสัมพันธ์ของบทบาทปาร์ตี้" />
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
          navigate("/v1/partyrelationship/new");
        }}
      />
    </>
  );
}
import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { list } from "../../services/communicationevent";
import UpdateButton from "../../components/buttons/UpdateButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

export default function CommunicationEvent() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const columns: GridColDef[] = [
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton onClick={() => navigate(`/v1/communicationevent/${params.row.id}`)} />
      ),
    },
    { field: "id", headerName: "ID", width: 70 },
    { field: "datetime_start", headerName: "Start DateTime", width: 180 },
    { field: "datetime_end", headerName: "End DateTime", width: 180 },
    { field: "note", headerName: "Note", width: 200 },
    { field: "contact_mechanism_type_description", headerName: "Contact Mechanism", width: 150 },
    { field: "communication_event_status_type_description", headerName: "Status", width: 120 },
    { field: "party_relationship_id", headerName: "Party Relationship ID", width: 150 },
    { field: "party_relationship_comment", headerName: "Relationship Comment", width: 200 },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCommunicationEvents = async () => {
    setLoading(true);
    try {
      const res = await list();
      console.log("Fetched communication event data:", res);
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
    fetchCommunicationEvents();
  }, []);

  return (
    <>
      <AppBarCustom title="Communication Event เหตุการณ์การสื่อสาร" />
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
          navigate("/v1/communicationevent/new");
        }}
      />
    </>
  );
}
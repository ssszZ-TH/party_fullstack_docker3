import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { list } from "../../services/communicationeventpurpose";
import UpdateButton from "../../components/buttons/UpdateButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

export default function CommunicationEventPurpose() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const columns: GridColDef[] = [
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton onClick={() => navigate(`/v1/communicationeventpurpose/${params.row.id}`)} />
      ),
    },
    { field: "id", headerName: "ID", width: 70 },
    { field: "communication_event_id", headerName: "Communication Event ID", width: 150 },
    { field: "communication_event_purpose_type_description", headerName: "Purpose Type", width: 150 },
    { field: "communication_event_note", headerName: "Event Note", width: 200 },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCommunicationEventPurposes = async () => {
    setLoading(true);
    try {
      const res = await list();
      console.log("Fetched communication event purpose data:", res);
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
    fetchCommunicationEventPurposes();
  }, []);

  return (
    <>
      <AppBarCustom title="Communication Event Purpose วัตถุประสงค์เหตุการณ์การสื่อสาร" />
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
          navigate("/v1/communicationeventpurpose/new");
        }}
      />
    </>
  );
}
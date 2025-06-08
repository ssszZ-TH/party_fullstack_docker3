import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { list } from "../../services/person";
import UpdateButton from "../../components/buttons/UpdateButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

export default function Person() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);


const columns: GridColDef[] = [
  {
    field: "update",
    headerName: "",
    width: 100,
    renderCell: (params) => (
      <UpdateButton onClick={() => navigate(`/v1/person/${params.row.id}`)} />
    ),
  },
  { field: "id", headerName: "ID", width: 70 },
  { field: "personal_id_number", headerName: "Personal ID Number", width: 150 },
  { field: "fname", headerName: "First Name", width: 120 },
  { field: "mname", headerName: "Middle Name", width: 120 },
  { field: "lname", headerName: "Last Name", width: 120 },
  { field: "nickname", headerName: "Nickname", width: 120 },
  { field: "gender_description", headerName: "Gender", width: 120 },
  { field: "citizenship_id", headerName: "Citizenship ID", width: 120 },
  { field: "country_name_en", headerName: "Current Citizenship", width: 150 },
  { field: "totalyearworkexperience", headerName: "Work Experience (Years)", width: 150 },
  { field: "birthdate", headerName: "Birth Date", width: 120 },
  { field: "mothermaidenname", headerName: "Mother's Maiden Name", width: 150 },
  { field: "height_val", headerName: "Height (cm)", width: 100 },
  { field: "weight_val", headerName: "Weight (kg)", width: 100 },
  { field: "marital_status_type_description", headerName: "Marital Status", width: 150 },
  { field: "comment", headerName: "Comment", width: 200 },
  
];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  

  interface PersonRow {
    id: number | null;
    personal_id_number: string;
    birthdate: string;
    mothermaidenname: string;
    totalyearworkexperience: number;
    comment: string;
    gender_type_id?: number;
  }

  

  const fetchPerson = async () => {
    setLoading(true);
    try {
      const res = await list();
      console.log("Fetched person data:", res);
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
    fetchPerson();
  }, []);

    

  return (
    <>
      <AppBarCustom title="Person ข้อมูลบุคคล" />
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
          navigate("/v1/person/new");
        }}
      />
    </>
  );
}

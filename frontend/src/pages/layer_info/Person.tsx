import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import PersonModal from "../../components/modal/PersonModal";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { create, get, list, update, deleteById } from "../../services/person";
import { list as listGenderTypes } from "../../services/gendertype";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

export default function Person() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const [genderTypes, setGenderTypes] = useState<{ id: number; description: string }[]>([]);

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "socialsecuritynumber", headerName: "Social Security Number", width: 150 },
    { field: "birthdate", headerName: "Birth Date", width: 120 },
    { field: "mothermaidenname", headerName: "Mother's Maiden Name", width: 150 },
    { field: "totalyearworkexperience", headerName: "Work Experience (Years)", width: 150, type: 'number' },
    {
      field: "gender_type_id",
      headerName: "Gender",
      width: 120,
      renderCell: (params) => {
        const gender = genderTypes.find(g => g.id === params.row.gender_type_id);
        return gender ? gender.description : 'None';
      }
    },
    { field: "comment", headerName: "Comment", width: 200 },
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton
          onClick={() => handleUpdateButton(params.row)}
        />
      ),
    },
    {
      field: "delete",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <DeleteButton
          onClick={() => handleDeleteButton(params.row.id)}
        />
      ),
    },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const [initialDetail, setInitialDetail] = useState({
    id: null,
    socialsecuritynumber: "",
    birthdate: "",
    mothermaidenname: "",
    totalyearworkexperience: 0,
    comment: "",
    gender_type_id: undefined,
  });
  const [openModalFor, setOpenModalFor] = useState("");

  interface PersonRow {
    id: number | null;
    socialsecuritynumber: string;
    birthdate: string;
    mothermaidenname: string;
    totalyearworkexperience: number;
    comment: string;
    gender_type_id?: number;
  }

  const handleUpdateButton = async (row: PersonRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail(row);
    openModal("update");
  };

  const handleDeleteButton = async (id: number) => {
    console.log("delete button receive value = ", id);
    setLoading(true);
    try {
      await deleteById({ id });
      await fetchPerson();
    } catch (err: any) {
      handleError(err);
    }
  };

  const fetchPerson = async () => {
    setLoading(true);
    try {
      const res = await list();
      // console.log("Fetched person data:", res);
      setRows(res);
      setError(null);
    } catch (err: any) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchGenderTypes = async () => {
    try {
      const data = await listGenderTypes();
      setGenderTypes(data);
    } catch (error) {
      console.error("Failed to fetch gender types:", error);
      setError("ไม่สามารถโหลดข้อมูลประเภทเพศได้");
    }
  };

  const handleError = (err: any) => {
    if (err.message === 'No access token found' || err.response?.status === 401) {
      setError('กรุณาเข้าสู่ระบบหรือ token หมดอายุ');
      logout();
      navigate('/login');
    } else {
      setError(err.message || 'ไม่สามารถโหลดข้อมูลได้');
    }
  };

  useEffect(() => {
    fetchPerson();
    fetchGenderTypes();
  }, []);

  const openModal = (reason?: string) => {
    setOpenModalFor(reason || "");
    setOpen(true);
  };

  const closeModal = () => {
    setOpen(false);
    setInitialDetail({
      id: null,
      socialsecuritynumber: "",
      birthdate: "",
      mothermaidenname: "",
      totalyearworkexperience: 0,
      comment: "",
      gender_type_id: undefined,
    });
    setOpenModalFor("");
  };

  interface Payload {
    id: number | null;
    socialsecuritynumber: string;
    birthdate: string;
    mothermaidenname: string;
    totalyearworkexperience: number;
    comment: string;
    gender_type_id: number;
  }

  const handleSubmit = async (payload: Payload) => {
    setLoading(true);
    try {
      if (payload.id) {
        await update(payload);
        console.log("Updated with payload:", payload);
      } else {
        await create(payload);
        console.log("Created with payload:", payload);
      }
      await fetchPerson();
      closeModal();
    } catch (err: any) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

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
        <DataTable
          columns={columns}
          rows={rows}
          getRowId={(row) => row.id}
        />
      )}
      <AddButton
        onClick={() => {
          openModal("create");
        }}
      />
      <PersonModal
        open={open}
        onClose={closeModal}
        initialDetail={initialDetail}
        onSubmit={handleSubmit}
        openModalFor={openModalFor}
        genderTypes={genderTypes}
      />
    </>
  );
}
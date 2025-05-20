import { useState, useEffect, useContext } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import PersonNameModal from "../../components/Modal/PersonNameModal";
import Loading from "../../components/Loading";
import { AuthContext } from "../../contexts/AuthContext";
import { create, get, list, update, deleteById } from "../../services/personname";
import { list as listPerson } from "../../services/person";
import { list as listPersonNameType } from "../../services/personnametype";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";
import { Alert } from "@mui/material";

interface DropdownItem {
  id: number;
  text: string;
}

export default function PersonName() {
  const navigate = useNavigate();
  const { logout } = useContext(AuthContext);

  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "fromdate", headerName: "From Date", width: 120 },
    { field: "thrudate", headerName: "Thru Date", width: 120 },
    { field: "person_id", headerName: "Person ID", width: 100 },
    {
      field: "person", // Column name in the table
      headerName: "Person Details", // Title shown at the top of the column
      width: 200, // How wide the column is (in pixels)
      renderCell: (params) => {
        // Function to show custom content in the cell
        const obj = personDD.find((item) => item.id === params.row.person_id); // Find person data by matching person_id
        return <>{obj ? obj.text : "N/A"}</>;
      },
    },
    { field: "personnametype_id", headerName: "Name Type ID", width: 120 },
    {
      field: "nametype", // Column name in the table
      headerName: "Name Type", // Title shown at the top of the column
      width: 200, // How wide the column is (in pixels)
      renderCell: (params) => {
        // Function to show custom content in the cell
        const obj = personNameTypeDD.find(
          (item) => item.id === params.row.personnametype_id
        ); // Find person name type data by matching personnametype_id
        return <>{obj ? obj.text : "N/A"}</>;
      },
    },
    { field: "name", headerName: "Name", width: 150 },
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton onClick={() => handleUpdateButton(params.row)} />
      ),
    },
    {
      field: "delete",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <DeleteButton onClick={() => handleDeleteButton(params.row.id)} />
      ),
    },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [open, setOpen] = useState(false);
  const [personDD, setPersonDD] = useState<DropdownItem[]>([]);
  const [personNameTypeDD, setPersonNameTypeDD] = useState<DropdownItem[]>([]);
  const [initialDetail, setInitialDetail] = useState({
    id: null,
    fromdate: "",
    thrudate: null,
    person_id: 0,
    personnametype_id: 0,
    name: "",
  });
  const [openModalFor, setOpenModalFor] = useState("");

  interface PersonNameRow {
    id: number;
    fromdate: string;
    thrudate: string | null;
    person_id: number;
    personnametype_id: number;
    name: string;
  }

  const handleUpdateButton = async (row: PersonNameRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail(row);
    openModal("update");
  };

  const handleDeleteButton = async (id: number) => {
    console.log("delete button receive value = ", id);
    setLoading(true);
    try {
      await deleteById({ id });
      await fetchPersonName();
    } catch (err: any) {
      handleError(err);
    }
  };

  const fetchPersonName = async () => {
    setLoading(true);
    try {
      const res = await list();
      setRows(res);
      setError(null);
    } catch (err: any) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchDropdownData = async () => {
    try {
      const personRes = await listPerson();
      const personNameTypeRes = await listPersonNameType();
      setPersonDD(
        personRes.map((item) => ({
          id: item.id,
          text: item.socialsecuritynumber + " " + item.comment,
        }))
      );
      setPersonNameTypeDD(
        personNameTypeRes.map((t: any) => ({
          id: t.id,
          text: t.description || `Type ${t.id}`,
        }))
      );
    } catch (err: any) {
      handleError(err);
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
    fetchPersonName();
    fetchDropdownData();
  }, []);

  const openModal = (reason?: string) => {
    setOpenModalFor(reason || "");
    setOpen(true);
  };

  const closeModal = () => {
    setOpen(false);
    setInitialDetail({
      id: null,
      fromdate: "",
      thrudate: null,
      person_id: 0,
      personnametype_id: 0,
      name: "",
    });
    setOpenModalFor("");
  };

  interface Payload {
    id: number | null;
    fromdate: string;
    thrudate: string | null;
    person_id: number;
    personnametype_id: number;
    name: string;
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
      await fetchPersonName();
      closeModal();
    } catch (err: any) {
      handleError(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <AppBarCustom title="Person Name ข้อมูลชื่อบุคคล" />
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
          openModal("create");
        }}
      />
      <PersonNameModal
        open={open}
        onClose={closeModal}
        initialDetail={initialDetail}
        onSubmit={handleSubmit}
        openModalFor={openModalFor}
        personDD={personDD}
        personNameTypeDD={personNameTypeDD}
      />
    </>
  );
}

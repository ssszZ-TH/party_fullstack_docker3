import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal from "../../components/Modal/Modal_id_des";
import Loading from "../../components/Loading";
import { create, get, list, update, deleteById } from "../../services/communicationeventpurposetype";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

export default function CommunicationEventPurposeType() {
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 },
    { field: "description", headerName: "Description", width: 300 },
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
  const [open, setOpen] = useState(false);
  const [initialDetail, setInitialDetail] = useState({
    id: null,
    description: "",
  });
  const [openModalFor, setOpenModalFor] = useState("");

  interface typeofTableRow {
    id: number;
    description: string;
  }

  const handleUpdateButton = async (row: typeofTableRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail(row);
    openModal("update");
  };

  const handleDeleteButton = async (id: number) => {
    console.log("delete button receive value = ", id);
    setLoading(true);
    await deleteById({ id });
    await fetchDataTable();
    setLoading(false);
  };

  const fetchDataTable = async () => {
    setLoading(true);
    const res = await list();
    setRows(res);
    setLoading(false);
  };

  useEffect(() => {
    fetchDataTable();
  }, []);

  const openModal = (reason?: string) => {
    setOpenModalFor(reason || "");
    setOpen(true);
  };

  const closeModal = () => {
    setOpen(false);
    setInitialDetail({
      id: null,
      description: "",
    });
    setOpenModalFor("");
  };

  interface typeofPayload {
    id: number | null;
    description: string;
  }

  const handleSubmit = async (payload: typeofPayload) => {
    setLoading(true);
    try {
      if (payload.id) {
        await update({
          id: payload.id,
          description: payload.description,
        });
        console.log("Updated with payload:", payload);
      } else {
        await create({
          description: payload.description,
        });
        console.log("Created with payload:", payload);
      }
    } catch (error) {
      console.error("while submit catch error = ", error);
    } finally {
      await fetchDataTable();
      closeModal();
      setLoading(false);
    }
  };

  return (
    <>
      <AppBarCustom title="Communication Event Purpose Type ประเภทวัตถุประสงค์การสื่อสาร" />
      {loading ? (
        <Loading />
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
      <Modal
        open={open}
        onClose={closeModal}
        initialDetail={initialDetail}
        onSubmit={handleSubmit}
        openModalFor={openModalFor}
      />
    </>
  );
}
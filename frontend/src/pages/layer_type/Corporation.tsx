import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal from "../../components/modal/CorporationModal";
import Loading from "../../components/Loading";
import { create, get, list, update, deleteById } from "../../services/corporation";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

export default function Corporation() {
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 },
    { field: "name_en", headerName: "English Name", width: 200 },
    { field: "name_th", headerName: "Thai Name", width: 200 },
    { field: "federal_tax_id_number", headerName: "Federal Tax ID", width: 150 },
    // {
    //   field: "update",
    //   headerName: "",
    //   width: 100,
    //   renderCell: (params) => (
    //     <UpdateButton onClick={() => handleUpdateButton(params.row)} />
    //   ),
    // },
    // {
    //   field: "delete",
    //   headerName: "",
    //   width: 100,
    //   renderCell: (params) => (
    //     <DeleteButton onClick={() => handleDeleteButton(params.row.id)} />
    //   ),
    // },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false);
  const [initialDetail, setInitialDetail] = useState({
    id: null,
    name_en: "",
    name_th: "",
    federal_tax_id_number: "",
  });
  const [openModalFor, setOpenModalFor] = useState("");

  interface typeofTableRow {
    id: number;
    name_en: string;
    name_th: string;
    federal_tax_id_number?: string;
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
      name_en: "",
      name_th: "",
      federal_tax_id_number: "",
    });
    setOpenModalFor("");
  };

  interface typeofPayload {
    id: number | null;
    name_en: string;
    name_th: string;
    federal_tax_id_number?: string;
  }

  const handleSubmit = async (payload: typeofPayload) => {
    setLoading(true);
    try {
      if (payload.id) {
        await update({
          id: payload.id,
          name_en: payload.name_en,
          name_th: payload.name_th,
          federal_tax_id_number: payload.federal_tax_id_number,
        });
        console.log("Updated with payload:", payload);
      } else {
        await create({
          name_en: payload.name_en,
          name_th: payload.name_th,
          federal_tax_id_number: payload.federal_tax_id_number,
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
      <AppBarCustom title="Corporation บริษัท" />
      {loading ? (
        <Loading />
      ) : (
        <DataTable
          columns={columns}
          rows={rows}
          getRowId={(row) => row.id}
        />
      )}
      {/* <AddButton
        onClick={() => {
          openModal("create");
        }}
      /> */}
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
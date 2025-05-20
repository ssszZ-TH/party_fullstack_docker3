import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal from "../../components/Modal/Modal_iso_name_enth"; // เเก้ modal ด้วย
import { Button } from "@mui/material";
import Loading from "../../components/Loading";
import {
  create,
  get,
  list,
  update,
  deleteById,
} from "../../services/country"; // เเก้ service ด้วย
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

export default function Country() {
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 },
    {
      field: "isocode",
      headerName: "ISO Code",
      width: 300,
    },
    {
      field: "name_en",
      headerName: "Name",
      width: 300,
    },
    {
      field: "name_th",
      headerName: "ชื่อ",
      width: 300,
    },
    {
      field: "update", // คอลัมน์ใหม่สำหรับปุ่ม Update
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton
          
          onClick={() => handleUpdateButton(params.row)} // เรียกใช้ฟังก์ชัน handleEdit เมื่อคลิก
        />
      ),
    },
    {
      field: "delete", // คอลัมน์ใหม่สำหรับปุ่ม Update
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <DeleteButton
          
          onClick={() => handleDeleteButton(params.row.id)} // เรียกใช้ฟังก์ชัน handleEdit เมื่อคลิก
        />
        
      ),
    },
  ];

  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true); // สถานะการโหลด
  const [open, setOpen] = useState(false);
  const [initialDetail, setInitialDetail] = useState<typeofTableRow>({
    id: null,
    isocode: "",
    name_en: "",
    name_th: "",
  });

  // เหตุผลในการเปิด modal มีเปิดเพื่อ อ่าน เปิด แก้ไข เปิดเพื่อสร้างข้อมูลใหม่
  const [openModalFor, setOpenModalFor] = useState("");

  interface typeofTableRow {
    id: number | null;
    isocode: string;
    name_en: string;
    name_th: string;
  }

  const handleUpdateButton = async (row: typeofTableRow) => {
    console.log("edit button receive value = ", row);

    // ตั้งค่า initialDetail ด้วยข้อมูลที่ถูกต้อง
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

  // modal ทำเพื่อให้เข้าใจง่ายยิ่งขึ้น
  const openModal = (reson?: string) => {
    setOpenModalFor(reson || "");
    setOpen(true);
  };
  const closeModal = () => {
    // ปิด modal
    setOpen(false);
    // ล้างค่า modal
    setInitialDetail({
      id: null,
      isocode: "",
      name_en: "",
      name_th: "",
    });
    setOpenModalFor("");
  };

  const handleSubmit = async (payload: typeofTableRow) => {
    // เเสดง loading
    setLoading(true);
    try {
      if (payload.id) {
        // in case update
        await update({
          id: payload.id,
          isocode: payload.isocode,
          name_en: payload.name_en,
          name_th: payload.name_th,
        });
        console.log("Updated with payload:", payload);
        // setLoading(false);
      } else {
        // in case create
        await create({
          isocode: payload.isocode,
          name_en: payload.name_en,
          name_th: payload.name_th,
        });
        console.log("Created with payload:", payload);
        // setLoading(false);
      }
    } catch (error) {
      // จับ error print ให้ดู
      console.error("while submit catch error = ", error);
    } finally {
      //sync ค่าในตาราง กับ database
      fetchDataTable();
      closeModal(); // ปิด modal
      setLoading(false);
    }
  };
  return (
    <>
      <AppBarCustom title="country ประเทศ" />
      {loading ? (
        <Loading /> // แสดง loading component ถ้ากำลังโหลด
      ) : (
        <DataTable
          columns={columns}
          rows={rows}
          getRowId={(row) => row.id} // ใช้ geo_id เป็น id
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

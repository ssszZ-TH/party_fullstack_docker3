// ไฟล์นี้เป็นหน้า GenderType สำหรับแสดงตารางข้อมูลประเภทเพศ
// รองรับการแสดงข้อมูล (read), สร้าง (create), อัพเดท (update), และลบ (delete)
// ใช้ DataTable จาก MUI สำหรับแสดงข้อมูล และ Modal สำหรับฟอร์ม
import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal from "../../components/Modal/Modal_id_des"; // Modal สำหรับจัดการฟอร์ม id และ description
import Loading from "../../components/Loading";
import { create, get, list, update, deleteById } from "../../services/gendertype"; // Service สำหรับ API gendertype
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

// Component หลักสำหรับหน้า GenderType
export default function GenderType() {
  // กำหนดคอลัมน์สำหรับ DataTable
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 }, // คอลัมน์แสดงรหัส
    {
      field: "description",
      headerName: "Description",
      width: 300, // คอลัมน์คำอธิบายประเภทเพศ
    },
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        // ปุ่ม Update เรียก handleUpdateButton
        <UpdateButton onClick={() => handleUpdateButton(params.row)} />
      ),
    },
    {
      field: "delete",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        // ปุ่ม Delete เรียก handleDeleteButton
        <DeleteButton onClick={() => handleDeleteButton(params.row.id)} />
      ),
    },
  ];

  // State สำหรับเก็บข้อมูลตาราง
  const [rows, setRows] = useState([]);
  // State สำหรับควบคุมสถานะการโหลด
  const [loading, setLoading] = useState(true);
  // State สำหรับควบคุมการเปิด/ปิด Modal
  const [open, setOpen] = useState(false);
  // State สำหรับเก็บข้อมูลเริ่มต้นของฟอร์มใน Modal
  const [initialDetail, setInitialDetail] = useState({
    id: null,
    description: "",
  });

  // State สำหรับเก็บโหมดของ Modal (create, update, read)
  const [openModalFor, setOpenModalFor] = useState("");

  // อินเทอร์เฟซสำหรับแถวในตารางและฟอร์ม
  interface typeofTableRow {
    id: number;
    description: string;
  }

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Update
  const handleUpdateButton = async (row: typeofTableRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail(row); // ตั้งค่า initialDetail
    openModal("update"); // เปิด Modal ในโหมด update
  };

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Delete
  const handleDeleteButton = async (id: number) => {
    console.log("delete button receive value = ", id);
    setLoading(true);
    await deleteById({ id }); // เรียก API ลบข้อมูล
    await fetchDataTable(); // รีเฟรชตาราง
    setLoading(false);
  };

  // ฟังก์ชันดึงข้อมูลตารางจาก API
  const fetchDataTable = async () => {
    setLoading(true);
    const res = await list(); // เรียก API `/v1/gendertype`
    setRows(res); // อัพเดทข้อมูลตาราง
    setLoading(false);
  };

  // useEffect สำหรับโหลดข้อมูลเมื่อ component เริ่มทำงาน
  useEffect(() => {
    fetchDataTable();
  }, []);

  // ฟังก์ชันเปิด Modal
  const openModal = (reason?: string) => {
    setOpenModalFor(reason || ""); // ตั้งค่าโหมด (create, update, read)
    setOpen(true); // เปิด Modal
  };

  // ฟังก์ชันปิด Modal
  const closeModal = () => {
    setOpen(false); // ปิด Modal
    // รีเซ็ต initialDetail เพื่อเคลียร์ฟอร์ม
    setInitialDetail({
      id: null,
      description: "",
    });
    setOpenModalFor("");
  };

  // อินเทอร์เฟซสำหรับ payload ที่ส่งไปยัง API
  interface typeofPayload {
    id: number | null;
    description: string;
  }

  // ฟังก์ชันจัดการการ submit ฟอร์มจาก Modal
  const handleSubmit = async (payload: typeofPayload) => {
    setLoading(true);
    try {
      if (payload.id) {
        // โหมด Update
        await update({
          id: payload.id,
          description: payload.description,
        });
        console.log("Updated with payload:", payload);
      } else {
        // โหมด Create
        await create({
          description: payload.description,
        });
        console.log("Created with payload:", payload);
      }
    } catch (error) {
      console.error("while submit catch error = ", error); // Log error เพื่อ debug
    } finally {
      await fetchDataTable(); // รีเฟรชตาราง
      closeModal(); // ปิด Modal
      setLoading(false);
    }
  };

  // JSX สำหรับ UI ของหน้า
  return (
    <>
      <AppBarCustom title="Gender Type ประเภทเพศ" /> {/* แถบด้านบน */}
      {loading ? (
        <Loading /> // แสดง Loading component ถ้ากำลังโหลด
      ) : (
        <DataTable
          columns={columns}
          rows={rows}
          getRowId={(row) => row.id} // ใช้ id เป็น key
        />
      )}
      <AddButton
        onClick={() => {
          openModal("create"); // เปิด Modal ในโหมด create
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
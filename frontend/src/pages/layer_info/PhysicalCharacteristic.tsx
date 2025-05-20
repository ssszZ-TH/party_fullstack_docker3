// ไฟล์นี้เป็นหน้า PhysicalCharacteristic สำหรับแสดงตารางข้อมูลลักษณะทางกายภาพ
// รองรับการแสดงข้อมูล (read), สร้าง (create), อัพเดท (update), และลบ (delete)
// ใช้ DataTable จาก MUI สำหรับแสดงข้อมูล และ Modal สำหรับฟอร์ม
import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal_physicalcharacteristic from "../../components/Modal/Modal_physicalcharacteristic"; // Modal สำหรับจัดการฟอร์ม
import { Button, Typography } from "@mui/material";
import Loading from "../../components/Loading";
import {
  create,
  get,
  list,
  update,
  deleteById,
} from "../../services/physicalcharacteristic"; // Service สำหรับ API physicalcharacteristic
import { list as listPhysicalCharacteristicType } from "../../services/physicalcharacteristictype"; // Service สำหรับ dropdown PhysicalCharacteristicType
import { list as listPerson } from "../../services/person"; // Service สำหรับ dropdown Person
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

// Component หลักสำหรับหน้า PhysicalCharacteristic
export default function PhysicalCharacteristic() {
  // กำหนดคอลัมน์สำหรับ DataTable
  // แต่ละคอลัมน์กำหนด field, headerName, และการ render เฉพาะ
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 }, // คอลัมน์แสดงรหัส
    {
      field: "fromdate",
      headerName: "From Date YYYY-MM-DD",
      width: 150, // คอลัมน์วันที่เริ่มต้น
    },
    {
      field: "thrudate",
      headerName: "Thru Date YYYY-MM-DD",
      width: 150, // คอลัมน์วันที่สิ้นสุด
    },
    {
      field: "person_id",
      headerName: "Person ID",
      width: 80, // คอลัมน์รหัสบุคคล
    },
    {
      field: "person",
      headerName: "Person Details",
      width: 200,
      renderCell: (params) => {
        // แสดงชื่อบุคคลจาก personDD โดยค้นหาด้วย person_id
        const obj = personDD.find((item) => item.id === params.row.person_id);
        return <>{obj ? obj.text : "N/A"}</>;
      },
    },
    {
      field: "physicalcharacteristictype_id",
      headerName: "Physical Characteristic Type ID",
      width: 100, // คอลัมน์รหัสประเภทลักษณะ
    },
    {
      field: "physicalcharacteristictype",
      headerName: "Physical Characteristic Type",
      width: 300,
      renderCell: (params) => {
        // แสดงชื่อประเภทลักษณะจาก physicalcharacteristictypeDD
        const item = physicalcharacteristictypeDD.find(
          (c) => c.id === params.row.physicalcharacteristictype_id
        );
        return <>{item ? item.text : "N/A"}</>;
      },
    },
    {
      field: "val",
      headerName: "Value",
      width: 100, // คอลัมน์ค่าลักษณะทางกายภาพ (เช่น ความสูง, น้ำหนัก)
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
  const [initialDetail, setInitialDetail] = useState<typeofTableRow>({
    id: null,
    fromdate: "",
    thrudate: "",
    val: 0,
    person_id: "", // ใช้ "" เพื่อป้องกัน MUI Select warning
    physicalcharacteristictype_id: "", // ใช้ "" เพื่อป้องกัน warning
  });

  // อินเทอร์เฟซสำหรับข้อมูลใน dropdown
  interface typeOfDD {
    id: number;
    text: string;
  }

  // ค่าเริ่มต้นสำหรับ dropdown ถ้า API ยังไม่โหลด
  const defaultPersonDD = [
    {
      id: 0,
      text: "",
    },
  ];
  const defaultPhysicalCharacteristicTypeDD = [
    {
      id: 0,
      text: "",
    },
  ];

  // State สำหรับเก็บข้อมูล dropdown
  const [personDD, setPersonDD] = useState<typeOfDD[]>(defaultPersonDD);
  const [physicalcharacteristictypeDD, setPhysicalCharacteristicTypeDD] = useState<typeOfDD[]>(
    defaultPhysicalCharacteristicTypeDD
  );

  // State สำหรับเก็บโหมดของ Modal (create, update, read)
  const [openModalFor, setOpenModalFor] = useState("");

  // อินเทอร์เฟซสำหรับแถวในตารางและฟอร์ม
  interface typeofTableRow {
    id: number | null;
    fromdate: string;
    thrudate: string;
    val: number;
    person_id: number | "";
    physicalcharacteristictype_id: number | "";
  }

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Update
  const handleUpdateButton = async (row: typeofTableRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail(row); // ตั้งค่า initialDetail ด้วยข้อมูลแถว
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
    const res = await list(); // เรียก API `/v1/physicalcharacteristic`
    setRows(res); // อัพเดทข้อมูลตาราง
    setLoading(false);
  };

  // อินเทอร์เฟซสำหรับข้อมูล Person จาก API
  interface TypeOfPerson {
    id: number;
    socialsecuritynumber: string;
    birthdate: string;
    mothermaidenname: string | null;
    totalyearworkexperience: number;
    comment: string;
  }

  // อินเทอร์เฟซสำหรับข้อมูล PhysicalCharacteristicType จาก API
  interface TypeOfPhysicalCharacteristicType {
    id: number;
    description: string;
  }

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ Person
  const fetchPersonDD = async () => {
    const res: Array<TypeOfPerson> = await listPerson();
    const DD = res.map((item) => ({
      id: item.id,
      text: `${item.socialsecuritynumber} ${item.comment || "N/A"}`, // รวม socialsecuritynumber และ comment
    }));
    setPersonDD(DD);
  };

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ PhysicalCharacteristicType
  const fetchPhysicalCharacteristicTypeDD = async () => {
    const res: Array<TypeOfPhysicalCharacteristicType> = await listPhysicalCharacteristicType();
    const DD = res.map((item) => ({
      id: item.id,
      text: item.description || "N/A",
    }));
    setPhysicalCharacteristicTypeDD(DD);
  };

  // useEffect สำหรับโหลดข้อมูลเมื่อ component เริ่มทำงาน
  useEffect(() => {
    fetchPersonDD(); // โหลด dropdown Person
    fetchPhysicalCharacteristicTypeDD(); // โหลด dropdown PhysicalCharacteristicType
    fetchDataTable(); // โหลดข้อมูลตาราง
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
      fromdate: "",
      thrudate: "",
      val: 0,
      person_id: "",
      physicalcharacteristictype_id: "",
    });
    setOpenModalFor("");
  };

  // ฟังก์ชันจัดการการ submit ฟอร์มจาก Modal
  const handleSubmit = async (payload: typeofTableRow) => {
    setLoading(true);
    try {
      if (payload.id) {
        // โหมด Update
        await update({
          id: payload.id,
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          val: payload.val,
          person_id: payload.person_id,
          physicalcharacteristictype_id: payload.physicalcharacteristictype_id,
        });
        console.log("Updated with payload:", payload);
      } else {
        // โหมด Create
        await create({
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          val: payload.val,
          person_id: payload.person_id,
          physicalcharacteristictype_id: payload.physicalcharacteristictype_id,
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
      <AppBarCustom title="Physical Characteristic ลักษณะทางกายภาพ" /> {/* แถบด้านบน */}
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
      <Modal_physicalcharacteristic
        open={open}
        onClose={closeModal}
        initialDetail={initialDetail}
        onSubmit={handleSubmit}
        openModalFor={openModalFor}
        personDD={personDD}
        physicalcharacteristictypeDD={physicalcharacteristictypeDD}
      />
    </>
  );
}
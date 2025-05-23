// ไฟล์นี้เป็นหน้า ClassifyByIndustry สำหรับแสดงตารางข้อมูลการจำแนกตามประเภทอุตสาหกรรม
// รองรับการแสดงข้อมูล (read), สร้าง (create), อัพเดท (update), และลบ (delete)
// ใช้ DataTable จาก MUI สำหรับแสดงข้อมูล และ Modal สำหรับฟอร์ม
import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal_classifybyindustry from "../../components/Modal/Modal_ClassifyByIndustry"; // Modal สำหรับจัดการฟอร์ม
import Loading from "../../components/Loading";
import {
  create,
  get,
  list,
  update,
  deleteById,
} from "../../services/classifybyindustry"; // Service สำหรับ API classifybyindustry
import { list as listPartyType } from "../../services/partytype"; // Service สำหรับ dropdown PartyType
import { list as listInformalOrganization } from "../../services/informalorganization"; // Service สำหรับ dropdown InformalOrganization
import { list as listLegalOrganization } from "../../services/legalorganization"; // Service สำหรับ dropdown LegalOrganization
import { list as listIndustryType } from "../../services/industrytype"; // Service สำหรับ dropdown IndustryType
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

// Component หลักสำหรับหน้า ClassifyByIndustry
export default function ClassifyByIndustry() {
  // กำหนดคอลัมน์สำหรับ DataTable
  // รวม naics_code และ description จากตาราง industrytype เพื่อแสดงผล
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
      field: "party_id",
      headerName: "Party ID",
      width: 100, // คอลัมน์รหัส Party (จาก InformalOrganization หรือ LegalOrganization)
    },
    {
      field: "party",
      headerName: "Organization Details",
      width: 300,
      renderCell: (params) => {
        // แสดงข้อมูล Organization จาก organizationDD โดยค้นหาด้วย party_id
        const obj = organizationDD.find((item) => item.id === params.row.party_id);
        return (
          <>
            {obj
              ? `${obj.text} (${obj.type === "informal" ? "inform" : "legal"})`
              : "N/A"}
          </>
        );
      },
    },
    {
      field: "party_type_id",
      headerName: "Party Type ID",
      width: 100, // คอลัมน์รหัสประเภท Party
    },
    {
      field: "party_type",
      headerName: "Party Type",
      width: 200,
      renderCell: (params) => {
        // แสดงข้อมูล PartyType จาก partyTypeDD
        const item = partyTypeDD.find((c) => c.id === params.row.party_type_id);
        return <>{item ? item.text : "N/A"}</>;
      },
    },
    {
      field: "industry_type_id",
      headerName: "Industry Type ID",
      width: 100, // คอลัมน์รหัสประเภทอุตสาหกรรม
    },
    {
      field: "naics_code",
      headerName: "NAICS Code",
      width: 150, // คอลัมน์รหัส NAICS (จาก industrytype)
    },
    {
      field: "description",
      headerName: "Industry Description",
      width: 200, // คอลัมน์คำอธิบายประเภทอุตสาหกรรม (จาก industrytype)
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
    party_id: "",
    party_type_id: "",
    industry_type_id: "",
  });

  // อินเทอร์เฟซสำหรับข้อมูลใน dropdown
  interface typeOfDD {
    id: number;
    text: string;
    type: "informal" | "legal"; // ระบุประเภทองค์กร
  }

  // ค่าเริ่มต้นสำหรับ dropdown ถ้า API ยังไม่โหลด
  const defaultOrganizationDD = [{ id: 0, text: "", type: "informal" }];
  const defaultPartyTypeDD = [{ id: 0, text: "" }];
  const defaultIndustryTypeDD = [{ id: 0, text: "" }];

  // State สำหรับเก็บข้อมูล dropdown
  const [organizationDD, setOrganizationDD] = useState<typeOfDD[]>(defaultOrganizationDD);
  const [partyTypeDD, setPartyTypeDD] = useState<typeOfDD[]>(defaultPartyTypeDD);
  const [industryTypeDD, setIndustryTypeDD] = useState<typeOfDD[]>(defaultIndustryTypeDD);

  // State สำหรับเก็บโหมดของ Modal (create, update, read)
  const [openModalFor, setOpenModalFor] = useState("");

  // อินเทอร์เฟซสำหรับแถวในตารางและฟอร์ม
  // ไม่รวม naics_code, description เพราะใช้ในตารางเท่านั้น
  interface typeofTableRow {
    id: number | null;
    fromdate: string;
    thrudate: string;
    party_id: number | "";
    party_type_id: number | "";
    industry_type_id: number | "";
    naics_code?: string; // Optional สำหรับแสดงในตาราง
    description?: string; // Optional สำหรับแสดงในตาราง
  }

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Update
  const handleUpdateButton = async (row: typeofTableRow) => {
    console.log("edit button receive value = ", row);
    setInitialDetail({
      id: row.id,
      fromdate: row.fromdate,
      thrudate: row.thrudate,
      party_id: row.party_id,
      party_type_id: row.party_type_id,
      industry_type_id: row.industry_type_id,
    }); // ตั้งค่า initialDetail (ไม่รวม naics_code, description)
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
    const res = await list(); // เรียก API `/v1/classifybyindustry`
    setRows(res); // อัพเดทข้อมูลตาราง
    setLoading(false);
  };

  // อินเทอร์เฟซสำหรับข้อมูล InformalOrganization จาก API
  interface TypeOfInformalOrganization {
    id: number; // อ้างอิง party_id
    name_en: string;
    name_th: string;
  }

  // อินเทอร์เฟซสำหรับข้อมูล LegalOrganization จาก API
  interface TypeOfLegalOrganization {
    id: number; // อ้างอิง party_id
    name_en: string;
    name_th: string;
    federal_tax_id_number: string;
  }

  // อินเทอร์เฟซสำหรับข้อมูล PartyType จาก API
  interface TypeOfPartyType {
    id: number;
    description: string;
  }

  // อินเทอร์เฟซสำหรับข้อมูล IndustryType จาก API
  interface TypeOfIndustryType {
    id: number;
    naics_code: string;
    description: string;
  }

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ Organization
  // รวม InformalOrganization และ LegalOrganization โดย party_id อ้างอิง id
  const fetchOrganizationDD = async () => {
    const informalRes: Array<TypeOfInformalOrganization> = await listInformalOrganization();
    const legalRes: Array<TypeOfLegalOrganization> = await listLegalOrganization();
    
    const informalDD = informalRes.map((item) => ({
      id: item.id,
      text: `${item.name_en} (${item.name_th})`,
      type: "informal" as const,
    }));
    
    const legalDD = legalRes.map((item) => ({
      id: item.id,
      text: `${item.name_en} (${item.name_th})`,
      type: "legal" as const,
    }));
    
    setOrganizationDD([...informalDD, ...legalDD]);
  };

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ PartyType
  const fetchPartyTypeDD = async () => {
    const res: Array<TypeOfPartyType> = await listPartyType();
    const DD = res.map((item) => ({
      id: item.id,
      text: item.description || "N/A",
    }));
    setPartyTypeDD(DD);
  };

  // ฟังก์ชันดึงข้อมูล dropdown สำหรับ IndustryType
  const fetchIndustryTypeDD = async () => {
    const res: Array<TypeOfIndustryType> = await listIndustryType();
    const DD = res.map((item) => ({
      id: item.id,
      text: `${item.naics_code} (${item.description})` || "N/A",
    }));
    setIndustryTypeDD(DD);
  };

  // useEffect สำหรับโหลดข้อมูลเมื่อ component เริ่มทำงาน
  useEffect(() => {
    fetchOrganizationDD(); // โหลด dropdown Organization
    fetchPartyTypeDD(); // โหลด dropdown PartyType
    fetchIndustryTypeDD(); // โหลด dropdown IndustryType
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
      party_id: "",
      party_type_id: "",
      industry_type_id: "",
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
          party_id: payload.party_id,
          party_type_id: payload.party_type_id,
          industry_type_id: payload.industry_type_id,
        });
        console.log("Updated with payload:", payload);
      } else {
        // โหมด Create
        await create({
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          party_id: payload.party_id,
          party_type_id: payload.party_type_id,
          industry_type_id: payload.industry_type_id,
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
      <AppBarCustom title="Classify By Industry การจำแนกตามประเภทอุตสาหกรรม" /> {/* แถบด้านบน */}
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
      <Modal_classifybyindustry
        open={open}
        onClose={closeModal}
        initialDetail={initialDetail}
        onSubmit={handleSubmit}
        openModalFor={openModalFor}
        organizationDD={organizationDD}
        partyTypeDD={partyTypeDD}
        industryTypeDD={industryTypeDD}
      />
    </>
  );
}
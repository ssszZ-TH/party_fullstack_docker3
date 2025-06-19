// OrganizationPage.tsx - Generic page for all organization types
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Loading from "../../components/Loading";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

// กำหนด service สำหรับ organization ต่างๆ
import * as corporationService from "../../services/corporation";
import * as familyService from "../../services/family";
import * as governmentAgencyService from "../../services/governmentAgency";
import * as otherInformalOrgService from "../../services/other_informal_organization";
import * as teamService from "../../services/team";

// กำหนดประเภท organization ทั้งหมด
const organizationTypes = [
  { key: "corporation", name: "Corporation", service: corporationService },
  { key: "family", name: "Family", service: familyService },
  {
    key: "governmentagency",
    name: "Government Agency",
    service: governmentAgencyService,
  },
  {
    key: "otherinformalorganization",
    name: "Other Informal Org",
    service: otherInformalOrgService,
  },
  { key: "team", name: "Team", service: teamService },
];

// Component หลักสำหรับหน้า Organization
export default function OrganizationPage() {
  const navigate = useNavigate();

  // กำหนดคอลัมน์สำหรับ DataTable
  const columns: GridColDef[] = [
    {
      field: "update",
      headerName: "",
      width: 100,
      renderCell: (params) => (
        <UpdateButton
          onClick={() =>
            handleUpdateButton(params.row.organization_type, params.row.id)
          }
        />
      ),
    },
    { field: "id", headerName: "ID", width: 50 },
    {
      field: "name_en",
      headerName: "Name",
      width: 200,
    },
    {
      field: "name_th",
      headerName: "Thai Name",
      width: 200,
    },
    {
      field: "organization_type",
      headerName: "Organization Type",
      width: 200,
    },
    {
      field: "federal_tax_id_number",
      headerName: "Federal Tax ID Number",
      width: 200,
    },
    
  ];

  // State สำหรับเก็บข้อมูลตาราง
  const [rows, setRows] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  // ดึงข้อมูลจาก service ทั้งหมด
  const fetchDataTable = async () => {
    setLoading(true);
    try {
      // ดึงข้อมูลจากทุก service พร้อมกัน
      const allData = await Promise.all(
        organizationTypes.map(async (orgType) => {
          const data = await orgType.service.list();
          // เพิ่ม organization_type ในข้อมูลแต่ละรายการ
          return data.map((item: any) => ({
            ...item,
            organization_type: orgType.key,
          }));
        })
      );

      // รวมข้อมูลทั้งหมดเป็น array เดียว
      const combinedData = allData.flat();
    //   console.log("Combined Data:", combinedData);
      setRows(combinedData);
    } catch (error) {
      console.error("Error loading data:", error);
    } finally {
      setLoading(false);
    }
  };

  // useEffect สำหรับโหลดข้อมูลเมื่อ component เริ่มทำงาน
  useEffect(() => {
    fetchDataTable();
  }, []);

  // ฟังก์ชันจัดการเมื่อกดปุ่ม Update
  const handleUpdateButton = (orgType: string, id: number) => {
    navigate(`/v1/${orgType}/${id}`); // Redirect ไปหน้า detail
  };


  // JSX สำหรับ UI ของหน้า
  return (
    <>
      <AppBarCustom title="Organizations Management" />

      {loading ? (
        <Loading />
      ) : (
        <>

          <DataTable
            columns={columns}
            rows={rows}
            getRowId={(row) => `${row.organization_type}-${row.id}`}
          />
          <AddButton onClick={() => navigate("/organization/create")} />
        </>
      )}
    </>
  );
}

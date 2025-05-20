import { useState, useEffect } from "react";
import AppBarCustom from "../../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../../components/DataTable";
import Modal from "../../components/Modal/Modal_passport"; // เเก้ modal ด้วย
import { Button, Typography } from "@mui/material";
import Loading from "../../components/Loading";
import { create, get, list, update, deleteById } from "../../services/passport"; // เเก้ service ด้วย

import { list as listCitizenship } from "../../services/citizenship";
import UpdateButton from "../../components/buttons/UpdateButton";
import DeleteButton from "../../components/buttons/DeleteButton";
import AddButton from "../../components/buttons/AddButton";

export default function Passport() {
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 },
    {
      field: "fromdate",
      headerName: "From Date YYYY-MM-DD",
      width: 150,
    },
    {
      field: "thrudate",
      headerName: "Thru Date YYYY-MM-DD",
      width: 150,
    },
    {
      field: "passportnumber",
      headerName: "Passport Number",
      width: 150,
    },
    {
      field: "citizenship_id",
      headerName: "Citizenship ID",
      width: 150,
    },
    {
      field: "citizenship",
      headerName: "Citizenship",
      width: 500,
      renderCell: (params) => {
        const obj = citizenshipDD.find(
          (item) => item.id === params.row.citizenship_id
        );
        return <>{obj ? obj.text : "N/A"}</>;
      },
    },
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
  const [loading, setLoading] = useState(true); // สถานะการโหลด
  const [open, setOpen] = useState(false);
  const [initialDetail, setInitialDetail] = useState<typeofTableRow>({
    id: null,
    fromdate: "",
    thrudate: "",
    passportnumber: "",
    citizenship_id: 0,
  });

  interface typeOfDD {
    id: number;
    text: string;
  }

  const defaultcitizenshipDD = [
    {
      id: 0,
      text: "",
    },
  ];

  const [citizenshipDD, setCitizenshipDD] =
    useState<typeOfDD[]>(defaultcitizenshipDD);

  // เหตุผลในการเปิด modal มีเปิดเพื่อ อ่าน เปิด แก้ไข เปิดเพื่อสร้างข้อมูลใหม่
  const [openModalFor, setOpenModalFor] = useState("");

  interface typeofTableRow {
    id: number | null;
    fromdate: string;
    thrudate: string;
    passportnumber: string;
    citizenship_id: number;
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

  interface TypeOfCitizenship {
    id: number;
    fromdate: string;
    thrudate: string;
    person_id: string;
    country_id: string;
  }

  const fetchCitizenshipDD = async () => {
    const res: Array<TypeOfCitizenship> = await listCitizenship();
    const DD = res.map((item) => ({
      id: item.id,
      text: `ID:${item.id} person:${item.person_id} live in country:${item.country_id} from ${item.fromdate} to ${item.thrudate}`,
    }));
    setCitizenshipDD(DD);
  };

  useEffect(() => {
    fetchCitizenshipDD();
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
      fromdate: "",
      thrudate: "",
      passportnumber: "",
      citizenship_id: 0,
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
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          passportnumber: payload.passportnumber,
          citizenship_id: payload.citizenship_id,
        });
        console.log("Updated with payload:", payload);
        // setLoading(false);
      } else {
        // in case create
        await create({
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          passportnumber: payload.passportnumber,
          citizenship_id: payload.citizenship_id,
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
      <AppBarCustom title="Passport หนังสือเดินทาง" />
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
        citizenshipDD={citizenshipDD}
      />
    </>
  );
}

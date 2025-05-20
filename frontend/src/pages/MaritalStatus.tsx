import { useState, useEffect } from "react";
import AppBarCustom from "../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../components/DataTable";
import Modal from "../components/Modal_maritalstatus"; // เเก้ modal ด้วย
import { Button, Typography } from "@mui/material";
import Loading from "../components/Loading";
import {
  create,
  get,
  list,
  update,
  deleteById,
} from "../services/maritalstatus"; // เเก้ service ด้วย

import { list as listMaritalStatusType } from "../services/maritalstatustype";
import { list as listPerson } from "../services/person";
import UpdateButton from "../components/buttons/UpdateButton";
import DeleteButton from "../components/buttons/DeleteButton";
import AddButton from "../components/buttons/AddButton";

export default function MaritalStatus() {
  const columns: GridColDef[] = [
    { field: "id", headerName: "ID", width: 50 },
    {
      field: "fromdate",
      headerName: "From Date YYYY-MM-DD",
      width: 200,
    },
    {
      field: "thrudate",
      headerName: "Thru Date YYYY-MM-DD",
      width: 200,
    },
    {
      field: "person_id",
      headerName: "Person ID",
      width: 100,
    },
    {
      field: "person", // Column name in the table
      headerName: "Person Details", // Title shown at the top of the column
      width: 300, // How wide the column is (in pixels)
      renderCell: (params) => {
        // Function to show custom content in the cell
        const obj = personDD.find((item) => item.id === params.row.person_id); // Find person data by matching person_id
        return <>{obj ? obj.text : "N/A"}</>;
      },
    },
    {
      field: "maritalstatustype_id",
      headerName: "Maritalstatus Type ID",
      width: 100,
    },
    {
      field: "maritalstatustype", // Column name in the table
      headerName: "Maritalstatus",
      width: 300,
      renderCell: (params) => {
        const item = maritalstatustypeDD.find(
          (c) => c.id === params.row.maritalstatustype_id
        );
        return <>{item ? item.text : "N/A"}</>;
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
    person_id: 0,
    maritalstatustype_id: 0,
  });

  interface typeOfDD {
    id: number;
    text: string;
  }

  const defaultPersonDD = [
    {
      id: 0,
      text: "",
    },
  ];

  const defaultmaritalstatustypsDD = [
    {
      id: 0,
      text: "",
    },
  ];

  const [personDD, setPersonDD] = useState<typeOfDD[]>(defaultPersonDD);
  const [maritalstatustypeDD, setMaritalstatustypeDD] = useState<typeOfDD[]>(
    defaultmaritalstatustypsDD
  );

  // เหตุผลในการเปิด modal มีเปิดเพื่อ อ่าน เปิด แก้ไข เปิดเพื่อสร้างข้อมูลใหม่
  const [openModalFor, setOpenModalFor] = useState("");

  interface typeofTableRow {
    id: number | null;
    fromdate: string;
    thrudate: string;
    person_id: number;
    maritalstatustype_id: number;
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

  interface TypeOfPerson {
    id: number;
    socialsecuritynumber: string;
    birthdate: string; // เก็บเป็น string เพราะรูปแบบ "YYYY-MM-DD" เป็น string
    mothermaidenname: string | null; // รองรับ null ได้
    totalyearworkexperience: number;
    comment: string;
  }

  interface TypeOfMaritalstatustype {
    id: number;
    description: string;
  }

  const fetchpersonDD = async () => {
    const res: Array<TypeOfPerson> = await listPerson();
    const DD = res.map((item) => ({ id: item.id, text: item.socialsecuritynumber+' '+item.comment }));
    setPersonDD(DD);
  };

  const fetchMaritalstatustypeDD = async () => {
    const res: Array<TypeOfMaritalstatustype> = await listMaritalStatusType();
    const DD = res.map((item) => ({
      id: item.id,
      text: item.description || "N/A",
    }));
    setMaritalstatustypeDD(DD);
  };

  useEffect(() => {
    fetchpersonDD();
    fetchMaritalstatustypeDD();
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
      person_id: 0,
      maritalstatustype_id: 0,
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
          person_id: payload.person_id,
          maritalstatustype_id: payload.maritalstatustype_id,
        });
        console.log("Updated with payload:", payload);
        // setLoading(false);
      } else {
        // in case create
        await create({
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          person_id: payload.person_id,
          maritalstatustype_id: payload.maritalstatustype_id,
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
      <AppBarCustom title="maritalstatus สถานะภาพสมรส" />
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
        personDD={personDD}
        maritalstatustypeDD={maritalstatustypeDD}
      />
    </>
  );
}

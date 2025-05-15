import { useState, useEffect } from "react";
import AppBarCustom from "../components/AppBarCustom";
import { GridColDef } from "@mui/x-data-grid";
import DataTable from "../components/DataTable";
import Modal from "../components/Modal_citizenship"; // เเก้ modal ด้วย
import { Button, Typography } from "@mui/material";
import Loading from "../components/Loading";
import { create, get, list, update, deleteById } from "../services/citizenship"; // เเก้ service ด้วย

import { list as listCountry } from "../services/country";
import { list as listPerson } from "../services/person";
import UpdateButton from "../components/buttons/UpdateButton";
import DeleteButton from "../components/buttons/DeleteButton";
import AddButton from "../components/buttons/AddButton";

export default function Citizenship() {
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
      headerName: "Person Comment", // Title shown at the top of the column
      width: 300, // How wide the column is (in pixels)
      renderCell: (params) => {
        // Function to show custom content in the cell
        const obj = personDD.find((item) => item.id === params.row.person_id); // Find person data by matching person_id
        return (
          <Typography
            variant="body2" // Small text style
            color={obj ? "text.primary" : "text.secondary"} // Black if found, gray if not
          >
            {obj ? obj.text : "N/A"}
          </Typography>
        );
      },
    },
    {
      field: "country_id",
      headerName: "Country ID",
      width: 100,
    },
    {
      field: "country",
      headerName: "Country",
      width: 300,
      renderCell: (params) => {
        const country = countryDD.find((c) => c.id === params.row.country_id);
        return (
          <Typography
            variant="body2"
            color={country ? "text.primary" : "text.secondary"}
          >
            {country ? country.text : "N/A"}
          </Typography>
        );
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
    country_id: 0,
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

  const defaultCountryDD = [
    {
      id: 0,
      text: "",
    },
  ];

  const [personDD, setPersonDD] = useState<typeOfDD[]>(defaultPersonDD);
  const [countryDD, setCountryDD] = useState<typeOfDD[]>(defaultCountryDD);

  // เหตุผลในการเปิด modal มีเปิดเพื่อ อ่าน เปิด แก้ไข เปิดเพื่อสร้างข้อมูลใหม่
  const [openModalFor, setOpenModalFor] = useState("");

  interface typeofTableRow {
    id: number | null;
    fromdate: string;
    thrudate: string;
    person_id: number;
    country_id: number;
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

  interface TypeOfCountry {
    id: number;
    isocode: string;
    name_en: string;
    name_th: string;
  }

  const fetchpersonDD = async () => {
    const res: Array<TypeOfPerson> = await listPerson();
    const DD = res.map((item) => ({ id: item.id, text: item.comment }));
    setPersonDD(DD);
  };

  const fetchCountryDD = async () => {
    const res: Array<TypeOfCountry> = await listCountry();
    const DD = res.map((item) => ({
      id: item.id,
      text: item.name_en + " - " + item.name_th,
    }));
    setCountryDD(DD);
  };

  useEffect(() => {
    fetchpersonDD();
    fetchCountryDD();
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
      country_id: 0,
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
          country_id: payload.country_id,
        });
        console.log("Updated with payload:", payload);
        // setLoading(false);
      } else {
        // in case create
        await create({
          fromdate: payload.fromdate,
          thrudate: payload.thrudate,
          person_id: payload.person_id,
          country_id: payload.country_id,
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
      <AppBarCustom title="Citizenship สัญชาติ" />
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
        countryDD={countryDD}
      />
    </>
  );
}

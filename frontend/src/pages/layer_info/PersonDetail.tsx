// ไฟล์นี้เป็นหน้า PersonDetail สำหรับแสดงรายละเอียดบุคคลตาม id ที่รับจาก URL
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import AppBarCustom from '../../components/AppBarCustom';
import Loading from '../../components/Loading';

import { Box, Typography, Paper } from '@mui/material';



// Component หลักสำหรับหน้า PersonDetail
export default function PersonDetail() {
  // ดึง id จาก URL
  const { paramId } = useParams<{ paramId: string }>();
  
  // State สำหรับจัดการ current_id
  const [currentId, setCurrentId] = useState<number | null>(null);

  // State สำหรับจัดการสถานะการโหลด
  const [loading, setLoading] = useState(true);
  
  // State สำหรับจัดการ error
  const [error, setError] = useState<string | null>(null);

  // useEffect สำหรับตั้งค่า current_id และดึงข้อมูลเมื่อ id เปลี่ยน
  useEffect(() => {
    console.log("PersonDetail: paramId = ", paramId);
    if (paramId) {
      setCurrentId(Number(paramId));
      setLoading(false);
    }
  }, [paramId]);



  // แสดง Loading ถ้ากำลังโหลด
  if (loading) {
    return <Loading />;
  }

  // แสดง Error ถ้ามี
  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <AppBarCustom title="Person Detail รายละเอียดบุคคล" />
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  // แสดงข้อมูลบุคคล
  return (
    <Box sx={{ p: 0 }}>
      <AppBarCustom title="Person Detail รายละเอียดบุคคล" />
      <Paper sx={{ p: 2, mt: 2 }}>
        <Typography variant="h6">Person ID: {currentId}</Typography>
        
      </Paper>
    </Box>
  );
}
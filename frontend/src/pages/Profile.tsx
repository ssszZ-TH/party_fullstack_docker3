import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Box,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { AuthContext } from '../contexts/AuthContext';
import { getProfile } from '../services/profile';
import EmailIcon from '@mui/icons-material/Email';
import PersonIcon from '@mui/icons-material/Person';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';

// อินเทอร์เฟซสำหรับข้อมูลผู้ใช้ที่ได้จาก API
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

// สไตล์สำหรับ Paper component เพื่อให้ดูสะอาดและ responsive
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3), // ลด padding เพื่อให้กะทัดรัด
  marginTop: theme.spacing(4), // ลด margin เพื่อให้อยู่ใกล้ขอบบน
  marginBottom: theme.spacing(4),
  borderRadius: theme.shape.borderRadius, // มุมโค้งเล็กน้อย
  boxShadow: theme.shadows[2], // เงาเบา ๆ
  background: theme.palette.background.paper, // ใช้สีพื้นหลังจาก theme
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
    marginTop: theme.spacing(2),
    marginLeft: theme.spacing(1),
    marginRight: theme.spacing(1),
  },
}));

// สไตล์สำหรับ Box ที่ใช้จัดวางข้อมูลและปุ่ม
const InfoBox = styled(Box)(({ theme }) => ({
  width: '100%',
  marginBottom: theme.spacing(2), // ระยะห่างก่อนปุ่ม
}));

// สไตล์สำหรับ Box ที่จัดวางปุ่ม
const ButtonBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center', // จัดปุ่มให้อยู่กึ่งกลาง
  gap: theme.spacing(2), // ระยะห่างระหว่างปุ่ม
  marginTop: theme.spacing(2),
}));

const Profile: React.FC = () => {
  // สถานะสำหรับจัดการข้อมูลผู้ใช้, loading state และ error
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // ใช้ navigate สำหรับการ redirect
  const navigate = useNavigate();

  // ใช้ AuthContext เพื่อจัดการการ logout และตรวจสอบ authentication
  const { logout, isAuthenticated } = useContext(AuthContext);

  // useEffect สำหรับดึงข้อมูลผู้ใช้เมื่อ component โหลด
  useEffect(() => {
    // ฟังก์ชัน async สำหรับดึงข้อมูล
    const fetchUser = async () => {
      try {
        // เรียก getProfile โดยส่ง object ว่าง เพราะใช้ token จาก cookie
        const data = await getProfile({});
        setUser(data);
        setLoading(false);
      } catch (err: any) {
        // จัดการ error โดยเฉพาะสำหรับ 401 หรือ endpoint ไม่ถูกต้อง
        if (err.response?.status === 401) {
          setError('Token ไม่ถูกต้องหรือหมดอายุ กรุณา login ใหม่');
          logout();
          navigate('/login');
        } else {
          setError(err.message || 'ไม่สามารถโหลดโปรไฟล์ได้');
        }
        setLoading(false);
      }
    };

    // เรียก fetchUser ถ้า authenticated
    if (isAuthenticated) {
      fetchUser();
    } else {
      // ถ้าไม่ได้ login ให้ redirect ไปหน้า login
      navigate('/login');
    }
  }, [isAuthenticated, navigate, logout]);

  // ฟังก์ชันสำหรับจัดการ logout
  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  // ฟังก์ชันสำหรับกลับไปหน้า Home
  const handleBackToHome = () => {
    navigate('/');
  };

  // ถ้ากำลังโหลด แสดง CircularProgress
  if (loading) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Box display="flex" justifyContent="center" py={4}>
            <CircularProgress color="primary" />
          </Box>
        </StyledPaper>
      </Container>
    );
  }

  // ถ้ามี error แสดง Alert
  if (error) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Alert severity="error" sx={{ width: '100%', m: 2 }}>
            {error}
          </Alert>
        </StyledPaper>
      </Container>
    );
  }

  // ถ้าไม่มี user (ไม่น่าจะเกิดขึ้น แต่เพื่อความปลอดภัย)
  if (!user) {
    return null;
  }

  return (
    <Container maxWidth="sm">
      <StyledPaper elevation={2}>
        {/* ข้อมูลโปรไฟล์: ใช้ List เพื่อแสดงข้อมูลตาม layout ที่กำหนด */}
        <InfoBox>
          <List>
            {/* ID ผู้ใช้ */}
            <ListItem>
              <ListItemIcon>
                <PersonIcon color="primary" />
              </ListItemIcon>
              <ListItemText
                primary="ID ผู้ใช้"
                secondary={user.id}
                primaryTypographyProps={{ fontWeight: 'bold' }}
              />
            </ListItem>
            <Divider component="li" />

            {/* อีเมล */}
            <ListItem>
              <ListItemIcon>
                <EmailIcon color="primary" />
              </ListItemIcon>
              <ListItemText
                primary="อีเมล"
                secondary={user.email}
                primaryTypographyProps={{ fontWeight: 'bold' }}
              />
            </ListItem>
            <Divider component="li" />

            {/* บทบาท */}
            <ListItem>
              <ListItemIcon>
                <AdminPanelSettingsIcon color="primary" />
              </ListItemIcon>
              <ListItemText
                primary="บทบาท"
                secondary="Admin"
                primaryTypographyProps={{ fontWeight: 'bold' }}
              />
            </ListItem>
            <Divider component="li" />
          </List>
        </InfoBox>

        {/* ปุ่ม Actions: ใช้ IconButton แทนปุ่มปกติ */}
        <ButtonBox>
          <IconButton
            color="primary"
            onClick={handleBackToHome}
            aria-label="กลับไปหน้า Home"
          >
            <HomeIcon />
          </IconButton>
          <IconButton
            color="secondary"
            onClick={handleLogout}
            aria-label="ออกจากระบบ"
          >
            <LogoutIcon />
          </IconButton>
        </ButtonBox>
      </StyledPaper>
    </Container>
  );
};

export default Profile;
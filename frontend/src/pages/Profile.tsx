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
  Button,
  Typography,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { AuthContext } from '../contexts/AuthContext';
import { getProfile } from '../services/profile';
import EmailIcon from '@mui/icons-material/Email';
import PersonIcon from '@mui/icons-material/Person';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import HomeIcon from '@mui/icons-material/Home';
import LogoutIcon from '@mui/icons-material/Logout';

// อินเทอร์เฟซสำหรับข้อมูลผู้ใช้
interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

// สไตล์สำหรับ Paper component
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginTop: theme.spacing(4),
  marginBottom: theme.spacing(4),
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[2],
  background: theme.palette.background.paper,
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
  marginBottom: theme.spacing(2),
}));

// สไตล์สำหรับ Box ที่จัดวางปุ่ม
const ButtonBox = styled(Box)(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  gap: theme.spacing(2),
  marginTop: theme.spacing(2),
}));

const Profile: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const data = await getProfile({});
        setUser(data);
        setLoading(false);
      } catch (err: any) {
        setLoading(false);
        if (err.response?.status === 401) {
          setError('Token ไม่ถูกต้องหรือหมดอายุ กรุณา login ใหม่');
          logout(); // ตั้ง isAuthenticated เป็น false และลบ token
        } else {
          setError(err.message || 'ไม่สามารถโหลดโปรไฟล์ได้');
        }
      }
    };

    if (isAuthenticated) {
      fetchUser();
    } else {
      setLoading(false); // ไม่โหลดข้อมูลถ้าไม่ได้ login
      setError('กรุณาเข้าสู่ระบบเพื่อดูโปรไฟล์');
    }
  }, [isAuthenticated, logout]);

  const handleLoginRedirect = () => {
    navigate('/login');
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleBackToHome = () => {
    navigate('/');
  };

  // ถ้ากำลังโหลด
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

  // ถ้าไม่ได้ login หรือ token ไม่ valid แสดงปุ่ม login
  if (!isAuthenticated || error?.includes('Token ไม่ถูกต้อง')) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <Typography variant="h6" align="center" gutterBottom>
            คุณยังไม่ได้เข้าสู่ระบบ
          </Typography>
          {error && (
            <Alert severity="error" sx={{ width: '100%', m: 2 }}>
              {error}
            </Alert>
          )}
          <Button
            fullWidth
            variant="contained"
            color="primary"
            onClick={handleLoginRedirect}
            sx={{ mt: 2 }}
          >
            ไปที่หน้าเข้าสู่ระบบ
          </Button>
        </StyledPaper>
      </Container>
    );
  }

  // ถ้ามี error อื่น ๆ
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

  // ถ้ามีข้อมูล user
  if (user) {
    return (
      <Container maxWidth="sm">
        <StyledPaper elevation={2}>
          <InfoBox>
            <List>
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
              <ListItem>
                <ListItemIcon>
                  <AdminPanelSettingsIcon color="primary" />
                </ListItemIcon>
                <ListItemText
                  primary="บทบาท"
                  secondary={user.role || 'Admin'}
                  primaryTypographyProps={{ fontWeight: 'bold' }}
                />
              </ListItem>
              <Divider component="li" />
            </List>
          </InfoBox>
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
  }

  return null;
};

export default Profile;
import React, { useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Link,
  Alert,
  CircularProgress,
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { AuthContext } from '../contexts/AuthContext';
import { login as apiLogin } from '../services/auth';

// สไตล์สำหรับ Paper component เพื่อให้ดูสวยงามและ responsive
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  marginTop: theme.spacing(8),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
    marginTop: theme.spacing(2), // แก้จาก -16 เป็น 2 เพื่อเลี่ยง layout ผิดปกติ
  },
}));

const Login: React.FC = () => {
  // สถานะสำหรับจัดการฟอร์ม, error และ loading
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // ใช้ navigate สำหรับการ redirect
  const navigate = useNavigate();

  // ใช้ AuthContext เพื่อจัดการ login และตรวจสอบ authentication
  const { login, isAuthenticated } = useContext(AuthContext);

  // Redirect ถ้า login แล้ว
  React.useEffect(() => {
    if (isAuthenticated) {
      navigate('/', { replace: true });
    }
  }, [isAuthenticated, navigate]);

  // ฟังก์ชันจัดการการ submit ฟอร์ม
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // เรียก service login โดยส่ง payload เป็น object
      const accessToken = await apiLogin({ email, password });
      // อัพเดท state และ cookie ด้วย access_token
      login(accessToken);
      // Redirect ไปหน้า home (จัดการโดย useEffect)
    } catch (err: any) {
      // ตั้งค่า error จาก service หรือข้อความ default
      setError(err.message || 'เกิดข้อผิดพลาดในการเข้าสู่ระบบ');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xs">
      <StyledPaper elevation={6}>
        {/* หัวข้อหน้า */}
        <Typography variant="h5" align="center" gutterBottom>
          เข้าสู่ระบบ
        </Typography>

        {/* แสดง error ถ้ามี */}
        {error && (
          <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
            {error}
          </Alert>
        )}

        {/* ฟอร์มเข้าสู่ระบบ */}
        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
          <TextField
            label="อีเมล"
            type="email"
            fullWidth
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
          <TextField
            label="รหัสผ่าน"
            type="password"
            fullWidth
            margin="normal"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'เข้าสู่ระบบ'}
          </Button>
          <Link
            href="/register"
            variant="body2"
            sx={{ display: 'block', textAlign: 'center' }}
          >
            ยังไม่มีบัญชี? สมัครสมาชิก
          </Link>
        </Box>
      </StyledPaper>
    </Container>
  );
};

export default Login;
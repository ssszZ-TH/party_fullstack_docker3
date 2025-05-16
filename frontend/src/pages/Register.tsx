import React, { useState } from 'react';
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
import { register } from '../services/auth';

// สไตล์สำหรับ Paper component เพื่อให้ดูสวยงามและ responsive
const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  marginTop: theme.spacing(8),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  [theme.breakpoints.down('sm')]: {
    padding: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
}));

const Register: React.FC = () => {
  // สถานะสำหรับจัดการฟอร์ม, error และ loading
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // ใช้ navigate สำหรับการ redirect
  const navigate = useNavigate();

  // ฟังก์ชันจัดการการ submit ฟอร์ม
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // เรียก service register โดยส่ง payload เป็น object
      await register({ name, email, password });
      // ถ้าสำเร็จ redirect ไปหน้า login
      navigate('/login');
    } catch (err: any) {
      // ตั้งค่า error จาก service หรือข้อความ default
      setError(err.message || 'เกิดข้อผิดพลาดในการสมัครสมาชิก');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="xs">
      <StyledPaper elevation={6}>
        {/* หัวข้อหน้า */}
        <Typography variant="h5" align="center" gutterBottom>
          สมัครสมาชิก
        </Typography>

        {/* แสดง error ถ้ามี */}
        {error && (
          <Alert severity="error" sx={{ mb: 2, width: '100%' }}>
            {error}
          </Alert>
        )}

        {/* ฟอร์มสมัครสมาชิก */}
        <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%' }}>
          <TextField
            label="ชื่อ"
            fullWidth
            margin="normal"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            disabled={loading}
          />
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
            {loading ? <CircularProgress size={24} /> : 'สมัครสมาชิก'}
          </Button>
          <Link
            href="/login"
            variant="body2"
            sx={{ display: 'block', textAlign: 'center' }}
          >
            มีบัญชีแล้ว? เข้าสู่ระบบ
          </Link>
        </Box>
      </StyledPaper>
    </Container>
  );
};

export default Register;
// styles/theme.ts
import { createTheme } from '@mui/material/styles';

export const lightTheme = createTheme({
  palette: {
    primary: {
      main: '#86B5EA', // สีปุ่มหลัก (Update, Add)
      light: '#A8C9F0', // สีอ่อนกว่า
      dark: '#5E9AE5', // สีเข้มกว่า
      contrastText: '#273D54', // สีตัวหนังสือ
    },
    secondary: {
      main: '#FFB3BA', // สีปุ่มแดง
      contrastText: '#273D54', // สีตัวหนังสือ (เหมือนเดิม)
    },
    error: {
      main: '#FFB3BA', // ใช้สีแดงเดียวกันสำหรับ error state
    },
    background: {
      default: '#E7F1FC', // สีฉากหลัง
      paper: '#FFFFFF', // สีพื้นของ Card, Modal
    },
    text: {
      primary: '#273D54', // สีตัวหนังสือหลัก
      secondary: '#5A6A85', // สีตัวหนังสือรอง (โทนเดียวกันแต่อ่อนกว่า)
    },
  },
  typography: {
    fontFamily: [
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif'
    ].join(','),
    h6: {
      fontWeight: 600, // ตัวหนาสำหรับหัวข้อ
      color: '#273D54'
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#E7F1FC',
          color: '#273D54',
        },
      },
    },
    // ปรับแต่ง AppBar (Navbar)
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#86B5EA', // ใช้สีเดียวกับปุ่มหลัก
          color: '#273D54',
          boxShadow: 'none', // เอาตกแต่งเงาออก
        },
      },
    },
    // ปรับแต่งปุ่ม
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none', // ปิดการแปลงเป็นตัวใหญ่ทั้งหมด
          fontWeight: 600,
          borderRadius: '8px',
          padding: '8px 16px',
        },
        containedPrimary: {
          '&:hover': {
            backgroundColor: '#5E9AE5', // สีเข้มกว่าเมื่อโฮเวอร์
          },
        },
        containedSecondary: {
          '&:hover': {
            backgroundColor: '#FF9BA3', // สีแดงเข้มกว่าเมื่อโฮเวอร์
          },
        },
      },
    },
    // ปรับแต่งการ์ด
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.1)', // เงาแบบนุ่ม
        },
      },
    },
  },
  shape: {
    borderRadius: 8, // ความโค้งมุมพื้นฐาน
  },
});

export const darkTheme = createTheme({
  palette: {
    primary: {
      main: '#86B5EA', // สีปุ่มหลัก (Update, Add)
      light: '#A8C9F0', // สีอ่อนกว่า
      dark: '#5E9AE5', // สีเข้มกว่า
      contrastText: '#273D54', // สีตัวหนังสือ
    },
    secondary: {
      main: '#FFB3BA', // สีปุ่มแดง
      contrastText: '#273D54', // สีตัวหนังสือ (เหมือนเดิม)
    },
    error: {
      main: '#FFB3BA', // ใช้สีแดงเดียวกันสำหรับ error state
    },
    background: {
      default: '#E7F1FC', // สีฉากหลัง
      paper: '#FFFFFF', // สีพื้นของ Card, Modal
    },
    text: {
      primary: '#273D54', // สีตัวหนังสือหลัก
      secondary: '#5A6A85', // สีตัวหนังสือรอง (โทนเดียวกันแต่อ่อนกว่า)
    },
  },
  typography: {
    fontFamily: [
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif'
    ].join(','),
    h6: {
      fontWeight: 600, // ตัวหนาสำหรับหัวข้อ
      color: '#273D54'
    },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        body: {
          backgroundColor: '#E7F1FC',
          color: '#273D54',
        },
      },
    },
    // ปรับแต่ง AppBar (Navbar)
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#86B5EA', // ใช้สีเดียวกับปุ่มหลัก
          color: '#273D54',
          boxShadow: 'none', // เอาตกแต่งเงาออก
        },
      },
    },
    // ปรับแต่งปุ่ม
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none', // ปิดการแปลงเป็นตัวใหญ่ทั้งหมด
          fontWeight: 600,
          borderRadius: '8px',
          padding: '8px 16px',
        },
        containedPrimary: {
          '&:hover': {
            backgroundColor: '#5E9AE5', // สีเข้มกว่าเมื่อโฮเวอร์
          },
        },
        containedSecondary: {
          '&:hover': {
            backgroundColor: '#FF9BA3', // สีแดงเข้มกว่าเมื่อโฮเวอร์
          },
        },
      },
    },
    // ปรับแต่งการ์ด
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0px 2px 8px rgba(0, 0, 0, 0.1)', // เงาแบบนุ่ม
        },
      },
    },
  },
  shape: {
    borderRadius: 8, // ความโค้งมุมพื้นฐาน
  },
});
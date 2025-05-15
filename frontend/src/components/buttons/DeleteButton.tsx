import React from "react";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete"; // Icon ถังขยะ
import { useTheme } from "@mui/material/styles";

interface DeleteButtonProps {
  onClick: () => void; // รับฟังก์ชัน onClick จากภายนอก
  disabled?: boolean; // เพิ่ม prop disabled เพื่อควบคุมการคลิก
}

/**
 * Reusable Delete Button Component
 * - Uses theme's error color
 * - Displays delete icon
 * - Accepts onClick handler from parent
 */
const DeleteButton: React.FC<DeleteButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme(); // ดึง theme จาก MUI

  return (
    <Button
      variant="contained"
      onClick={onClick}
      disabled={disabled}
      sx={{
        backgroundColor: theme.palette.error.main, // สีจาก theme
        color: theme.palette.error.contrastText, // สีข้อความจาก theme
        "&:hover": {
          backgroundColor: theme.palette.error.dark, // สีเมื่อโฮเวอร์
        },
      }}
    >
      <DeleteIcon />
    </Button>
  );
};

export default DeleteButton;

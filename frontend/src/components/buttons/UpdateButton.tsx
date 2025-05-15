import React from "react";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit"; // Icon ปากกา
import { useTheme } from "@mui/material/styles";

interface UpdateButtonProps {
  onClick: () => void; // รับฟังก์ชัน onClick จากภายนอก
  disabled?: boolean; // เพิ่ม prop disabled เพื่อควบคุมการคลิก
}

/**
 * Reusable Update Button Component
 * - Uses theme's primary color
 * - Displays edit icon
 * - Accepts onClick handler from parent
 */
const UpdateButton: React.FC<UpdateButtonProps> = ({
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
        backgroundColor: theme.palette.primary.main, // สีจาก theme
        color: theme.palette.primary.contrastText, // สีข้อความจาก theme
        "&:hover": {
          backgroundColor: theme.palette.primary.dark, // สีเมื่อโฮเวอร์
        },
      }}
    >
      <EditIcon />
    </Button>
  );
};

export default UpdateButton;

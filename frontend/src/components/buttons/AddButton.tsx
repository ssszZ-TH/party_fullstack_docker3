import React from "react";
import Button from "@mui/material/Button";
import AddIcon from "@mui/icons-material/Add"; // Icon บวก
import { useTheme } from "@mui/material/styles";
import { Tooltip } from "@mui/material";

interface AddButtonProps {
  onClick: () => void;
  disabled?: boolean;
  label?: string; // เพิ่ม prop สำหรับเปลี่ยนข้อความได้
}

/**
 * Reusable Add Button Component
 * - Uses theme's primary color
 * - Displays plus icon
 * - Accepts custom label
 */
const AddButton: React.FC<AddButtonProps> = ({
  onClick,
  disabled = false,
  label = "Add", // ค่า default
}) => {
  const theme = useTheme();

  return (
    <Tooltip title={label} placement="top">
      <Button
        variant="contained"
        onClick={onClick}
        disabled={disabled}
        sx={{
          backgroundColor: theme.palette.primary.main,
          color: theme.palette.primary.contrastText,
          "&:hover": {
            backgroundColor: theme.palette.primary.dark,
          },
          margin: "4px",
          textTransform: "none", // ป้องกันตัวอักษรใหญ่ทั้งหมด
        }}
      >
        <AddIcon />
      </Button>
    </Tooltip>
  );
};

export default AddButton;

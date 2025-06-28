import React from "react";
import Button from "@mui/material/Button";
import GroupIcon from "@mui/icons-material/Group";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface SizeButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const SizeButton: React.FC<SizeButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Manage Size for this organization" placement="top">
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
          textTransform: "none",
          display: "flex",
          alignItems: "center",
          gap: 1,
        }}
      >
        <GroupIcon />
        Size
      </Button>
    </Tooltip>
  );
};

export default SizeButton;
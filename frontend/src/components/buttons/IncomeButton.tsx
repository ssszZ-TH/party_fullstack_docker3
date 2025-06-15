import React from "react";
import Button from "@mui/material/Button";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface IncomeButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const IncomeButton: React.FC<IncomeButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Manage income for this person" placement="top">
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
        <AttachMoneyIcon />
        Income
      </Button>
    </Tooltip>
  );
};

export default IncomeButton;
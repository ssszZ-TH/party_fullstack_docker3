import React from "react";
import Button from "@mui/material/Button";
import CloseIcon from "@mui/icons-material/Close";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface CancelButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const CancelButton: React.FC<CancelButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Cancel" placement="top">
      <Button
        variant="contained"
        onClick={onClick}
        disabled={disabled}
        sx={{
          backgroundColor: theme.palette.error.main,
          color: theme.palette.error.contrastText,
          "&:hover": {
            backgroundColor: theme.palette.error.dark,
          },
          margin: "4px",
          textTransform: "none",
        }}
      >
        <CloseIcon />
      </Button>
    </Tooltip>
  );
};

export default CancelButton;
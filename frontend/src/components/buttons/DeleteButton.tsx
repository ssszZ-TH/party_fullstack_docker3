import React from "react";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface DeleteButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const DeleteButton: React.FC<DeleteButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Delete" placement="top">
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
        <DeleteIcon />
      </Button>
    </Tooltip>
  );
};

export default DeleteButton;
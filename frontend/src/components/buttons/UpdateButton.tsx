import React from "react";
import Button from "@mui/material/Button";
import EditIcon from "@mui/icons-material/Edit";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface UpdateButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const UpdateButton: React.FC<UpdateButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Edit" placement="top">
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
        }}
      >
        <EditIcon />
      </Button>
    </Tooltip>
  );
};

export default UpdateButton;
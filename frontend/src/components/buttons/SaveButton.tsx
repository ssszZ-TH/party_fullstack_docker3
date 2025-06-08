import React from "react";
import Button from "@mui/material/Button";
import SaveIcon from "@mui/icons-material/Save";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface SaveButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const SaveButton: React.FC<SaveButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Save" placement="top">
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
        <SaveIcon />
      </Button>
    </Tooltip>
  );
};

export default SaveButton;
import React from "react";
import Button from "@mui/material/Button";
import Diversity3Icon from "@mui/icons-material/Diversity3";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface MinorityButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const MinorityButton: React.FC<MinorityButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Manage Minority status for this person" placement="top">
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
        <Diversity3Icon />
        Minority
      </Button>
    </Tooltip>
  );
};

export default MinorityButton;
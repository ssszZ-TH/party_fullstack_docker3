import React from "react";
import Button from "@mui/material/Button";
import PassportIcon from "@mui/icons-material/CardTravel";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface PassportButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const PassportButton: React.FC<PassportButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Manage passports for this citizenship" placement="top">
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
        <PassportIcon />
        Passport
      </Button>
    </Tooltip>
  );
};

export default PassportButton;
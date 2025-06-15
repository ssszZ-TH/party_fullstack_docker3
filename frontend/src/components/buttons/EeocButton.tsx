import React from "react";
import Button from "@mui/material/Button";
import EqualizerIcon from "@mui/icons-material/Equalizer";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface EeocButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const EeocButton: React.FC<EeocButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Manage EEOC for this person" placement="top">
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
        <EqualizerIcon />
        EEOC
      </Button>
    </Tooltip>
  );
};

export default EeocButton;
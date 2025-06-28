import React from "react";
import Button from "@mui/material/Button";
import BusinessIcon from "@mui/icons-material/Business";
import { useTheme } from "@mui/material/styles";
import Tooltip from "@mui/material/Tooltip";

interface IndustryButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

const IndustryButton: React.FC<IndustryButtonProps> = ({
  onClick,
  disabled = false,
}) => {
  const theme = useTheme();

  return (
    <Tooltip title="Manage Industry for this organization" placement="top">
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
        <BusinessIcon />
        Industry
      </Button>
    </Tooltip>
  );
};

export default IndustryButton;
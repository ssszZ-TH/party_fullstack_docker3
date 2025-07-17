import React from "react";
import { useNavigate } from "react-router-dom";
import { useTheme } from "@mui/material/styles";
import { Box, Button, } from "@mui/material";
import AppBarCustom from "../../components/AppBarCustom";

const organizationMenuItems = [
  { name: "Team", path: "/v1/team" },
  { name: "Family", path: "/v1/family" },
  { name: "Government Agency", path: "/v1/governmentagency" },
  { name: "Corporation", path: "/v1/corporation" },
  { name: "Other Informal Organization", path: "/v1/otherinformalorganization" },
];

export default function OrganizationMenu() {
  const navigate = useNavigate();
  const theme = useTheme();

  return (
    <>
      <AppBarCustom title={`Select Organization Type`} />
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          minHeight: "calc(100vh - 64px)", // Adjust for AppBar height
          gap: 2,
          p: 2,
        }}
      >
        {organizationMenuItems.map((item) => (
          <Button
            key={item.path}
            variant="contained"
            onClick={() => navigate(item.path)}
            sx={{
              backgroundColor: theme.palette.primary.main,
              color: theme.palette.primary.contrastText,
              "&:hover": {
                backgroundColor: theme.palette.primary.dark,
              },
              width: "100%",
              maxWidth: "400px",
              padding: "12px 24px",
              fontSize: "1.1rem",
              textTransform: "none",
            }}
          >
            {item.name}
          </Button>
        ))}
      </Box>
    </>
  );
}
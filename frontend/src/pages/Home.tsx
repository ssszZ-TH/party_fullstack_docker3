import React, { useContext, useEffect } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import {
  Box,
  Container,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";
import {
  Person as PersonIcon,
  Settings as SettingsIcon,
  Info as AboutIcon,
  Storage as DatabaseIcon,
  School as TutorialIcon,
} from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";
import { AuthContext } from "../contexts/AuthContext";
import { getProfile } from "../services/profile";

// Services data arrays
const services = [
  {
    title: "Role",
    items: [{ name: "Party Role", path: "/v1/partyrole" }],
  },
  {
    title: "Classify",
    items: [
      { name: "Classify by Minority", path: "/v1/classifybyminority" },
      { name: "Classify by Size", path: "/v1/classifybysize" },
      { name: "Classify by Industry", path: "/v1/classifybyindustry" },
      { name: "Classify by Income", path: "/v1/classifybyincome" },
      { name: "Classify by EEOC", path: "/v1/classifybyeeoc" },
    ],
  },
  {
    title: "Organization",
    items: [
      { name: "Specific Organization Type", path: "/v1/organizationmenu" },
      { name: "Organization", path: "/v1/organization" },
    ],
  },
  {
    title: "Person",
    items: [
      { name: "Physical Characteristic", path: "/v1/physicalcharacteristic" },
      { name: "Passport", path: "/v1/passport" },
      { name: "Citizenship", path: "/v1/citizenship" },
      { name: "Person Name", path: "/v1/personname" },
      { name: "Marital Status", path: "/v1/maritalstatus" },
      { name: "Person", path: "/v1/person" },
    ],
  },
  {
    title: "Type",
    items: [
      { name: "Gender Type", path: "/v1/gendertype" },
      { name: "Minority Type", path: "/v1/minoritytype" },
      { name: "Employee Count Range", path: "/v1/employeecountrange" },
      { name: "Industry Type", path: "/v1/industrytype" },
      { name: "Income Range", path: "/v1/incomerange" },
      { name: "Ethnicity", path: "/v1/ethnicity" },
      {
        name: "Physical Characteristic Type",
        path: "/v1/physicalcharacteristictype",
      },
      { name: "Person Name Type", path: "/v1/personnametype" },
      { name: "Marital Status Type", path: "/v1/maritalstatustype" },
      {
        name: "Communication Event Purpose Type",
        path: "/v1/communicationeventpurposetype",
      },
      { name: "Contact Mechanism Type", path: "/v1/contactmechanismtype" },
      {
        name: "Communication Event Status Type",
        path: "/v1/communicationeventstatustype",
      },
      { name: "Priority Type", path: "/v1/prioritytype" },
      {
        name: "Party Relationship Status Type",
        path: "/v1/partyrelationshipstatustype",
      },
      { name: "Party Relationship Type", path: "/v1/partyrelationshiptype" },
      { name: "Role Type", path: "/v1/roletype" },
    ],
  },
  {
    title: "Base",
    items: [{ name: "Country", path: "/v1/country" }],
  },
];

// Navigation items
const navItems = [
  { name: "Profile", icon: <PersonIcon />, path: "/v1/profile" },
  { name: "Settings", icon: <SettingsIcon />, path: "/v1/settings" },
  { name: "About", icon: <AboutIcon />, path: "/v1/about" },
  { name: "Database", icon: <DatabaseIcon />, path: "/v1/database" },
  { name: "Tutorial", icon: <TutorialIcon />, path: "/v1/tutorial" },
];

export default function Home() {
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const theme = useTheme();

  useEffect(() => {
    const checkTokenValidity = async () => {
      console.log("Home: isAuthenticated =", isAuthenticated);
      if (!isAuthenticated) {
        console.log("Home: No authentication, redirecting to /login");
        navigate("/login", { replace: true });
        return;
      }
      try {
        console.log("Home: Checking token with getProfile");
        await getProfile();
        console.log("Home: Token is valid");
      } catch (err: any) {
        console.log("Home: Token check error:", err);
        logout();
        navigate("/login", { replace: true });
      }
    };

    checkTokenValidity();
  }, [logout, navigate]);

  const renderServiceGrid = (
    serviceItems: { name: string; path: string }[]
  ) => (
    <Box
      sx={{
        display: "flex",
        flexWrap: "wrap",
        gap: "12px",
        justifyContent: "flex-start",
      }}
    >
      {serviceItems.map((service) => (
        <Box
          key={service.path}
          component={RouterLink}
          to={service.path}
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            width: "110px",
            height: "110px",
            textDecoration: "none",
            transition: "transform 0.2s",
            "&:hover": {
              transform: "scale(1.05)",
            },
          }}
        >
          <Avatar
            src={`/home_thumbnail/${service.name
              .toLowerCase()
              .replace(/\s+/g, "_")}.png`}
            sx={{
              width: 60,
              height: 60,
              mb: 0.5,
              borderRadius: "10%",
            }}
          />
          <Typography
            variant="body2"
            align="center"
            color="text.primary"
            sx={{
              fontWeight: 500,
              fontSize: "0.75rem",
              lineHeight: 1.2,
              height: "28px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "100%",
              overflow: "hidden",
              textOverflow: "ellipsis",
            }}
          >
            {service.name}
          </Typography>
        </Box>
      ))}
    </Box>
  );

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <Box
        sx={{
          width: 240,
          position: "fixed",
          height: "100vh",
          bgcolor: "primary.light",
          boxShadow: 3,
          zIndex: 10,
        }}
      >
        <Box sx={{ p: 2, textAlign: "center" }}>
          <img
            src="/sphere_wire_frame.svg"
            alt="Logo"
            style={{
              width: "100%",
              objectFit: "contain",
            }}
          />
        </Box>
        <Divider />
        <List>
          {navItems.map((item) => (
            <ListItem key={item.name} disablePadding>
              <ListItemButton
                component={RouterLink}
                to={item.path}
                sx={{
                  "&:hover": {
                    bgcolor: theme.palette.action.hover,
                  },
                }}
              >
                <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
                <ListItemText primary={item.name} />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Box>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          ml: 30,
          position: "relative",
        }}
      >
        <img
          src="/sphere_wire_frame.svg"
          alt="Background"
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            height: "100vh",
            objectFit: "cover",
            zIndex: -1,
            opacity: 0.2,
          }}
        />
        <Container maxWidth="lg" sx={{ py: 4 }}>
          <Box sx={{ textAlign: "center", mb: 4 }}>
            <Typography variant="h4" gutterBottom>
              Party Sync
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              manage comprehensive party details, including individuals and
              organizations, with a focus on relationships, communications with
              layered data management.
            </Typography>
          </Box>
          {services.map((section) => (
            <Box key={section.title}>
              {renderServiceGrid(section.items)}
              <hr style={{ margin: "20px 0" }} />
            </Box>
          ))}
        </Container>
      </Box>
    </Box>
  );
}

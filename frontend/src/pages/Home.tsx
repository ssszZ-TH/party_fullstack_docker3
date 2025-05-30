import React, { useContext, useEffect } from "react";
import { Link as RouterLink, useNavigate } from "react-router-dom";
import {
  Box,
  Container,
  Grid,
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
  ArrowForward as ArrowForwardIcon,
} from "@mui/icons-material";
import { useTheme } from "@mui/material/styles";

// to check authentication
import { AuthContext } from "../contexts/AuthContext";
import { getProfile } from "../services/profile";

// Services data array
// อาร์เรย์ของ services
const services_layer_type = [
  { name: "Marital Status Type", path: "/v1/maritalstatustype" },

  { name: "Person Name Type", path: "/v1/personnametype" },
  {
    name: "Physical Characteristic Type",
    path: "/v1/physicalcharacteristictype",
  },
  { name: "Country", path: "/v1/country" },
  
  
  { name: "Party Type", path: "/v1/partytype" },

  // { name: "Legal Organization", path: "/v1/legalorganization" },
  // { name: "Informal Organization", path: "/v1/informalorganization" },
  { name: "Ethnicity", path: "/v1/ethnicity" },
  { name: "Income Range", path: "/v1/incomerange" },
  { name: "Industry Type", path: "/v1/industrytype" },
  { name: "Employee Count Range", path: "/v1/employeecountrange" },
  { name: "Minority Type", path: "/v1/minoritytype" },
  { name: "Gender Type", path: "/v1/gendertype" },
  { name: "Other Informal Organization", path: "/v1/otherinformalorganization" },
  { name: "Team", path: "/v1/team" },
  { name: "Family", path: "/v1/family" },

  { name: "Government Agency", path: "/v1/governmentagency" },
  { name: "Corporation", path: "/v1/corporation" },

];

const services_layer_info = [
  { name: "Marital Status", path: "/v1/maritalstatus" },
  { name: "Person Name", path: "/v1/personname" },
  { name: "Citizenship", path: "/v1/citizenship" },
  { name: "Passport", path: "/v1/passport" },
  { name: "Person", path: "/v1/person" },
  { name: "Physical Characteristic", path: "/v1/physicalcharacteristic" },
  { name: "Classify by EEOC", path: "/v1/classifybyeeoc" },
  { name: "Classify by Income", path: "/v1/classifybyincome" },
  { name: "Classify by Industry", path: "/v1/classifybyindustry" },
  { name: "Classify by Size", path: "/v1/classifybysize" },
  { name: "Classify by Minority", path: "/v1/classifybyminority" },
  
];

const services_layer_relation = [
  { name: "Classify by Minority", path: "/v1/classifybyminority" },

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
  //do about authentication
  const { isAuthenticated, logout } = useContext(AuthContext);
  const navigate = useNavigate();

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
        await getProfile({});
        console.log("Home: Token is valid");
      } catch (err: any) {
        console.log("Home: Token check error:", err);
        logout();
        navigate("/login", { replace: true });
      }
    };

    checkTokenValidity();
  }, [logout, navigate]); // ถ้าม logout หรือ navigate เปลี่ยนแปลง จะเรียก useEffect ใหม่

  const theme = useTheme();

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      {/* Vertical Navigation Bar */}
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
        {/* Logo */}
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

        {/* Navigation Items */}
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

      {/* Main Content Area */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          ml: 30, // Match nav width + spacing
          position: "relative",
        }}
      >
        {/* Background Graphic */}
        <img
          src="/sphere_wire_frame.svg"
          alt="Background"
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            // width: "100%",
            height: "100vh",
            objectFit: "cover",
            zIndex: -1,
            opacity: 0.2,
          }}
        />

        {/* Content Container */}
        <Container maxWidth="lg" sx={{ py: 4 }}>
          {/* Page Header */}
          <Box sx={{ textAlign: "center", mb: 4 }}>
            <Typography variant="h4" gutterBottom>
              Party Model Admin
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Explore and manage your services
            </Typography>
          </Box>

          {/* Services Grid */}
          <Box
            sx={{
              display: "flex",
              flexWrap: "wrap",
              gap: "12px", // Reduced gap between items
              justifyContent: "flex-start",
            }}
          >
            {services_layer_type.map((service) => (
              <Box
                key={service.path}
                component={RouterLink}
                to={service.path}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  width: "110px", // Compact width
                  height: "110px", // Compact height
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
                    width: 60, // Smaller thumbnail
                    height: 60,
                    mb: 0.5, // Reduced margin
                    borderRadius: "10%",
                  }}
                />
                <Typography
                  variant="body2"
                  align="center"
                  color="text.primary"
                  sx={{
                    fontWeight: 500,
                    fontSize: "0.75rem", // Smaller text
                    lineHeight: 1.2,
                    height: "28px", // Fixed height for text
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

          <hr style={{ margin: "20px 0" }} />

          {/* Services Grid */}
          <Box
            sx={{
              display: "flex",
              flexWrap: "wrap",
              gap: "12px", // Reduced gap between items
              justifyContent: "flex-start",
            }}
          >
            {services_layer_info.map((service) => (
              <Box
                key={service.path}
                component={RouterLink}
                to={service.path}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  width: "110px", // Compact width
                  height: "110px", // Compact height
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
                    width: 60, // Smaller thumbnail
                    height: 60,
                    mb: 0.5, // Reduced margin
                    borderRadius: "10%",
                  }}
                />
                <Typography
                  variant="body2"
                  align="center"
                  color="text.primary"
                  sx={{
                    fontWeight: 500,
                    fontSize: "0.75rem", // Smaller text
                    lineHeight: 1.2,
                    height: "28px", // Fixed height for text
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
          
          <hr style={{ margin: "20px 0" }} />

          {/* Services Grid */}
          <Box
            sx={{
              display: "flex",
              flexWrap: "wrap",
              gap: "12px", // Reduced gap between items
              justifyContent: "flex-start",
            }}
          >
            {services_layer_relation.map((service) => (
              <Box
                key={service.path}
                component={RouterLink}
                to={service.path}
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  width: "110px", // Compact width
                  height: "110px", // Compact height
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
                    width: 60, // Smaller thumbnail
                    height: 60,
                    mb: 0.5, // Reduced margin
                    borderRadius: "10%",
                  }}
                />
                <Typography
                  variant="body2"
                  align="center"
                  color="text.primary"
                  sx={{
                    fontWeight: 500,
                    fontSize: "0.75rem", // Smaller text
                    lineHeight: 1.2,
                    height: "28px", // Fixed height for text
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
        </Container>
      </Box>
    </Box>
  );
}

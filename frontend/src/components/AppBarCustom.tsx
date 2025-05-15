import * as React from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuIcon from "@mui/icons-material/Menu";
import Container from "@mui/material/Container";
import Avatar from "@mui/material/Avatar";
import Button from "@mui/material/Button";
import Tooltip from "@mui/material/Tooltip";
import MenuItem from "@mui/material/MenuItem";
import ArrowBackIcon from "@mui/icons-material/ArrowBack"; // Changed from AdbIcon to ArrowBack
import { styled, useTheme } from "@mui/material/styles";

interface ResponsiveAppBarProps {
  title: string;
}

const settings = ["Profile", "Account", "Dashboard", "Logout"];

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  background: theme.palette.primary.main,
  boxShadow: theme.shadows[4],
}));

const StyledMenuItem = styled(MenuItem)(({ theme }) => ({
  "&:hover": {
    backgroundColor: theme.palette.primary.light,
    color: theme.palette.primary.contrastText,
    transition: "background-color 0.2s ease-in-out",
  },
}));

function ResponsiveAppBar({ title }: ResponsiveAppBarProps) {
  const theme = useTheme();

  const [titleText] = React.useState<string>(title || "...");

  const handleGoHome = () => {
    window.location.href = "/";
  };





  return (
    <StyledAppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Back Arrow Icon (Left-most element) */}
          <IconButton
            edge="start" // This makes it stick to the left
            color="inherit"
            aria-label="go back"
            onClick={handleGoHome}
            sx={{ 
              mr: 1,
              "&:hover": { 
                backgroundColor: theme.palette.action.hover,
                transform: "scale(1.1)",
                transition: "all 0.2s ease-in-out"
              }
            }}
          >
            <ArrowBackIcon />
          </IconButton>

          {/* Title (Center) */}
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{
              flexGrow: 1,
              display: { xs: "none", md: "flex" },
              fontFamily: theme.typography.fontFamily,
              fontWeight: 700,
              letterSpacing: ".1rem",
              color: "inherit",
              justifyContent: "center", // Center the title
              ml: -5 // Adjust to compensate for arrow button
            }}
          >
            {titleText}
          </Typography>

          {/* Mobile Title */}
          <Typography
            variant="h5"
            noWrap
            component="div"
            sx={{
              flexGrow: 1,
              display: { xs: "flex", md: "none" },
              fontFamily: theme.typography.fontFamily,
              fontWeight: 700,
              letterSpacing: ".1rem",
              color: "inherit",
              justifyContent: "center"
            }}
          >
            {titleText}
          </Typography>

          {/* User Menu (Right) */}
          <Box sx={{ flexGrow: 0 }}>
          </Box>
        </Toolbar>
      </Container>
    </StyledAppBar>
  );
}

export default ResponsiveAppBar;
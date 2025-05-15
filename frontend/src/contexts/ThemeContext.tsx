// contexts/ThemeContext.tsx

// Import necessary React hooks and MUI components
import { createContext, useContext, useState, useMemo } from 'react';
import { ThemeProvider as MuiThemeProvider } from '@mui/material';
// Import theme configurations
import { lightTheme, darkTheme } from '../styles/theme';

// Define the shape (type) of our theme context
type ThemeContextType = {
  toggleTheme: () => void;    // Function to switch between themes
  isDarkMode: boolean;        // Current theme status (true = dark, false = light)
};

// Create context with default values
const ThemeContext = createContext<ThemeContextType>({
  toggleTheme: () => {},      // Empty default toggle function
  isDarkMode: false,          // Default to light theme
});

// Custom hook to easily access theme context
export const useTheme = () => useContext(ThemeContext);

// Theme provider component (wrap around your app)
export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  // State to track dark mode status
  const [isDarkMode, setIsDarkMode] = useState(false);
  
  // Memoize theme object to prevent unnecessary recalculations
  const theme = useMemo(() => 
    isDarkMode ? darkTheme : lightTheme,  // Choose theme based on mode
    [isDarkMode]                          // Recalculate only when mode changes
  );

  // Function to toggle between dark/light modes
  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);  // Flip current state
  };

  return (
    // Provide theme context to child components
    <ThemeContext.Provider value={{ toggleTheme, isDarkMode }}>
      {/* Apply MUI theme to all children */}
      <MuiThemeProvider theme={theme}>
        {children}
      </MuiThemeProvider>
    </ThemeContext.Provider>
  );
};
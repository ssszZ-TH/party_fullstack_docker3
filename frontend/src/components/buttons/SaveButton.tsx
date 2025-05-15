import React from 'react';
import Button from '@mui/material/Button';
import SaveIcon from '@mui/icons-material/Save';
import { useTheme } from '@mui/material/styles';

interface SaveButtonProps {
  onClick: () => void;
  disabled?: boolean;
}

/**
 * Reusable Save Button Component
 * - Uses theme's primary color
 * - Displays save icon (floppy disk)
 * - Consistent with other button styles
 */
const SaveButton: React.FC<SaveButtonProps> = ({ 
  onClick, 
  disabled = false 
}) => {
  const theme = useTheme();

  return (
    <Button
      variant="contained"
      onClick={onClick}
      disabled={disabled}
      sx={{
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.primary.contrastText,
        '&:hover': {
          backgroundColor: theme.palette.primary.dark,
        },
        margin: '4px',
        textTransform: 'none'
      }}
    >
        <SaveIcon />
    </Button>
  );
};

export default SaveButton;
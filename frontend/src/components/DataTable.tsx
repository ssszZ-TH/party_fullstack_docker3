import { DataGrid, GridColDef } from "@mui/x-data-grid";
import Paper from "@mui/material/Paper";
import { useTheme } from "@mui/material/styles";

interface DataTableProps {
  columns: GridColDef[];
  rows: any[];
  getRowId?: (row: any) => string | number;
}

const paginationModel = { page: 0, pageSize: 10 };

export default function DataTable({ columns, rows, getRowId }: DataTableProps) {
  const theme = useTheme(); // เรียกใช้ theme จาก context

  return (
    <Paper 
      sx={{ 
        height: "82vh", 
        width: "100%",
        backgroundColor: theme.palette.background.default, // ใช้สีจาก theme
        boxShadow: theme.shadows[3], // ใช้ shadow จาก theme
      }}
    >
      <DataGrid
        rows={rows}
        columns={columns}
        initialState={{ pagination: { paginationModel } }}
        pageSizeOptions={[5, 10, 20, 50, 100, 200]}
        getRowId={getRowId}
        sx={{
          border: 0,
          '& .MuiDataGrid-columnHeaders': {
            backgroundColor: theme.palette.primary.main, // สีหัวคอลัมน์
            color: theme.palette.primary.contrastText, // สีข้อความหัวคอลัมน์
            fontSize: '0.875rem',
          },
          '& .MuiDataGrid-cell': {
            borderBottom: `1px solid ${theme.palette.divider}`, // เส้นแบ่งแถว
          },
          '& .MuiDataGrid-row:hover': {
            backgroundColor: theme.palette.action.hover, // สีเมื่อ hover
          },
          '& .MuiTablePagination-root': {
            color: theme.palette.text.primary, // สีตัวเลข pagination
          },
        }}
      />
    </Paper>
  );
}
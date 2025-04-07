import { Drawer, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { Info } from '@mui/icons-material';
import DataSidebarContent from './DataSidebarContent';

export default function DataSidebar ({ sidebarOpen, setSidebarOpen, quickFactData, isLoading, error }) {
  return (
    <Drawer
      anchor="right"
      open={sidebarOpen}
      onClose={() => setSidebarOpen(false)}
      PaperProps={{ sx: { width: 400, p: 3 } }}
    >
      {isLoading ? (
        <div className="loading-spinner">Loading...</div>
      ) : error ? (
        <Typography color="error">{error}</Typography>
      ) : quickFactData && (
        <DataSidebarContent facts={quickFactData.facts} location_id={quickFactData.location_id} location_name={quickFactData.location_name}/>
      )}
    </Drawer>
  );
};
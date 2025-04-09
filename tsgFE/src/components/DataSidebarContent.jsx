import React from 'react';
import { 
  Box,
  Paper,
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Typography,
  Chip,
  Tooltip,
  IconButton
} from '@mui/material';
import { Info, LocationOn, Map, Flag } from '@mui/icons-material';

export default function DataSidebarContent({ 
  location_id, 
  location_name, 
  setCountyGeoJson,
  facts = [], 
  enclosingStates = [], 
  enclosingCounties = [],
}) {
  return (
    <Box sx={{ p: 2 }}>
      {/* Header Section */}
      <Paper elevation={0} sx={{ 
        p: 2, 
        mb: 2,
        bgcolor: 'grey.100', // Light grey background
        borderLeft: '4px solid',
        borderColor: 'grey.400'
      }}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <LocationOn fontSize="small" sx={{ color: 'grey.700' }} />
          <Typography variant="h6" component="div" sx={{ color: 'grey.900' }}>
            {location_name}
          </Typography>
        </Box>
        <Box display="flex" alignItems="center" gap={1}>
          <Flag fontSize="small" sx={{ color: 'grey.700' }} />
          <Typography variant="subtitle2" sx={{ color: 'grey.700' }}>
            FIPS: <Chip label={location_id} size="small" sx={{ bgcolor: 'grey.200' }} />
          </Typography>
        </Box>
      </Paper>

      <Typography variant="subtitle1" gutterBottom sx={{ mt: 2, color: 'grey.800' }}>
        Demographic Facts
        <Tooltip title="Data from US Census Bureau">
          <IconButton size="small" sx={{ ml: 1, color: 'grey.600' }}>
            <Info fontSize="small" />
          </IconButton>
        </Tooltip>
      </Typography>
      <TableContainer component={Paper} sx={{ mb: 3, border: '1px solid', borderColor: 'grey.300' }}>
        <Table size="small">
          <TableHead>
            <TableRow sx={{ bgcolor: 'grey.100' }}>
              <TableCell sx={{ fontWeight: 'bold', color: 'grey.800' }}>Metric</TableCell>
              <TableCell align="right" sx={{ fontWeight: 'bold', color: 'grey.800' }}>Value</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {facts.map((fact, index) => (
              <TableRow 
                key={index} 
                hover
                sx={{ '&:nth-of-type(odd)': { bgcolor: 'grey.50' } }}
              >
                <TableCell sx={{ color: 'grey.800' }}>{fact.fact_name}</TableCell>
                <TableCell align="right" sx={{ fontFamily: 'Monospace', color: 'grey.900' }}>
                  {fact.fact_value}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Enclosing Areas Section */}
      <Box sx={{ mt: 3 }}>
        <Typography variant="subtitle1" gutterBottom sx={{ color: 'grey.800' }}>
          Enclosing Areas
          <Tooltip title="Geographic hierarchy">
            <IconButton size="small" sx={{ ml: 1, color: 'grey.600' }}>
              <Map fontSize="small" />
            </IconButton>
          </Tooltip>
        </Typography>

        {/* States */}
        {enclosingStates.length > 0 && (
          <>
            <Typography variant="subtitle2" sx={{ mt: 1, color: 'grey.600' }}>
              States ({enclosingStates.length})
            </Typography>
            <Box sx={{ 
              display: 'flex', 
              flexWrap: 'wrap', 
              gap: 1, 
              mt: 1, 
              mb: 2,
              '& .MuiChip-root': {
                borderColor: 'grey.300',
                color: 'grey.800'
              }
            }}>
              {enclosingStates.map((state, index) => (
                <Chip 
                  key={index}
                  label={state.name}
                  size="small"
                  variant="outlined"
                />
              ))}
            </Box>
          </>
        )}

        {/* Counties */}
        {enclosingCounties.length > 0 && (
          <>
            <Typography variant="subtitle2" sx={{ mt: 1, color: 'grey.600' }}>
              Counties ({enclosingCounties.length})
            </Typography>
            <Box sx={{ 
              display: 'flex', 
              flexWrap: 'wrap', 
              gap: 1, 
              mt: 1,
              '& .MuiChip-root': {
                borderColor: 'grey.300',
                color: 'grey.900'
              }
            }}>
              {enclosingCounties.map((county, index) => (
                <Chip 
                  key={index}
                  label={county.name}
                  size="small"
                  variant="outlined"
                  onMouseEnter={() => setCountyGeoJson(county.geometry)}
                  onMouseLeave={() => setCountyGeoJson(null)}
                  sx={{
                    borderColor: 'grey.300',
                    color: 'grey.900',
                    '&:hover': {
                      backgroundColor: '#1976d2', // Blue color
                      color: '#fff', // White text
                      borderColor: '#1976d2' // Blue border
                    }
                  }}
                />
              ))}
            </Box>
          </>
        )}

        {enclosingStates.length === 0 && enclosingCounties.length === 0 && (
          <Typography variant="body2" sx={{ color: 'grey.600', fontStyle: 'italic' }}>
            No enclosing areas found
          </Typography>
        )}
      </Box>
    </Box>
  );
}
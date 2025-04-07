import React from 'react'
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { Info } from '@mui/icons-material';

export default function DataSidebarContent({location_id, location_name, facts}) {
  return (
    <>
        <div className="sidebar-header">
            <Info color="primary" />
            <Typography variant="h6">
                Location: {location_name}
            </Typography>
            <Typography variant="h6">
                FIPS: {location_id}
            </Typography>
        </div>
        <TableContainer>
            <Table size="small">
                <TableHead>
                <TableRow>
                    <TableCell>Metric</TableCell>
                    <TableCell align="right">Value</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {facts.map((fact, index) => (
                    <TableRow key={index}>
                    <TableCell>{fact.fact_name}</TableCell>
                    <TableCell align="right">
                        {fact.fact_value}
                    </TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
        </TableContainer>
    </>
  )
}

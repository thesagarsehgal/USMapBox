import { Button, Select, MenuItem, Typography } from '@mui/material';
import { RestartAlt } from '@mui/icons-material';

export default function MapControls({ boundaryType, setBoundaryType, resetView, center, zoom }) {
  return (
	<div className="control-panel">
		<Button
			variant="contained"
			startIcon={<RestartAlt />}
			onClick={resetView}
			className='reset-button'
		>
			Reset View
		</Button>
		
		<Select
			value={boundaryType}
			onChange={(e) => setBoundaryType(e.target.value)}
			size="small"
			className='dropdown'
		>
			<MenuItem value="state">State Boundaries</MenuItem>
			<MenuItem value="county">County Boundaries</MenuItem>
		</Select>

		<div className="coordinates-display">
			<Typography variant="caption">
				Longitude: {center[0].toFixed(4)}<br />
				Latitude: {center[1].toFixed(4)}<br />
				Zoom: {zoom.toFixed(2)}
			</Typography>
		</div>
	</div>
  );
};

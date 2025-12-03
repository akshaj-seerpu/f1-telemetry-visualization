"""Data processing module for normalizing and preparing race data for replay."""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
import logging
from scipy.interpolate import interp1d

from backend.utils.constants import TELEMETRY_FREQUENCY, INTERPOLATION_METHOD

logger = logging.getLogger(__name__)


class RaceDataProcessor:
    """Processes race data for smooth replay visualization."""
    
    def __init__(self, session):
        """Initialize processor with a FastF1 session."""
        self.session = session
        self.laps = session.laps
        self.drivers = session.drivers
        
    def create_timeline(self) -> np.ndarray:
        """
        Create a unified timeline for the entire race.
        
        Returns:
            Array of timestamps in seconds
        """
        # Get race start and end times
        all_telemetry = []
        
        for driver in self.drivers:
            driver_laps = self.laps.pick_driver(driver)
            if not driver_laps.empty:
                for idx, lap in driver_laps.iterrows():
                    try:
                        telemetry = lap.get_telemetry()
                        if not telemetry.empty and 'Time' in telemetry.columns:
                            all_telemetry.append(telemetry['Time'])
                    except:
                        continue
        
        if not all_telemetry:
            return np.array([])
        
        # Find min and max times
        min_time = min(tel.min() for tel in all_telemetry if len(tel) > 0)
        max_time = max(tel.max() for tel in all_telemetry if len(tel) > 0)
        
        # Create timeline with specified frequency
        duration = (max_time - min_time).total_seconds()
        num_points = int(duration * TELEMETRY_FREQUENCY)
        
        timeline = np.linspace(0, duration, num_points)
        
        logger.info(f"Created timeline: {duration:.1f}s, {num_points} points")
        return timeline, min_time
    
    def interpolate_driver_data(
        self, 
        driver_number: str, 
        timeline: np.ndarray,
        race_start_time
    ) -> Optional[Dict[str, np.ndarray]]:
        """
        Interpolate driver position and telemetry data for the timeline.
        
        Args:
            driver_number: Driver number
            timeline: Timeline array in seconds
            race_start_time: Race start timestamp
        
        Returns:
            Dictionary with interpolated data arrays
        """
        try:
            driver_laps = self.laps.pick_driver(driver_number)
            if driver_laps.empty:
                return None
            
            # Collect all telemetry data for this driver
            all_data = []
            
            for idx, lap in driver_laps.iterrows():
                try:
                    telemetry = lap.get_telemetry()
                    if not telemetry.empty:
                        all_data.append(telemetry)
                except:
                    continue
            
            if not all_data:
                return None
            
            # Combine all telemetry
            combined = pd.concat(all_data, ignore_index=True)
            combined = combined.sort_values('Time')
            
            # Convert time to seconds from race start
            time_seconds = np.array([
                (t - race_start_time).total_seconds() 
                for t in combined['Time']
            ])
            
            # Interpolate position data
            interpolated = {
                'time': timeline,
            }
            
            # Interpolate X, Y positions
            if 'X' in combined.columns and 'Y' in combined.columns:
                x_interp = interp1d(
                    time_seconds, 
                    combined['X'].values, 
                    kind=INTERPOLATION_METHOD,
                    bounds_error=False,
                    fill_value='extrapolate'
                )
                y_interp = interp1d(
                    time_seconds, 
                    combined['Y'].values, 
                    kind=INTERPOLATION_METHOD,
                    bounds_error=False,
                    fill_value='extrapolate'
                )
                
                interpolated['x'] = x_interp(timeline)
                interpolated['y'] = y_interp(timeline)
            
            # Interpolate speed
            if 'Speed' in combined.columns:
                speed_interp = interp1d(
                    time_seconds,
                    combined['Speed'].fillna(0).values,
                    kind='linear',
                    bounds_error=False,
                    fill_value=0
                )
                interpolated['speed'] = speed_interp(timeline)
            
            # Interpolate gear (use nearest neighbor)
            if 'nGear' in combined.columns:
                gear_interp = interp1d(
                    time_seconds,
                    combined['nGear'].fillna(0).values,
                    kind='nearest',
                    bounds_error=False,
                    fill_value=0
                )
                interpolated['gear'] = gear_interp(timeline).astype(int)
            
            # Interpolate DRS
            if 'DRS' in combined.columns:
                drs_interp = interp1d(
                    time_seconds,
                    combined['DRS'].fillna(0).values,
                    kind='nearest',
                    bounds_error=False,
                    fill_value=0
                )
                interpolated['drs'] = drs_interp(timeline).astype(int)
            
            return interpolated
            
        except Exception as e:
            logger.error(f"Error interpolating driver {driver_number}: {e}")
            return None
    
    def process_race_data(self) -> Dict[str, Any]:
        """
        Process complete race data for all drivers.
        
        Returns:
            Dictionary with processed race data
        """
        logger.info("Processing race data...")
        
        # Create timeline
        timeline, race_start = self.create_timeline()
        
        if len(timeline) == 0:
            logger.error("Failed to create timeline")
            return {}
        
        # Process each driver
        drivers_data = {}
        
        for driver_number in self.drivers:
            driver_info = self.session.get_driver(driver_number)
            driver_data = self.interpolate_driver_data(driver_number, timeline, race_start)
            
            if driver_data:
                drivers_data[str(driver_number)] = {
                    'abbreviation': driver_info['Abbreviation'],
                    'full_name': f"{driver_info['FirstName']} {driver_info['LastName']}",
                    'team': driver_info['TeamName'],
                    'team_color': driver_info.get('TeamColor', '#FFFFFF'),
                    'telemetry': driver_data
                }
        
        logger.info(f"Processed data for {len(drivers_data)} drivers")
        
        return {
            'timeline': timeline.tolist(),
            'drivers': drivers_data,
            'total_frames': len(timeline),
            'duration': float(timeline[-1]) if len(timeline) > 0 else 0,
        }
    
    def get_leaderboard_at_time(self, time_index: int) -> List[Dict[str, Any]]:
        """
        Get leaderboard positions at a specific time index.
        
        Args:
            time_index: Index in the timeline
        
        Returns:
            List of driver positions sorted by race order
        """
        # This is a simplified version - in reality, you'd need lap counting logic
        # For now, we'll return drivers in order
        leaderboard = []
        
        for driver_number in self.drivers:
            driver_info = self.session.get_driver(driver_number)
            leaderboard.append({
                'position': len(leaderboard) + 1,
                'driver_number': driver_number,
                'abbreviation': driver_info['Abbreviation'],
                'team': driver_info['TeamName'],
            })
        
        return leaderboard

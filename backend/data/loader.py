"""Data loading module for fetching F1 race data using FastF1."""

import fastf1
import pandas as pd
from pathlib import Path
from typing import Optional, Dict, Any
import logging

from backend.utils.constants import CACHE_DIR, CACHE_ENABLED

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class F1DataLoader:
    """Handles loading and caching of F1 race data."""
    
    def __init__(self, cache_dir: str = CACHE_DIR):
        """Initialize the data loader with cache directory."""
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        if CACHE_ENABLED:
            fastf1.Cache.enable_cache(str(self.cache_dir))
            logger.info(f"FastF1 cache enabled at: {self.cache_dir}")
    
    def load_session(
        self, 
        year: int, 
        gp: str, 
        session_type: str = "R"
    ) -> Optional[fastf1.core.Session]:
        """
        Load a specific F1 session.
        
        Args:
            year: Year of the race
            gp: Grand Prix name or round number
            session_type: Session type (R=Race, Q=Qualifying, FP1/FP2/FP3=Practice)
        
        Returns:
            FastF1 Session object or None if loading fails
        """
        try:
            logger.info(f"Loading {year} {gp} {session_type}")
            session = fastf1.get_session(year, gp, session_type)
            session.load()
            logger.info(f"Successfully loaded session: {session.event['EventName']}")
            return session
        except Exception as e:
            logger.error(f"Error loading session: {e}")
            return None
    
    def get_available_races(self, year: int) -> list:
        """
        Get list of available races for a given year.
        
        Args:
            year: Year to get races for
        
        Returns:
            List of race information dictionaries
        """
        try:
            schedule = fastf1.get_event_schedule(year)
            races = []
            
            for idx, event in schedule.iterrows():
                if pd.notna(event['EventDate']):
                    races.append({
                        'round': int(event['RoundNumber']),
                        'name': event['EventName'],
                        'location': event['Location'],
                        'country': event['Country'],
                        'date': event['EventDate'].strftime('%Y-%m-%d')
                    })
            
            return races
        except Exception as e:
            logger.error(f"Error getting race schedule: {e}")
            return []
    
    def get_session_info(self, session: fastf1.core.Session) -> Dict[str, Any]:
        """
        Extract session information.
        
        Args:
            session: FastF1 Session object
        
        Returns:
            Dictionary with session information
        """
        return {
            'event_name': session.event['EventName'],
            'location': session.event['Location'],
            'country': session.event['Country'],
            'date': session.event['EventDate'].strftime('%Y-%m-%d'),
            'session_type': session.name,
            'total_laps': int(session.total_laps) if hasattr(session, 'total_laps') and session.total_laps is not None else 0,
        }
    
    def get_drivers_info(self, session: fastf1.core.Session) -> list:
        """
        Get information about all drivers in the session.
        
        Args:
            session: FastF1 Session object
        
        Returns:
            List of driver information dictionaries
        """
        drivers = []
        
        for driver_number in session.drivers:
            driver = session.get_driver(driver_number)
            drivers.append({
                'number': driver_number,
                'abbreviation': driver['Abbreviation'],
                'full_name': f"{driver['FirstName']} {driver['LastName']}",
                'team': driver['TeamName'],
                'team_color': driver['TeamColor'] if 'TeamColor' in driver else '#FFFFFF',
            })
        
        return drivers
    
    def get_track_data(self, session: fastf1.core.Session) -> Optional[Dict[str, Any]]:
        """
        Get track layout data.
        
        Args:
            session: FastF1 Session object
        
        Returns:
            Dictionary with track coordinates and information
        """
        try:
            # Get a lap to extract track position data
            laps = session.laps
            if laps.empty:
                return None
            
            # Get the fastest lap for track reference
            fastest_lap = laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()
            
            if telemetry.empty:
                return None
            
            return {
                'x': telemetry['X'].tolist(),
                'y': telemetry['Y'].tolist(),
                'circuit_key': session.event.get('CircuitKey', 'unknown'),
            }
        except Exception as e:
            logger.error(f"Error getting track data: {e}")
            return None

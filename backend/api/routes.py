"""API routes for the F1 Race Replay application."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging

from backend.data.loader import F1DataLoader
from backend.data.processor import RaceDataProcessor

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# Global data loader instance
data_loader = F1DataLoader()

# Cache for processed race data
race_data_cache = {}


@router.get("/races/{year}")
async def get_races(year: int) -> List[Dict[str, Any]]:
    """
    Get list of available races for a given year.
    
    Args:
        year: Year to get races for
    
    Returns:
        List of race information
    """
    try:
        races = data_loader.get_available_races(year)
        return races
    except Exception as e:
        logger.error(f"Error getting races: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{year}/{gp}/{session_type}")
async def get_session_info(year: int, gp: str, session_type: str = "R") -> Dict[str, Any]:
    """
    Get session information without loading full telemetry.
    
    Args:
        year: Year of the race
        gp: Grand Prix name or round number
        session_type: Session type (R, Q, FP1, FP2, FP3)
    
    Returns:
        Session information
    """
    try:
        session = data_loader.load_session(year, gp, session_type)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_info = data_loader.get_session_info(session)
        drivers_info = data_loader.get_drivers_info(session)
        
        return {
            'session': session_info,
            'drivers': drivers_info,
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting session info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/race-data/{year}/{gp}/{session_type}")
async def get_race_data(year: int, gp: str, session_type: str = "R") -> Dict[str, Any]:
    """
    Load and process complete race data for replay.
    
    Args:
        year: Year of the race
        gp: Grand Prix name or round number
        session_type: Session type
    
    Returns:
        Processed race data with timeline and driver telemetry
    """
    cache_key = f"{year}_{gp}_{session_type}"
    
    # Check cache first
    if cache_key in race_data_cache:
        logger.info(f"Returning cached data for {cache_key}")
        return race_data_cache[cache_key]
    
    try:
        # Load session
        session = data_loader.load_session(year, gp, session_type)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get session info
        session_info = data_loader.get_session_info(session)
        drivers_info = data_loader.get_drivers_info(session)
        track_data = data_loader.get_track_data(session)
        
        # Process race data
        processor = RaceDataProcessor(session)
        race_data = processor.process_race_data()
        
        # Combine all data
        result = {
            'session': session_info,
            'drivers_info': drivers_info,
            'track': track_data,
            'race_data': race_data,
        }
        
        # Cache the result
        race_data_cache[cache_key] = result
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing race data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/track/{year}/{gp}")
async def get_track_layout(year: int, gp: str) -> Dict[str, Any]:
    """
    Get track layout data.
    
    Args:
        year: Year of the race
        gp: Grand Prix name or round number
    
    Returns:
        Track coordinates and information
    """
    try:
        session = data_loader.load_session(year, gp, "R")
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        track_data = data_loader.get_track_data(session)
        if not track_data:
            raise HTTPException(status_code=404, detail="Track data not available")
        
        return track_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting track layout: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "F1 Race Replay API"}

"""WebSocket handlers for real-time race replay streaming."""

from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class ReplayManager:
    """Manages race replay streaming via WebSocket."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.replay_tasks: Dict[str, asyncio.Task] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection."""
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection."""
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        if client_id in self.replay_tasks:
            self.replay_tasks[client_id].cancel()
            del self.replay_tasks[client_id]
        logger.info(f"Client {client_id} disconnected")
    
    async def send_message(self, client_id: str, message: Dict[str, Any]):
        """Send a message to a specific client."""
        if client_id in self.active_connections:
            try:
                await self.active_connections[client_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending message to {client_id}: {e}")
    
    async def stream_replay(
        self, 
        client_id: str, 
        race_data: Dict[str, Any],
        playback_speed: float = 1.0
    ):
        """
        Stream race replay data frame by frame.
        
        Args:
            client_id: Client identifier
            race_data: Processed race data
            playback_speed: Playback speed multiplier
        """
        try:
            timeline = race_data['race_data']['timeline']
            drivers = race_data['race_data']['drivers']
            total_frames = len(timeline)
            
            logger.info(f"Starting replay stream for {client_id}, {total_frames} frames")
            
            for frame_idx in range(total_frames):
                # Check if client is still connected
                if client_id not in self.active_connections:
                    break
                
                # Prepare frame data
                frame_data = {
                    'type': 'frame',
                    'frame_index': frame_idx,
                    'time': timeline[frame_idx],
                    'drivers': {}
                }
                
                # Add driver data for this frame
                for driver_num, driver_data in drivers.items():
                    telemetry = driver_data['telemetry']
                    
                    if frame_idx < len(telemetry['time']):
                        frame_data['drivers'][driver_num] = {
                            'abbreviation': driver_data['abbreviation'],
                            'team': driver_data['team'],
                            'team_color': driver_data['team_color'],
                            'x': float(telemetry['x'][frame_idx]) if 'x' in telemetry else 0,
                            'y': float(telemetry['y'][frame_idx]) if 'y' in telemetry else 0,
                            'speed': float(telemetry['speed'][frame_idx]) if 'speed' in telemetry else 0,
                            'gear': int(telemetry['gear'][frame_idx]) if 'gear' in telemetry else 0,
                            'drs': int(telemetry['drs'][frame_idx]) if 'drs' in telemetry else 0,
                        }
                
                # Send frame
                await self.send_message(client_id, frame_data)
                
                # Calculate delay based on playback speed
                # Assuming 10 Hz data (0.1s between frames)
                delay = 0.1 / playback_speed
                await asyncio.sleep(delay)
            
            # Send completion message
            await self.send_message(client_id, {
                'type': 'replay_complete',
                'message': 'Replay finished'
            })
            
            logger.info(f"Replay stream completed for {client_id}")
            
        except asyncio.CancelledError:
            logger.info(f"Replay stream cancelled for {client_id}")
        except Exception as e:
            logger.error(f"Error in replay stream for {client_id}: {e}")
            await self.send_message(client_id, {
                'type': 'error',
                'message': str(e)
            })


# Global replay manager instance
replay_manager = ReplayManager()


async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket endpoint for race replay streaming.
    
    Args:
        websocket: WebSocket connection
        client_id: Unique client identifier
    """
    await replay_manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_json()
            message_type = data.get('type')
            
            if message_type == 'ping':
                await replay_manager.send_message(client_id, {'type': 'pong'})
            
            elif message_type == 'start_replay':
                # Start replay streaming
                race_data = data.get('race_data')
                playback_speed = data.get('playback_speed', 1.0)
                
                if race_data:
                    # Cancel any existing replay task
                    if client_id in replay_manager.replay_tasks:
                        replay_manager.replay_tasks[client_id].cancel()
                    
                    # Start new replay task
                    task = asyncio.create_task(
                        replay_manager.stream_replay(client_id, race_data, playback_speed)
                    )
                    replay_manager.replay_tasks[client_id] = task
            
            elif message_type == 'stop_replay':
                # Stop replay streaming
                if client_id in replay_manager.replay_tasks:
                    replay_manager.replay_tasks[client_id].cancel()
                    del replay_manager.replay_tasks[client_id]
            
    except WebSocketDisconnect:
        replay_manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for {client_id}: {e}")
        replay_manager.disconnect(client_id)

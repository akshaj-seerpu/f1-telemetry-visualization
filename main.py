"""Main entry point for the F1 Race Replay FastAPI application."""

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

from backend.api.routes import router
from backend.api.websocket import websocket_endpoint
from backend.utils.constants import HOST, PORT, APP_NAME, APP_VERSION

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Interactive F1 race replay visualization with real-time telemetry"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.websocket("/ws/replay/{client_id}")
async def websocket_replay(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for race replay streaming."""
    await websocket_endpoint(websocket, client_id)


if __name__ == "__main__":
    logger.info(f"Starting {APP_NAME} v{APP_VERSION}")
    logger.info(f"Server running on http://{HOST}:{PORT}")
    logger.info(f"API documentation available at http://{HOST}:{PORT}/docs")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,
        log_level="info"
    )

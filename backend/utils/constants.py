"""Configuration constants for the F1 Race Replay application."""

# Application settings
APP_NAME = "F1 Race Replay"
APP_VERSION = "1.0.0"

# Server settings
HOST = "0.0.0.0"
PORT = 8000

# Cache settings
CACHE_DIR = "cache"
CACHE_ENABLED = True

# Playback settings
DEFAULT_FPS = 60
PLAYBACK_SPEEDS = [0.5, 1.0, 2.0, 4.0, 8.0]
DEFAULT_SPEED = 1.0

# Data settings
TELEMETRY_FREQUENCY = 10  # Hz
INTERPOLATION_METHOD = "linear"

# Track rendering
TRACK_SCALE_FACTOR = 1.0
TRACK_MARGIN = 50  # pixels

# Driver marker settings
DRIVER_MARKER_SIZE = 10  # pixels
DRIVER_MARKER_OUTLINE = 2  # pixels

# UI settings
LEADERBOARD_MAX_DRIVERS = 20
TELEMETRY_UPDATE_INTERVAL = 100  # ms

# WebSocket settings
WS_HEARTBEAT_INTERVAL = 30  # seconds
WS_MESSAGE_QUEUE_SIZE = 100

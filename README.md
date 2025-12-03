# F1 Race Replay - Telemetry Visualization

An interactive web application for visualizing Formula 1 race replays with real-time telemetry data, driver positions, and race statistics.

## Features

- 🏎️ Real-time race replay visualization
- 📊 Live telemetry data (speed, gear, DRS status)
- 🏁 Interactive leaderboard with driver positions
- ⏯️ Playback controls (play/pause, speed adjustment)
- 🎨 Team colors and tyre compound visualization
- 📡 WebSocket-based real-time updates

## Tech Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **FastF1**: Official F1 data API
- **WebSockets**: Real-time data streaming

### Frontend
- **React**: Modern UI framework
- **TailwindCSS**: Utility-first styling
- **Lucide Icons**: Beautiful icon set
- **Canvas API**: Track and driver visualization

## Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
python main.py
```

The backend will start on `http://localhost:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will start on `http://localhost:3000`

## Usage

1. Start the backend server
2. Start the frontend development server
3. Open your browser to `http://localhost:3000`
4. Select a race (year, grand prix, session)
5. Watch the race replay with interactive controls

## Project Structure

```
f1-telemetry-visualization/
├── main.py                 # FastAPI entry point
├── backend/
│   ├── data/
│   │   ├── loader.py      # FastF1 data fetching
│   │   └── processor.py   # Data processing & normalization
│   ├── api/
│   │   ├── routes.py      # API endpoints
│   │   └── websocket.py   # WebSocket handlers
│   └── utils/
│       ├── colors.py      # Team colors
│       └── constants.py   # Configuration
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   └── utils/         # Utilities
│   └── public/
└── cache/                 # FastF1 data cache
```

## API Endpoints

- `GET /api/races` - List available races
- `GET /api/race/{year}/{gp}` - Get race data
- `WS /ws/replay` - WebSocket for race replay stream

## Development

### Running Tests
```bash
# Backend tests
pytest

# Frontend tests
cd frontend && npm test
```

### Building for Production
```bash
# Build frontend
cd frontend && npm run build

# The built files will be in frontend/build/
```

## License

MIT

## Acknowledgments

- FastF1 for providing F1 data
- Formula 1 for the amazing sport

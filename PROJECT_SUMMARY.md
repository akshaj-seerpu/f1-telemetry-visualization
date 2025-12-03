# F1 Race Replay - Project Summary

## Overview

F1 Race Replay is a full-stack web application that provides interactive visualization of Formula 1 race replays with real-time telemetry data, driver positions, and race statistics.

## Architecture

### Technology Stack

**Backend:**
- FastAPI (Python web framework)
- FastF1 (F1 data API)
- WebSockets (real-time streaming)
- NumPy & Pandas (data processing)
- SciPy (interpolation)

**Frontend:**
- React 18
- Canvas API (track rendering)
- Lucide Icons
- Axios (HTTP client)
- WebSocket client

### System Design

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   React     │ ◄─────► │   FastAPI    │ ◄─────► │   FastF1    │
│  Frontend   │  HTTP   │   Backend    │  API    │     API     │
│             │  WS     │              │         │             │
└─────────────┘         └──────────────┘         └─────────────┘
      │                        │
      │                        │
      ▼                        ▼
┌─────────────┐         ┌──────────────┐
│   Browser   │         │    Cache     │
│   Canvas    │         │  (FastF1)    │
└─────────────┘         └──────────────┘
```

## Features Implemented

### ✅ Core Features

1. **Race Data Loading**
   - FastF1 integration for official F1 data
   - Support for multiple years (2015-2024)
   - All Grand Prix events
   - Multiple session types (Race, Qualifying, Practice)
   - Intelligent caching system

2. **Track Visualization**
   - Accurate track layouts from telemetry data
   - Auto-scaling to fit viewport
   - Smooth rendering with Canvas API
   - Driver position markers with team colors

3. **Real-time Telemetry**
   - Speed (km/h)
   - Gear position
   - DRS status
   - Track position (X, Y coordinates)

4. **Interactive Leaderboard**
   - Live driver positions
   - Team colors
   - Driver abbreviations
   - Click to select driver

5. **Playback Controls**
   - Play/Pause functionality
   - Multiple playback speeds (0.5x - 8.0x)
   - Progress bar
   - Frame counter
   - Keyboard shortcuts

6. **Race Information Display**
   - Event name and location
   - Session type
   - Race date
   - Elapsed time

### 🔧 Technical Features

1. **Data Processing Pipeline**
   - Timeline normalization
   - Position interpolation (linear)
   - Telemetry data smoothing
   - Frame-by-frame data generation

2. **WebSocket Streaming**
   - Real-time frame updates
   - Adjustable playback speed
   - Connection management
   - Error handling

3. **API Endpoints**
   - `/api/races/{year}` - List races
   - `/api/session/{year}/{gp}/{session}` - Session info
   - `/api/race-data/{year}/{gp}/{session}` - Full race data
   - `/api/track/{year}/{gp}` - Track layout
   - `/ws/replay/{client_id}` - WebSocket stream

4. **Caching System**
   - FastF1 data caching
   - Processed race data caching
   - Significant performance improvement

## Project Structure

```
f1-telemetry-visualization/
├── main.py                      # FastAPI application entry
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview
├── SETUP.md                     # Detailed setup guide
├── PROJECT_SUMMARY.md          # This file
├── LICENSE                      # MIT License
├── .gitignore                   # Git ignore rules
│
├── backend/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py           # FastF1 data loading
│   │   └── processor.py        # Data processing & normalization
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py           # REST API endpoints
│   │   └── websocket.py        # WebSocket handlers
│   └── utils/
│       ├── __init__.py
│       ├── colors.py           # Team colors & utilities
│       └── constants.py        # Configuration constants
│
├── frontend/
│   ├── package.json            # Node dependencies
│   ├── public/
│   │   └── index.html          # HTML template
│   └── src/
│       ├── index.js            # React entry point
│       ├── index.css           # Global styles
│       ├── App.js              # Main app component
│       ├── App.css             # App styles
│       ├── hooks/
│       │   ├── useRaceData.js  # Race data management
│       │   └── useWebSocket.js # WebSocket connection
│       └── components/
│           ├── RaceSelector.js      # Race selection UI
│           ├── RaceSelector.css
│           ├── TrackView.js         # Track visualization
│           ├── TrackView.css
│           ├── Leaderboard.js       # Driver leaderboard
│           ├── Leaderboard.css
│           ├── TelemetryPanel.js    # Telemetry display
│           ├── TelemetryPanel.css
│           ├── PlaybackControls.js  # Playback UI
│           ├── PlaybackControls.css
│           ├── RaceInfo.js          # Race information
│           └── RaceInfo.css
│
├── cache/                       # FastF1 data cache (gitignored)
│
└── scripts/
    ├── start_backend.sh        # Backend startup (Linux/Mac)
    ├── start_frontend.sh       # Frontend startup (Linux/Mac)
    ├── start_backend.bat       # Backend startup (Windows)
    └── start_frontend.bat      # Frontend startup (Windows)
```

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- 4GB+ RAM
- Internet connection

### Installation

```bash
# Clone repository
git clone https://github.com/akshaj-seerpu/f1-telemetry-visualization.git
cd f1-telemetry-visualization

# Backend setup
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend setup
cd frontend
npm install
cp .env.example .env
```

### Running

**Terminal 1 - Backend:**
```bash
./start_backend.sh  # or start_backend.bat on Windows
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh  # or start_frontend.bat on Windows
```

Access the app at `http://localhost:3000`

## Data Flow

1. **User selects race** → Frontend sends request to backend
2. **Backend loads data** → FastF1 API (cached if available)
3. **Data processing** → Timeline normalization, interpolation
4. **WebSocket connection** → Established between frontend and backend
5. **Frame streaming** → Backend sends frame-by-frame data
6. **Visualization** → Frontend renders track and drivers
7. **User interaction** → Select drivers, control playback

## Performance Considerations

### Backend
- Data caching reduces API calls
- Interpolation creates smooth 10Hz timeline
- WebSocket streaming for efficient updates
- Async processing with FastAPI

### Frontend
- Canvas API for efficient rendering
- Component memoization
- Debounced updates
- Optimized re-renders

## Known Limitations

1. **First Load Time**: Initial race load can take 2-5 minutes for data download
2. **Data Availability**: Older races may have incomplete telemetry
3. **Memory Usage**: Large races (24+ drivers) require more RAM
4. **Browser Performance**: Canvas rendering may vary by browser

## Future Enhancements

### Planned Features
- [ ] Lap-by-lap position tracking
- [ ] Pit stop visualization
- [ ] Tire compound changes
- [ ] Sector times
- [ ] Gap to leader/ahead
- [ ] Multiple camera views
- [ ] Race highlights markers
- [ ] Export to video
- [ ] Comparison mode (2 drivers)
- [ ] Weather data overlay

### Technical Improvements
- [ ] Database for processed data
- [ ] Redis caching layer
- [ ] Docker containerization
- [ ] Production deployment guide
- [ ] Unit tests
- [ ] Integration tests
- [ ] Performance profiling
- [ ] Mobile responsive design

## API Documentation

### REST Endpoints

**GET /api/races/{year}**
- Returns list of available races for the year
- Response: `[{round, name, location, country, date}, ...]`

**GET /api/session/{year}/{gp}/{session_type}**
- Returns session information
- Response: `{session: {...}, drivers: [...]}`

**GET /api/race-data/{year}/{gp}/{session_type}**
- Returns complete processed race data
- Response: `{session, drivers_info, track, race_data}`

**GET /api/track/{year}/{gp}**
- Returns track layout coordinates
- Response: `{x: [...], y: [...], circuit_key}`

### WebSocket Protocol

**Connection:** `ws://localhost:8000/ws/replay/{client_id}`

**Client Messages:**
```json
{
  "type": "start_replay",
  "race_data": {...},
  "playback_speed": 1.0
}
```

**Server Messages:**
```json
{
  "type": "frame",
  "frame_index": 0,
  "time": 0.0,
  "drivers": {
    "1": {
      "abbreviation": "VER",
      "team": "Red Bull Racing",
      "team_color": "#3671C6",
      "x": 1234.5,
      "y": 5678.9,
      "speed": 287.3,
      "gear": 7,
      "drs": 1
    }
  }
}
```

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - See LICENSE file

## Acknowledgments

- **FastF1** - Official F1 data API
- **Formula 1** - For the sport
- **React** - Frontend framework
- **FastAPI** - Backend framework

## Contact

For issues, questions, or suggestions:
- GitHub Issues: https://github.com/akshaj-seerpu/f1-telemetry-visualization/issues
- FastF1 Docs: https://docs.fastf1.dev/

---

**Built with ❤️ for F1 fans**

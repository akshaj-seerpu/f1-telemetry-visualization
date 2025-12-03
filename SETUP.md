# F1 Race Replay - Setup Guide

This guide will help you set up and run the F1 Race Replay application.

## Prerequisites

### Required Software
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Node.js 16+**: [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js) or **yarn**
- **Git**: [Download Git](https://git-scm.com/)

### System Requirements
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: At least 2GB free space for cache
- **Internet**: Required for initial data download

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/akshaj-seerpu/f1-telemetry-visualization.git
cd f1-telemetry-visualization
```

### 2. Backend Setup

#### Install Python Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### Create Cache Directory

```bash
mkdir cache
```

### 3. Frontend Setup

#### Install Node Dependencies

```bash
cd frontend
npm install
```

#### Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# The default values should work for local development:
# REACT_APP_API_URL=http://localhost:8000
# REACT_APP_WS_URL=ws://localhost:8000
```

## Running the Application

### Start Backend Server

Open a terminal in the project root directory:

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Run the FastAPI server
python main.py
```

The backend will start on `http://localhost:8000`

You can access the API documentation at `http://localhost:8000/docs`

### Start Frontend Development Server

Open a **new terminal** and navigate to the frontend directory:

```bash
cd frontend
npm start
```

The frontend will start on `http://localhost:3000` and should automatically open in your browser.

## Using the Application

### 1. Select a Race

- Choose a **Year** (2015-2024)
- Select a **Grand Prix** from the dropdown
- Choose a **Session** (Race, Qualifying, or Practice)
- Click **Load Race**

### 2. First Load

⚠️ **Important**: The first time you load a race, it will take several minutes to download and process the data from the FastF1 API. Subsequent loads of the same race will be much faster due to caching.

### 3. Watch the Replay

Once loaded, you'll see:
- **Track View**: Overhead view of the circuit with driver positions
- **Leaderboard**: Current race positions
- **Telemetry Panel**: Detailed data for selected driver
- **Playback Controls**: Play/pause and speed controls

### 4. Interact with the Replay

- **Click on drivers** in the track view or leaderboard to view their telemetry
- **Use playback controls** to play/pause and adjust speed
- **Keyboard shortcuts**:
  - `SPACE`: Play/Pause
  - `←/→`: Decrease/Increase playback speed

## Troubleshooting

### Backend Issues

#### "Module not found" errors
```bash
# Make sure you're in the virtual environment
pip install -r requirements.txt
```

#### "FastF1 cache error"
```bash
# Clear the cache and try again
rm -rf cache/*
```

#### Port 8000 already in use
```bash
# Find and kill the process using port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

#### "npm install" fails
```bash
# Clear npm cache
npm cache clean --force
# Try again
npm install
```

#### Port 3000 already in use
The app will automatically try port 3001. Or you can specify a different port:
```bash
PORT=3001 npm start
```

#### Cannot connect to backend
- Make sure the backend server is running on `http://localhost:8000`
- Check the `.env` file has the correct API URL
- Check browser console for CORS errors

### Data Loading Issues

#### Race data not loading
- Check your internet connection
- Some older races may have incomplete data
- Try a different race or session
- Check backend logs for specific errors

#### Slow performance
- Close other applications to free up RAM
- Try reducing playback speed
- Some races with 24+ drivers may be more resource-intensive

## Development

### Project Structure

```
f1-telemetry-visualization/
├── main.py                    # FastAPI entry point
├── requirements.txt           # Python dependencies
├── backend/
│   ├── data/
│   │   ├── loader.py         # FastF1 data loading
│   │   └── processor.py      # Data processing
│   ├── api/
│   │   ├── routes.py         # REST API endpoints
│   │   └── websocket.py      # WebSocket handlers
│   └── utils/
│       ├── colors.py         # Team colors
│       └── constants.py      # Configuration
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── App.js            # Main app component
│   │   └── index.js          # Entry point
│   └── package.json
└── cache/                     # FastF1 data cache
```

### API Endpoints

- `GET /api/races/{year}` - List available races
- `GET /api/session/{year}/{gp}/{session_type}` - Get session info
- `GET /api/race-data/{year}/{gp}/{session_type}` - Load full race data
- `GET /api/track/{year}/{gp}` - Get track layout
- `WS /ws/replay/{client_id}` - WebSocket for race replay

### Building for Production

#### Backend
```bash
# The backend can be deployed using any ASGI server
uvicorn main:app --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm run build
# Built files will be in frontend/build/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
- Check the [GitHub Issues](https://github.com/akshaj-seerpu/f1-telemetry-visualization/issues)
- Review the FastF1 documentation: https://docs.fastf1.dev/

## License

MIT License - see LICENSE file for details

## Acknowledgments

- **FastF1**: For providing F1 data API
- **Formula 1**: For the amazing sport
- **React**: For the frontend framework
- **FastAPI**: For the backend framework

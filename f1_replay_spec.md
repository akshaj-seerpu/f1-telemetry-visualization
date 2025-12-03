# F1 Race Replay - Project Specification

## Project Overview

F1 Race Replay is an interactive Python application that visualizes Formula 1 race replays from an overhead perspective, providing users with a comprehensive view of race dynamics, driver positions, and telemetry data in real-time.

## Core Objectives

- Create an engaging, interactive race replay experience
- Visualize driver positions on accurate track layouts
- Display real-time telemetry and race statistics
- Provide intuitive playback controls
- Ensure smooth performance and responsive UI

## Technical Stack

### Primary Technologies
- **Language**: Python 3.8+
- **Data Source**: FastF1 (for race data, telemetry, and track information)
- **GUI Framework**: Arcade (2D graphics and animation)
- **Data Processing**: NumPy (for timeline normalization and calculations)

### Additional Libraries (as needed)
- **Pandas**: Data manipulation and preprocessing
- **Shapely**: Track geometry handling (if needed)
- **Pillow**: Image processing for textures/backgrounds

## Required Features

### 1. Race Replay Visualization
- **Track Rendering**: Display accurate track layout with proper scale
- **Driver Markers**: Show all drivers as distinct colored dots/cars on track
- **Position Updates**: Smooth interpolation between data points for fluid movement
- **Track Details**: Display track name, circuit layout, and key features

### 2. Leaderboard Display
- **Position Ranking**: Real-time driver positions (1st through last)
- **Driver Information**: 
  - Position number
  - Driver abbreviation/name
  - Team colors
  - Current tyre compound (Soft/Medium/Hard/Intermediate/Wet)
- **Status Indicators**: Mark retired drivers as "OUT"
- **Interactive Selection**: Click on drivers to view their telemetry

### 3. Race Information Panel
- **Current Lap**: Display current lap / total laps
- **Race Time**: Show elapsed race time (HH:MM:SS format)
- **Race Name**: Display Grand Prix name and year

### 4. Driver Telemetry Panel
- **Selected Driver Info**:
  - Current speed (km/h)
  - Current gear
  - DRS status (On/Off)
  - Current lap number
- **Update Frequency**: Real-time updates as race progresses

### 5. Playback Controls
- **Keyboard Shortcuts**:
  - `[SPACE]`: Pause/Resume playback
  - `[←] / [→]`: Rewind / Fast Forward
  - `[↑] / [↓]`: Increase / Decrease playback speed
  - Speed multipliers: 0.5x, 1x, 2x, 4x
- **Visual Indicators**: Show current playback speed and pause state

## Data Architecture

### Data Processing Pipeline

```
FastF1 Data → Raw Telemetry → Timeline Normalization → Frame-by-Frame Data → Rendering
```

#### Step 1: Data Acquisition
- Use FastF1 to fetch race session data
- Load lap timing, telemetry, position data, and tyre information
- Cache data locally to avoid repeated API calls

#### Step 2: Timeline Normalization
- Create a unified timeline for the entire race (second-by-second or sub-second)
- Interpolate driver positions between telemetry samples
- Calculate exact position, speed, gear, DRS status for each timestamp
- Track tyre compound changes and pit stops

#### Step 3: Frame Generation
- Convert normalized data into renderable frames
- Each frame contains:
  - All driver positions (x, y coordinates on track)
  - Current lap numbers
  - Race time
  - Leaderboard state
  - Driver-specific telemetry

#### Step 4: Track Rendering
- Use FastF1 track position data to create track layout
- Scale and center track for optimal viewing
- Add visual elements (start/finish line, DRS zones, pit lane)

## Implementation Guidelines

### Application Structure

```
f1_race_replay/
├── main.py                 # Entry point, Arcade window setup
├── data/
│   ├── loader.py          # FastF1 data fetching and caching
│   ├── processor.py       # Timeline normalization
│   └── cache/             # Cached race data
├── rendering/
│   ├── track.py           # Track rendering logic
│   ├── drivers.py         # Driver marker rendering
│   ├── leaderboard.py     # Leaderboard UI component
│   └── telemetry.py       # Telemetry panel component
├── controls/
│   └── playback.py        # Playback control logic
└── utils/
    ├── colors.py          # Team colors and themes
    └── constants.py       # Configuration constants
```

### Key Implementation Details

#### 1. Data Loading & Caching
- Implement caching mechanism to store processed race data
- Check cache before fetching from FastF1
- Allow user to select: Year, Grand Prix, Session (Race/Qualifying/Practice)

#### 2. Track Coordinate System
- Convert FastF1 position data (meters) to screen coordinates (pixels)
- Maintain aspect ratio of actual track
- Center track in viewing window with appropriate margins

#### 3. Driver Position Interpolation
- FastF1 provides data at ~3-20 Hz
- Interpolate positions for smooth 60 FPS rendering
- Use linear or bezier interpolation for natural movement

#### 4. Leaderboard Updates
- Recalculate positions based on lap completion and time
- Handle overtakes dynamically
- Update tyre compounds when pit stops occur

#### 5. Performance Optimization
- Preload all frame data before playback
- Use sprite batching for driver markers
- Optimize drawing calls (don't redraw static elements)

## User Interface Design

### Layout Recommendation

```
┌─────────────────────────────────────────────────────────┐
│  F1 Race Replay - [Race Name] [Year]                    │
├───────────────────────────────┬─────────────────────────┤
│                               │  LEADERBOARD            │
│                               │  1. PIA  [Soft]         │
│                               │  2. NOR  [Medium]       │
│      TRACK VIEW              │  3. HUL  [Hard]         │
│   (Main Canvas Area)          │  4. ALO  [Soft]         │
│                               │  ...                    │
│                               │  17. HAD  OUT           │
│                               ├─────────────────────────┤
│                               │  SELECTED DRIVER: RUS   │
│                               │  Speed: 287.8 km/h      │
│                               │  Gear: 7                │
│                               │  DRS: On                │
│                               │  Current Lap: 34        │
├───────────────────────────────┴─────────────────────────┤
│  Lap: 35/58  |  Race Time: 01:08:18  |  [PAUSED] 2.0x  │
│  Controls: [SPACE] Pause  [←/→] Rewind/FF  [↑/↓] Speed │
└─────────────────────────────────────────────────────────┘
```

### Color Scheme
- Use official F1 team colors for driver markers
- Dark background for main track area
- Contrasting colors for UI elements
- Highlighted selection for active driver

## Enhancement Suggestions

### Additional Features to Consider

1. **Race Highlights**
   - Mark key moments (overtakes, crashes, pit stops)
   - Jump to specific events with hotkeys

2. **Multiple Camera Views**
   - Track overview (default)
   - Follow specific driver
   - Sector zoom

3. **Data Overlay**
   - Speed trace visualization
   - Gap to leader/ahead/behind
   - Tire age indicator

4. **Comparison Mode**
   - Highlight two drivers for comparison
   - Show relative gaps and positions

5. **Weather Information**
   - Track temperature
   - Weather conditions
   - Rainfall indicator

6. **Mini-map**
   - Show full track with current focus area highlighted

7. **Export Options**
   - Save race replay as video
   - Export data to CSV

8. **Session Selection Menu**
   - GUI for choosing race/year before loading
   - Show available sessions

## Installation & Setup

### User Installation Steps
```bash
# Clone repository
git clone <repository-url>
cd f1-race-replay

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

### Dependencies (requirements.txt)
```
arcade>=2.6.0
fastf1>=3.0.0
numpy>=1.20.0
pandas>=1.3.0
matplotlib>=3.5.0
pillow>=9.0.0
```

## Development Priorities

### Phase 1: Core Functionality (MVP)
1. Data loading and caching from FastF1
2. Timeline normalization
3. Basic track rendering
4. Driver position visualization
5. Simple playback controls (play/pause)

### Phase 2: Enhanced UI
1. Leaderboard with live updates
2. Race information display
3. Playback speed controls
4. Keyboard shortcuts

### Phase 3: Telemetry & Interactivity
1. Driver selection mechanism
2. Telemetry panel
3. Tyre compound visualization
4. Driver status (OUT markers)

### Phase 4: Polish & Optimization
1. Performance optimization
2. Visual enhancements
3. Error handling
4. User documentation

## Success Criteria

- Application runs smoothly at 60 FPS
- Data loads and caches efficiently
- All drivers visible and distinguishable
- Controls are responsive and intuitive
- Leaderboard updates accurately
- Telemetry displays correct information
- Works with multiple races/seasons

## Notes & Considerations

- FastF1 requires internet connection for first-time data fetch
- Some older races may have incomplete data
- Large races (24+ drivers) may require UI adjustments
- Consider display resolution (optimize for 1920x1080 minimum)
- Handle edge cases (red flags, safety cars, race suspensions)

---

## Getting Started with Claude

To begin implementation, Claude should:
1. Set up the project structure
2. Implement basic data loading from FastF1
3. Create a simple Arcade window with track rendering
4. Add driver markers with basic movement
5. Incrementally add features according to development phases

Feel free to ask Claude to:
- Implement specific features first
- Optimize certain components
- Add creative enhancements
- Debug issues as they arise
- Suggest improvements to architecture
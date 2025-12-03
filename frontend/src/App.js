import React, { useState, useEffect } from 'react';
import './App.css';
import RaceSelector from './components/RaceSelector';
import TrackView from './components/TrackView';
import Leaderboard from './components/Leaderboard';
import TelemetryPanel from './components/TelemetryPanel';
import PlaybackControls from './components/PlaybackControls';
import RaceInfo from './components/RaceInfo';
import { useRaceData } from './hooks/useRaceData';
import { useWebSocket } from './hooks/useWebSocket';

function App() {
  const [selectedRace, setSelectedRace] = useState(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [selectedDriver, setSelectedDriver] = useState(null);

  const { raceData, loading, error, loadRace } = useRaceData();
  const { frameData, connect, disconnect, isConnected } = useWebSocket();

  useEffect(() => {
    if (selectedRace) {
      loadRace(selectedRace.year, selectedRace.gp, selectedRace.session);
    }
  }, [selectedRace, loadRace]);

  useEffect(() => {
    if (frameData) {
      setCurrentFrame(frameData.frame_index);
    }
  }, [frameData]);

  const handleRaceSelect = (race) => {
    setSelectedRace(race);
    setIsPlaying(false);
    setCurrentFrame(0);
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
  };

  const handleSpeedChange = (speed) => {
    setPlaybackSpeed(speed);
  };

  const handleDriverSelect = (driverNum) => {
    setSelectedDriver(driverNum);
  };

  if (!selectedRace) {
    return (
      <div className="app">
        <RaceSelector onRaceSelect={handleRaceSelect} />
      </div>
    );
  }

  if (loading) {
    return (
      <div className="app loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Loading race data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app error">
        <div className="error-message">
          <h2>Error Loading Race</h2>
          <p>{error}</p>
          <button onClick={() => setSelectedRace(null)}>Back to Selection</button>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>F1 Race Replay</h1>
        <button className="back-button" onClick={() => setSelectedRace(null)}>
          Change Race
        </button>
      </header>

      <div className="app-content">
        <div className="main-view">
          <RaceInfo 
            session={raceData?.session} 
            currentFrame={currentFrame}
            totalFrames={raceData?.race_data?.total_frames || 0}
            currentTime={frameData?.time || 0}
          />
          
          <TrackView 
            trackData={raceData?.track}
            driversData={frameData?.drivers || {}}
            selectedDriver={selectedDriver}
            onDriverSelect={handleDriverSelect}
          />
          
          <PlaybackControls
            isPlaying={isPlaying}
            playbackSpeed={playbackSpeed}
            onPlayPause={handlePlayPause}
            onSpeedChange={handleSpeedChange}
            currentFrame={currentFrame}
            totalFrames={raceData?.race_data?.total_frames || 0}
          />
        </div>

        <div className="sidebar">
          <Leaderboard 
            drivers={frameData?.drivers || {}}
            driversInfo={raceData?.drivers_info || []}
            selectedDriver={selectedDriver}
            onDriverSelect={handleDriverSelect}
          />
          
          <TelemetryPanel 
            driverData={frameData?.drivers?.[selectedDriver]}
            driverInfo={raceData?.drivers_info?.find(d => d.number === selectedDriver)}
          />
        </div>
      </div>
    </div>
  );
}

export default App;

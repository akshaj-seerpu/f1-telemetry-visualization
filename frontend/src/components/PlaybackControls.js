import React from 'react';
import { Play, Pause, SkipBack, SkipForward, Gauge } from 'lucide-react';
import './PlaybackControls.css';

const PlaybackControls = ({
  isPlaying,
  playbackSpeed,
  onPlayPause,
  onSpeedChange,
  currentFrame,
  totalFrames,
}) => {
  const speeds = [0.5, 1.0, 2.0, 4.0, 8.0];

  const handleSpeedUp = () => {
    const currentIndex = speeds.indexOf(playbackSpeed);
    if (currentIndex < speeds.length - 1) {
      onSpeedChange(speeds[currentIndex + 1]);
    }
  };

  const handleSpeedDown = () => {
    const currentIndex = speeds.indexOf(playbackSpeed);
    if (currentIndex > 0) {
      onSpeedChange(speeds[currentIndex - 1]);
    }
  };

  const progress = totalFrames > 0 ? (currentFrame / totalFrames) * 100 : 0;

  return (
    <div className="playback-controls">
      <div className="progress-bar">
        <div className="progress-fill" style={{ width: `${progress}%` }} />
      </div>

      <div className="controls-row">
        <div className="frame-info">
          Frame: {currentFrame} / {totalFrames}
        </div>

        <div className="control-buttons">
          <button
            className="control-btn"
            onClick={handleSpeedDown}
            disabled={playbackSpeed === speeds[0]}
            title="Decrease speed"
          >
            <SkipBack size={20} />
          </button>

          <button
            className="control-btn play-pause"
            onClick={onPlayPause}
            title={isPlaying ? 'Pause' : 'Play'}
          >
            {isPlaying ? <Pause size={24} /> : <Play size={24} />}
          </button>

          <button
            className="control-btn"
            onClick={handleSpeedUp}
            disabled={playbackSpeed === speeds[speeds.length - 1]}
            title="Increase speed"
          >
            <SkipForward size={20} />
          </button>
        </div>

        <div className="speed-indicator">
          <Gauge size={16} />
          <span>{playbackSpeed}x</span>
        </div>
      </div>

      <div className="keyboard-hints">
        <span>SPACE: Play/Pause</span>
        <span>←/→: Speed</span>
      </div>
    </div>
  );
};

export default PlaybackControls;

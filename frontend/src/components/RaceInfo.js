import React from 'react';
import './RaceInfo.css';

const RaceInfo = ({ session, currentFrame, totalFrames, currentTime }) => {
  if (!session) return null;

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="race-info">
      <div className="race-title">
        <h2>{session.event_name}</h2>
        <span className="session-type">{session.session_type}</span>
      </div>

      <div className="race-stats">
        <div className="stat">
          <span className="stat-label">Location</span>
          <span className="stat-value">{session.location}, {session.country}</span>
        </div>

        <div className="stat">
          <span className="stat-label">Date</span>
          <span className="stat-value">{session.date}</span>
        </div>

        <div className="stat">
          <span className="stat-label">Race Time</span>
          <span className="stat-value">{formatTime(currentTime)}</span>
        </div>
      </div>
    </div>
  );
};

export default RaceInfo;

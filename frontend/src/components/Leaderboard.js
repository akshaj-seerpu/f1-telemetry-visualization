import React from 'react';
import './Leaderboard.css';

const Leaderboard = ({ drivers, driversInfo, selectedDriver, onDriverSelect }) => {
  // Create leaderboard entries
  const leaderboard = Object.entries(drivers).map(([driverNum, data], index) => {
    const info = driversInfo.find(d => d.number === driverNum) || {};
    return {
      position: index + 1,
      number: driverNum,
      abbreviation: data.abbreviation || info.abbreviation || driverNum,
      team: data.team || info.team || 'Unknown',
      teamColor: data.team_color || info.team_color || '#FFFFFF',
      speed: data.speed || 0,
    };
  });

  // Sort by position (in real implementation, this would be based on lap times)
  leaderboard.sort((a, b) => a.position - b.position);

  return (
    <div className="leaderboard">
      <h3>Leaderboard</h3>
      <div className="leaderboard-list">
        {leaderboard.map((driver) => (
          <div
            key={driver.number}
            className={`leaderboard-item ${selectedDriver === driver.number ? 'selected' : ''}`}
            onClick={() => onDriverSelect(driver.number)}
          >
            <div className="position">{driver.position}</div>
            <div
              className="team-color"
              style={{ backgroundColor: driver.teamColor }}
            />
            <div className="driver-info">
              <div className="driver-abbr">{driver.abbreviation}</div>
              <div className="driver-team">{driver.team}</div>
            </div>
            <div className="driver-speed">
              {driver.speed.toFixed(0)} km/h
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Leaderboard;

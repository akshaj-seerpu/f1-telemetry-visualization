import React from 'react';
import './TelemetryPanel.css';

const TelemetryPanel = ({ driverData, driverInfo }) => {
  if (!driverData || !driverInfo) {
    return (
      <div className="telemetry-panel">
        <h3>Telemetry</h3>
        <div className="no-selection">
          <p>Select a driver to view telemetry</p>
        </div>
      </div>
    );
  }

  return (
    <div className="telemetry-panel">
      <h3>Telemetry</h3>
      
      <div className="driver-header">
        <div
          className="driver-color"
          style={{ backgroundColor: driverInfo.team_color || '#FFFFFF' }}
        />
        <div className="driver-details">
          <div className="driver-name">{driverInfo.full_name}</div>
          <div className="driver-team-name">{driverInfo.team}</div>
        </div>
      </div>

      <div className="telemetry-data">
        <div className="telemetry-item">
          <div className="telemetry-label">Speed</div>
          <div className="telemetry-value speed">
            {driverData.speed?.toFixed(1) || 0} <span className="unit">km/h</span>
          </div>
        </div>

        <div className="telemetry-item">
          <div className="telemetry-label">Gear</div>
          <div className="telemetry-value gear">
            {driverData.gear || 0}
          </div>
        </div>

        <div className="telemetry-item">
          <div className="telemetry-label">DRS</div>
          <div className={`telemetry-value drs ${driverData.drs ? 'active' : ''}`}>
            {driverData.drs ? 'ACTIVE' : 'OFF'}
          </div>
        </div>

        <div className="telemetry-item">
          <div className="telemetry-label">Position</div>
          <div className="telemetry-value position">
            X: {driverData.x?.toFixed(0) || 0}<br/>
            Y: {driverData.y?.toFixed(0) || 0}
          </div>
        </div>
      </div>
    </div>
  );
};

export default TelemetryPanel;

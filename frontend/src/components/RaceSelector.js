import React, { useState } from 'react';
import './RaceSelector.css';

const RaceSelector = ({ onRaceSelect }) => {
  const [year, setYear] = useState(2024);
  const [gp, setGp] = useState('');
  const [session, setSession] = useState('R');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (gp) {
      onRaceSelect({ year, gp, session });
    }
  };

  const currentYear = new Date().getFullYear();
  const years = Array.from({ length: 10 }, (_, i) => currentYear - i);

  const grandPrix = [
    'Bahrain', 'Saudi Arabia', 'Australia', 'Japan', 'China',
    'Miami', 'Emilia Romagna', 'Monaco', 'Canada', 'Spain',
    'Austria', 'Great Britain', 'Hungary', 'Belgium', 'Netherlands',
    'Italy', 'Azerbaijan', 'Singapore', 'United States', 'Mexico',
    'Brazil', 'Las Vegas', 'Qatar', 'Abu Dhabi'
  ];

  return (
    <div className="race-selector">
      <div className="selector-container">
        <h1>F1 Race Replay</h1>
        <p className="subtitle">Select a race to visualize</p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="year">Year</label>
            <select
              id="year"
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
            >
              {years.map(y => (
                <option key={y} value={y}>{y}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="gp">Grand Prix</label>
            <select
              id="gp"
              value={gp}
              onChange={(e) => setGp(e.target.value)}
              required
            >
              <option value="">Select a Grand Prix</option>
              {grandPrix.map(race => (
                <option key={race} value={race}>{race}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label htmlFor="session">Session</label>
            <select
              id="session"
              value={session}
              onChange={(e) => setSession(e.target.value)}
            >
              <option value="R">Race</option>
              <option value="Q">Qualifying</option>
              <option value="FP1">Free Practice 1</option>
              <option value="FP2">Free Practice 2</option>
              <option value="FP3">Free Practice 3</option>
            </select>
          </div>

          <button type="submit" className="load-button">
            Load Race
          </button>
        </form>

        <div className="info-box">
          <p>⚠️ First load may take a few minutes as data is downloaded and cached.</p>
        </div>
      </div>
    </div>
  );
};

export default RaceSelector;

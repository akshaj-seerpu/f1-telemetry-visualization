import { useState, useCallback } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const useRaceData = () => {
  const [raceData, setRaceData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadRace = useCallback(async (year, gp, sessionType = 'R') => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/race-data/${year}/${gp}/${sessionType}`
      );
      setRaceData(response.data);
      return response.data;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to load race data';
      setError(errorMessage);
      console.error('Error loading race data:', err);
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getRaces = useCallback(async (year) => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/races/${year}`);
      return response.data;
    } catch (err) {
      console.error('Error getting races:', err);
      return [];
    }
  }, []);

  return {
    raceData,
    loading,
    error,
    loadRace,
    getRaces,
  };
};

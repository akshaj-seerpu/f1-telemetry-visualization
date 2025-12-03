import React, { useRef, useEffect } from 'react';
import './TrackView.css';

const TrackView = ({ trackData, driversData, selectedDriver, onDriverSelect }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current || !trackData) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    // Set canvas size
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;

    // Clear canvas
    ctx.fillStyle = '#0f0f0f';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw track
    if (trackData && trackData.x && trackData.y) {
      drawTrack(ctx, trackData, canvas.width, canvas.height);
    }

    // Draw drivers
    if (driversData) {
      drawDrivers(ctx, driversData, trackData, canvas.width, canvas.height, selectedDriver);
    }
  }, [trackData, driversData, selectedDriver]);

  const drawTrack = (ctx, track, width, height) => {
    const x = track.x;
    const y = track.y;

    if (!x || !y || x.length === 0) return;

    // Calculate bounds
    const minX = Math.min(...x);
    const maxX = Math.max(...x);
    const minY = Math.min(...y);
    const maxY = Math.max(...y);

    const trackWidth = maxX - minX;
    const trackHeight = maxY - minY;

    // Calculate scale to fit canvas with margin
    const margin = 50;
    const scaleX = (width - 2 * margin) / trackWidth;
    const scaleY = (height - 2 * margin) / trackHeight;
    const scale = Math.min(scaleX, scaleY);

    // Draw track outline
    ctx.strokeStyle = '#444';
    ctx.lineWidth = 3;
    ctx.beginPath();

    for (let i = 0; i < x.length; i++) {
      const px = (x[i] - minX) * scale + margin;
      const py = (y[i] - minY) * scale + margin;

      if (i === 0) {
        ctx.moveTo(px, py);
      } else {
        ctx.lineTo(px, py);
      }
    }

    ctx.stroke();

    // Store transform for driver rendering
    ctx.trackTransform = { minX, minY, scale, margin };
  };

  const drawDrivers = (ctx, drivers, track, width, height, selected) => {
    if (!track || !ctx.trackTransform) return;

    const { minX, minY, scale, margin } = ctx.trackTransform;

    Object.entries(drivers).forEach(([driverNum, driver]) => {
      if (!driver.x || !driver.y) return;

      const px = (driver.x - minX) * scale + margin;
      const py = (driver.y - minY) * scale + margin;

      // Draw driver marker
      const isSelected = driverNum === selected;
      const radius = isSelected ? 8 : 6;

      // Outer circle (team color)
      ctx.fillStyle = driver.team_color || '#FFFFFF';
      ctx.beginPath();
      ctx.arc(px, py, radius, 0, 2 * Math.PI);
      ctx.fill();

      // Inner circle (white)
      ctx.fillStyle = '#FFFFFF';
      ctx.beginPath();
      ctx.arc(px, py, radius - 2, 0, 2 * Math.PI);
      ctx.fill();

      // Selection highlight
      if (isSelected) {
        ctx.strokeStyle = '#FFD700';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(px, py, radius + 3, 0, 2 * Math.PI);
        ctx.stroke();
      }

      // Draw abbreviation
      ctx.fillStyle = '#FFFFFF';
      ctx.font = 'bold 10px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(driver.abbreviation, px, py - 12);
    });
  };

  const handleCanvasClick = (e) => {
    if (!canvasRef.current || !driversData || !trackData) return;

    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    const ctx = canvas.getContext('2d');
    if (!ctx.trackTransform) return;

    const { minX, minY, scale, margin } = ctx.trackTransform;

    // Find clicked driver
    for (const [driverNum, driver] of Object.entries(driversData)) {
      if (!driver.x || !driver.y) continue;

      const px = (driver.x - minX) * scale + margin;
      const py = (driver.y - minY) * scale + margin;

      const distance = Math.sqrt((x - px) ** 2 + (y - py) ** 2);
      if (distance < 15) {
        onDriverSelect(driverNum);
        break;
      }
    }
  };

  return (
    <div className="track-view">
      <canvas
        ref={canvasRef}
        onClick={handleCanvasClick}
      />
    </div>
  );
};

export default TrackView;

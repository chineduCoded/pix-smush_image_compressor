import React, { useState, useEffect } from 'react';
import "../styles/circular-progress.css"

const CircleProgressBar = ({ percentage }) => {
  const [offset, setOffset] = useState(0);

  useEffect(() => {
    const progress = percentage / 100;
    const circumference = 2 * Math.PI * 50;
    const offsetValue = circumference * (1 - progress);
    setOffset(offsetValue);
  }, [percentage]);

  return (
    <svg className="progress-ring" width="120" height="120">
      <circle
        className="progress-ring__circle"
        stroke="#ddd"
        strokeWidth="10"
        fill="transparent"
        r="50"
        cx="60"
        cy="60"
      />
      <circle
        className="progress-ring__circle"
        stroke="#07c"
        strokeWidth="10"
        fill="transparent"
        r="50"
        cx="60"
        cy="60"
        style={{
          strokeDasharray: `${2 * Math.PI * 50}px ${2 * Math.PI * 50}px`,
          strokeDashoffset: `${offset}px`,
        }}
      />
      <text x="50%" y="50%" textAnchor="middle" fill="#333">
        {percentage}%
      </text>
    </svg>
  );
};

export default CircleProgressBar;
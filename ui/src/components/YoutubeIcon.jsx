import React from 'react';

const YouTubeIcon = ({ size, color, hoverColor }) => {
    const style = {
        fill: color,
        transition: "fill 0.2s",
        cursor: "pointer",
    };

    const handleMouseEnter = (event) => {
        event.target.style.fill = hoverColor;
    };

    const handleMouseLeave = (event) => {
        event.target.style.fill = color;
    };

    return (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width={size} height={size} style={style} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <path d="M0 0h24v24H0z" fill="none" />
            <path d="M21.6 7.4c-.2-.7-.7-1.2-1.4-1.4C19.1 6 12 6 12 6s-7.1 0-8.2-.1c-.7-.1-1.2.4-1.4 1.1-.4 1.8-.8 3.6-.8 5.4s.3 3.6.8 5.4c.2.7.7 1.2 1.4 1.4 1.1.1 8.2.1 8.2.1s7.1 0 8.2-.1c.7-.2 1.2-.7 1.4-1.4.4-1.8.8-3.6.8-5.4s-.4-3.6-.8-5.4zM9.5 15V9l5.8 3-5.8 3z" />
        </svg>
    );
};

export default YouTubeIcon;

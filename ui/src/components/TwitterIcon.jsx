import React from 'react';

const TwitterIcon = ({ size, color, hoverColor }) => {
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
            <path d="M22.5 4.1c-.8.4-1.6.7-2.5.9.9-.6 1.5-1.5 1.8-2.6-.8.5-1.7.8-2.7 1-.8-.8-2-1.3-3.3-1.3-2.5 0-4.5 2-4.5 4.5 0 .4 0 .9.1 1.3C5.7 9.4 3.3 8 1.4 5.9c-.4.7-.6 1.6-.6 2.5 0 1.7.9 3.2 2.3 4.1-.8 0-1.6-.2-2.3-.7v.1c0 2.4 1.7 4.4 4 4.9-.4.1-.8.1-1.2.1-.3 0-.6 0-.9-.1.6 1.9 2.4 3.2 4.5 3.2-1.7 1.3-3.8 2.1-6.1 2.1-.4 0-.9 0-1.3-.1 2.3 1.5 5 2.4 7.9 2.4 9.4 0 14.5-7.8 14.5-14.5l-.1-.7c1-1-2-1.9-2.9-1.4z" />
        </svg>
    );
};

export default TwitterIcon;

import React from 'react';

const UploadInCloudIcon = ({ color = '#000', size = 32, animate = false }) => {
    const animationClass = animate ? 'animate' : '';

    return (
        <svg
            xmlns="http://www.w3.org/2000/svg"
            width={size}
            height={size}
            viewBox="0 0 32 32"
            className={animationClass}
        >
            <path
                d="M26 16c-.07 0-.136.018-.204.02A10.03 10.03 0 0 0 26 14c0-5.522-4.478-10-10-10S6 8.478 6 14c0 .034.01.066.01.1C2.618 14.584 0 17.474 0 21a7 7 0 0 0 7 7h5.016A1.984 1.984 0 0 0 14 26.016V20H9.756L16 12l6.244 8H18v6.016c0 1.096.888 1.984 1.984 1.984H26a6 6 0 1 0 0-12z"
                fill={color}
            />
        </svg>
    );
};

export default UploadInCloudIcon;

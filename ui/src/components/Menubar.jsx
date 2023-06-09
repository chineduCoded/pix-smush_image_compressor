import React, { useState } from 'react';

const MenuBar = () => {
    const [isOpen, setIsOpen] = useState(false);

    const handleClick = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className="menu-bar" onClick={handleClick}>
            <svg
                className={`menu-icon ${isOpen ? 'active' : ''}`}
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                width="35"
                height="35"
            >
                {isOpen ? (
                    <path
                        fill="#000000"
                        d="M7,6.41L8.41,5L12,8.59L15.59,5L17,6.41L13.41,10L17,13.59L15.59,15L12,11.41L8.41,15L7,13.59L10.59,10L7,6.41Z"
                    />
                ) : (
                    <path
                        fill="#000000"
                        d="M3,5H21V7H3V5ZM3,11H21V13H3V11ZM3,17H21V19H3V17Z"
                    />
                )}
            </svg>
        </div>
    );
};

export default MenuBar;

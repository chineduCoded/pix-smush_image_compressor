import React from 'react';

const Button = ({ padding, size, bkgColor, content, width, height, contentColor, onSubmit, onClick}) => {
    const buttonStyle = {
        padding,
        fontSize: size,
        backgroundColor: bkgColor,
        color: contentColor,
        width,
        height,
    };

    return (
        <button
            aria-label='Custom button'
            className='btn'
            style={buttonStyle}
            onClick={onClick ? onClick : undefined}
            onSubmit={onSubmit ? onClick : undefined}>
            {content}
        </button>
    );
};

export default Button;

import React, { useRef } from 'react';

const CopyImage = ({ imageUrl }) => {
  
  const inputRef = useRef(null);

  const handleCopy = () => {
    if (inputRef.current) {
      inputRef.current.select();
      inputRef.current.setSelectionRange(0, inputRef.current.value.length);

      try {
        document.execCommand('copy');
        console.log('URL copied to clipboard');
      } catch (err) {
        console.error('Failed to copy URL to clipboard', err);
      }
    }
  };


  return (
    <div>
      <img src={imageUrl} alt="Screenshot" />
      <div>
        <input
          ref={inputRef}
          type="text"
          value={imageUrl}
          style={{ display: 'none' }}
          readOnly
        />
        <button onClick={handleCopy}>Copy Link</button>
      </div>
    </div>
  );
}

export default CopyImage;

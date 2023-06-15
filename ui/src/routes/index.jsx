import React from 'react';
import "../styles/home.css";
import ImageUploader from '../components/ImageUploader';

export const HomeScreen = () => {
  return (
    <div>
      <div className="hero">
        <h1 className='text'>Make Every Pixel Count: PixSmush's Cutting-Edge Image Compression</h1>
        <div className='tag'>
          <h3 className='tag-text'>Optimize JPEG, PNG, and WEBP</h3>
        </div>
      </div>
      <div className='upload-container'>
        <ImageUploader />
      </div>
    </div>
  );
};

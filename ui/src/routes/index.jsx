import React, { useState } from 'react';
import "../styles/home.css";
import AddIcon from '../components/AddIcon';
import UploadInCloudIcon from '../components/UploadIcon';
import Button from '../components/Button';
import QRCode from "../images/qrcode.png";
import { useCompressImageMutation, useDownloadImageQuery, useGetAllImagesQuery } from '../services/api';
import { unwrapResult } from '@reduxjs/toolkit';

export const HomeScreen = () => {
  const [file, setFile] = useState([]);
  const { mutate: compressImage } = useCompressImageMutation();
//   const { data: allImages, isLoading: isFetching } = useGetAllImagesQuery();

  const handleFileChangeAndUpload = async (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      try {
        const result = await compressImage(selectedFile);
        const data = unwrapResult(result);
        setFile(data);
        console.log(data)
        // downloadImage(imageId);
      } catch (error) {
        // Handle upload error
        console.error('Error uploading image:', error);
      }
    } else {
      // Handle invalid file selection error
      console.error('Invalid file selected.');
    }
  };

  const DownloadImage = ({ imageId }) => {
    const { data: downloadedImage, isError: downloadError, error: downloadErrorMessage } = useDownloadImageQuery(imageId);

    if (downloadError) {
      // Handle download error
      console.error('Error downloading image:', downloadErrorMessage);
      return null;
    }

    if (downloadedImage) {
      // Handle successful download
      console.log('Downloading image with ID:', imageId);
      // Implement your download logic here
    }

    return null;
  };

  return (
    <div>
      <div className="hero">
        <h1 className='text'>Make Every Pixel Count: PixSmush's Cutting-Edge Image Compression</h1>
        <div className='tag'>
          <h3 className='tag-text'>Optimize JPEG, PNG, and WEBP</h3>
        </div>
      </div>
      <div className='upload-container'>
        <label htmlFor='upload-image' className="upload">
          <UploadInCloudIcon color='rgb(24, 92, 77)' size={50} />
          <p>Compress jpg, png, webp. Max 5MB</p>
          <div>
            <div>
              <div className='add-image'>
                <AddIcon color='rgb(115, 115, 115)' />
                <span>Select image</span>
              </div>
              <input
                placeholder='Upload Image'
                aria-label='Upload image'
                type="file"
                name='upload'
                id='upload-image'
                accept=".png, .jpg, .jpeg, .webp"
                onChange={handleFileChangeAndUpload}
                hidden
              />
            </div>
          </div>
        </label>
        <div className='display-result'>
          <div className="table-wrapper">
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Before</th>
                    <th>Status</th>
                    <th>After</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td data-label="Name">
                      desert_locust_517340.jpg
                    </td>
                    <td data-label="Before">100 KB</td>
                    <td data-label="Status">
                      <span className='saved'>saved 67%</span>
                    </td>
                    <td data-label="After">45 KB</td>
                    <td data-label="action">
                      <Button
                        padding="5px 8px"
                        bkgColor="rgb(24, 92, 77)"
                        contentColor="#fff"
                        content="Download"
                        // onClick={DownloadImage()}
                      />
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div className="action-wrapper">
            <Button
              padding="10px 15px"
              bkgColor="rgb(24, 92, 77)"
              contentColor="#fff"
              content="Copy URL"
              width={280}
            />
          </div>
          <div className="qrcode-wrapper">
            hey
          </div>
        </div>
      </div>
    </div>
  );
};

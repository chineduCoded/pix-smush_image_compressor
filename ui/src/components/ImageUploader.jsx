import React, { useEffect, useState } from 'react';
import { useCompressImageMutation, useDownloadImageQuery, useQRCodeQuery } from "../services/api"
import UploadInCloudIcon from './UploadIcon';
import AddIcon from './AddIcon';
import Button from "./Button"
import "../styles/home.css"
import QRCode from "../images/qrcode.png"
import axios from 'axios';

const ImageUploader = () => {
  const [compressedData, setCompressedData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [downloadButtonDisabled, setDownloadButtonDisabled] = useState(false);
  const [imageSrc, setImageSrc] = useState('');
  const [compressImage, { isLoading, isError, isSuccess, error }] = useCompressImageMutation()

  const handleFileChange = async (e) => {
    const file = e.target.files[0];

    if (!file) {
      console.error('No file selected');
      return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
      const { data } = await compressImage(formData);
      setCompressedData(data)
      // const imageId = data.id
      // handleImageDownload(imageId);
    } catch (err) {
      console.error({"Error compressing image": err})
    }
  };

  const DownloadImage = ({ id, filename }) => {
    
    const handleImageDownload = () => {
      if (id) {
        const baseUrl = "http://127.0.0.1:5000/api/download/"
        const url = `${baseUrl}${id}`
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)

        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
      } else {
        console.error("Image cannot be downloaded!");
      }
    }
  
    return (
      <Button
        content="download"
        padding="8px 12px"
        bkgColor="rgb(24, 92, 77)"
        contentColor="white"
        disabled={isLoading || error }
        onClick={handleImageDownload}
      />
    );
  }

  const ImageSrc = ({ id }) => {
    const baseUrl = "http://127.0.0.1:5000/api/qrcode/"
    const url = `${baseUrl}${id}`

   
    useEffect(() => {
      const fetchData = async () => {
        try {
          const response = await axios.get(url, {
            responseType: 'arraybuffer',
          });
          const base64 = btoa(
            new Uint8Array(response.data).reduce(
              (data, byte) => data + String.fromCharCode(byte),
              ''
            )
          );
          const objectUrl = `data:image/png;base64,${base64}`;
          setImageSrc(objectUrl);
        } catch (error) {
          console.error('Error fetching QR code image:', error);
        }
      };
  
      fetchData();
    }, []);

    return (
      <>
       <img src={imageSrc} alt="QR Code" />
      </>
    )
  }

  return (
    <div>
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
                onChange={handleFileChange}
                hidden
              />
            </div>
          </div>
      </label>
      {
        compressedData ===  null ? (
          <div></div>
        ) : (
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
                    {compressedData.filename}
                  </td>
                  <td data-label="Before">{compressedData.original_size}</td>
                  <td data-label="Status">
                    <span className='saved'>saved {compressedData.percentage_saved}%</span>
                  </td>
                  <td data-label="After">{compressedData.compressed_size}</td>
                  <td data-label="action">
                  <DownloadImage id={compressedData.id} filemame={compressedData.filename} />
                  {errorMessage && <div>{errorMessage}</div>}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div className="action-wrapper">
          <Button
          content="Copy URL"
          padding="8px 12px"
          bkgColor="rgb(24, 92, 77)"
          contentColor="white"
          width={280} 
          />
        </div>
        <div className="qrcode-wrapper">
          <div className="image">
            {/* <img src={QRCode} alt='QR code' /> */}
            <ImageSrc id={compressedData.id} />
          </div>
        </div>
      </div>
        )
      }
    </div>
  );
}

export default ImageUploader

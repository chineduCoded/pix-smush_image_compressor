import React, { useState } from 'react';
import { useCompressImageMutation, useDownloadImageQuery } from "../services/api"
import UploadInCloudIcon from './UploadIcon';
import AddIcon from './AddIcon';
import Button from "./Button"
import "../styles/home.css"
import QRCode from "../images/qrcode.png"

const ImageUploader = () => {
  const [compressedData, setCompressedData] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [downloadButtonDisabled, setDownloadButtonDisabled] = useState(false);
  const [compressImage, { isLoading, isError, isSuccess, error }] = useCompressImageMutation()
  const downloadImage = useDownloadImageQuery()

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

  console.log(compressedData)

  const handleImageDownload = (data) => {
    if (data && data.id) {
      const { id } = data
      downloadImage(id)
    } else {
      console.error("Image cannot be downloaded!");

    // Set an error message state
    setErrorMessage("Image cannot be downloaded!");

    // Disable the download button
    setDownloadButtonDisabled(true);
    }
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
                  <Button
                    content="download"
                    padding="8px 12px"
                    bkgColor="rgb(24, 92, 77)"
                    contentColor="white"
                    onClick={() => handleImageDownload(compressedData)}
                    disabled={downloadButtonDisabled}
                  />
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
            <img src={QRCode} alt='QR code' />
          </div>
        </div>
      </div>
        )
      }
    </div>
  );
}

export default ImageUploader

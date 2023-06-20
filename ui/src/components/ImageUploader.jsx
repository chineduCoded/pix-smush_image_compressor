import React, { useState } from 'react';
import { useCompressImageMutation } from "../services/api"
import AddIcon from './AddIcon';
import "../styles/home.css"
import { Loader } from './Loader';
import { CompressedImage } from './Compressed';

const ImageUploader = () => {
  const [compressedData, setCompressedData] = useState(null);
  const [compressImage, { isLoading }] = useCompressImageMutation()

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
      console.log(data)
    } catch (err) {
      console.error({"Error compressing image": err})
    }
  };

  return (
    <div>
      
       {
        compressedData == null ? (
          <div className='upload'>
            <label htmlFor='upload-image'>
              <div className='add-image'>
                <AddIcon color='#fff' />
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
              <p className='para_text'> or drop images here</p>
            </label>
       </div>
        ) : (
          <>
          {isLoading && <div className='loader'><Loader /></div>}
        <div>
          <CompressedImage 
          percentage={compressedData.percentage_saved} 
          originalSize={compressedData.original_size}
          compressedSize={compressedData.compressed_size}
          id={compressedData.id}
          filename={compressedData.filename}
          imageUrl={compressedData.image_url}
          />
        </div>
       </>
        )
       }
    </div>
  );
}

export default ImageUploader

import React from 'react'
import "../styles/home.css"
import AddIcon from '../components/AddIcon'
import UploadInCloudIcon from '../components/UploadIcon'

export const HomeScreen = () => {
    return (
        <div>
            <dv className="hero">
                <h1 className='text'>Make Every Pixel Count: PixSmush's Cutting-Edge Image Compression</h1>
                <div className='tag'>
                    <h3 className='tag-text'>Optimize JPEG, PNG, and WEBP</h3>
                </div>
            </dv>
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
                                hidden />
                        </div>
                    </div>
                </label>
                <div className='display-result'>
                    <div className='compressed'>
                        <div className="compressed-image">
                            <div className='image-name'>
                                <span>web_image.png</span>
                                <button>X</button>
                            </div>
                            <div className='saved-percentage'>-78%</div>
                            <button type="submit" className='download'>Download</button>
                        </div>
                    </div>
                    <div className='compressed'>
                        <div className="compressed-qrcode"></div>
                    </div>
                </div>
            </div>
        </div>
    )
}

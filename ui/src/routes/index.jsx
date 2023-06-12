import React, { useState } from 'react'
import "../styles/home.css"
import AddIcon from '../components/AddIcon'
import UploadInCloudIcon from '../components/UploadIcon'

export const HomeScreen = () => {
    const [imageSrc, setImageSrc] = useState("")
    const [isLoading, setIsLoading] = useState(false)
    const [isCompressing, setIsCompressing] = useState(false)
    const [isDownloadDisabled, setIsDownloadDisabled] = useState(true)

    const handleImageUpload = (event) => {
        const file = event.target.files[0]
        const reader = new FileReader()

        reader.onload = (e) => {
            const image = new Image()
            image.src = e.target.result

            setIsLoading(true)

            image.onload = () => {
                setImageSrc(image.src)
                setIsLoading(false)
                setIsCompressing(true)

                // Simulate compressing state for 2 seconds
                setTimeout(() => {
                    setIsCompressing(false)
                    setIsDownloadDisabled(false)
                }, 2000)
            }

        }

        reader.readAsDataURL(file)
    }

    const handleDownload = () => { }

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
                                accept=".png, .jpg, .jpeg, .webp"
                                onChange={handleImageUpload}
                                hidden />
                        </div>
                    </div>
                </label>
                <div className='display-result'>
                    <div className='compressed'>
                        <div className="compressed-image" style={{ backgroundImage: `url(${imageSrc})`, backgroundSize: 'cover', backgroundPosition: 'center' }}>
                            <div className='image-name'>
                                <span>web_image.png</span>
                                <button>X</button>
                            </div>
                            {/* {imageSrc && <div className="image-overlay"></div>} */}
                            {/* <div className='saved-percentage'>-78%</div> */}
                            {isLoading && <div className="loading-state">Uploading...</div>}
                            {isCompressing && <div className="compressing-state">Compressing...</div>}
                            <button type="submit" className='download' onClick={handleDownload} disabled={isDownloadDisabled}>Download</button>
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

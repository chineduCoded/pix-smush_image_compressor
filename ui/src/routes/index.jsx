import React, { useState } from 'react'
import "../styles/home.css"
import AddIcon from '../components/AddIcon'
import UploadInCloudIcon from '../components/UploadIcon'
import Button from '../components/Button'
import QRCode from "../images/qrcode.png"

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
                    <div className="table-wrapper">
                        <div class="table-container">
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
    )
}

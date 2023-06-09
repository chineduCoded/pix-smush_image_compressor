import React from 'react'
import "../styles/home.css"

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
                <div className="upload">
                    <p>Icon</p>
                    <p>teext</p>
                    <div>
                        <button>
                            + Select file
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

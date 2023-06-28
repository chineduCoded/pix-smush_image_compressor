import React from "react"
import "../styles/compressed.css"
import { FaArrowLeft, FaDownload, FaLink, FaLongArrowAltRight } from "react-icons/fa"
import { HiOutlineTrash } from "react-icons/hi"
import { Tooltip } from 'react-tooltip'
import { CircularProgressbarWithChildren } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import Modal from "./Modal"
import { usePixSmush } from "../contexts/pixSmushContext"


export const CompressedImage = ({ percentage, originalSize, compressedSize, id, filename, imageUrl }) => {
    const { toggleModal } = usePixSmush()
   
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
            <button 
            className="download"
            onClick={handleImageDownload}
            >
            <span><FaDownload size={24} /></span>
                Download
            </button>
        );
      }
      

    return (
        <div className="compressed-container">
            <h2>Your image is compressed!</h2>
            <div className="btns-holder">
                <button 
                className="icon prev"
                data-tooltip-id="prev"
                data-tooltip-content="Back to compress image"
                >
                    <FaArrowLeft />
                </button>
                <Tooltip id="prev" place="top" effect="solid" />
                <DownloadImage id={id} filename={filename} />
                <div className="link_del">
                    <button
                    onClick={toggleModal}
                    className="icon link" 
                    data-tooltip-id="share" 
                    data-tooltip-content="Share download link or scan QR"
                    >
                        <FaLink />
                    </button>
                    <Tooltip id="share" place="top" effect="solid" />
                    <Modal 
                    id={id}
                    imageUrl={imageUrl}
                    />
                    <button 
                    className="icon trash"
                    data-tooltip-id="delete"
                    data-tooltip-content="Delete image"
                    >
                        <HiOutlineTrash/>
                    </button>
                    <Tooltip id="delete" place="bottom" effect="solid" />
                </div>
            </div>
            <div className="stats">
                <div className="progress">
                <CircularProgressbarWithChildren 
                value={percentage} 
                strokeWidth={8}
                styles={{
                    path: {stroke: 'rgb(24, 92, 77)'},
                    text: {
                        fill: '#555',
                        fontSize: '14px',
                        fontWeight: '700'
                    }
                }}>
                    <strong>
                        {percentage}%
                    </strong>
                    <h6 style={{ textTransform: "uppercase", fontSize: "12px" }}>saved</h6>
                </CircularProgressbarWithChildren>
                </div>
                <div>
                    <span style={{ color: "#555" }}>Your Image is now {percentage}% smaller!</span>
                    <div className="saved">
                       {originalSize} <FaLongArrowAltRight /> {compressedSize}
                    </div>
                </div>
            </div>
        </div>
    )
}


import React, { useEffect, useState } from "react";
import { animated, useTransition } from '@react-spring/web'
import "../styles/modal.css"
import axios from "axios"
import { AiOutlineClose } from "react-icons/ai"
import { FaCopy } from "react-icons/fa"
import Button from "./Button"
import { usePixSmush } from "../contexts/pixSmushContext";
import { useRef } from "react";


const Modal = ({ imageUrl, id }) => {
  const [imageSrc, setImageSrc] = useState('');
  const { openModal, setOpenModal } = usePixSmush()

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
    }, [url]);

    useEffect(() => {
      const handleScroll = (e) => {
        if (openModal) {
          e.preventDefault()
        }
      }
      if(openModal) {
        document.body.classList.add("modal-open")
        window.addEventListener('scroll', handleScroll, {passive: false})
      }

      return () => {
        document.body.classList.remove('modal-open')
        window.addEventListener('scroll', handleScroll)
      }
    }, [])

    return (
      <>
       <img src={imageSrc} className="img-style" alt="QR Code"/>
      </>
    )
  }

  const transitions = useTransition(openModal, {
    from: { opacity: 0, transform: 'translate(-50%, -50%) scale(0.8)' },
    enter: { opacity: 1, transform: 'translate(-50%, -50%) scale(1)' },
    leave: { opacity: 0, transform: 'translate(-50%, -50%) scale(0.8)' },
    config: {
      tension: 300,
      friction: 20
    }
  });

  const inputRef = useRef(null);

  const handleFocus = () => {
    inputRef.current.select();
  };

  const handleCopy = async () => {
    const text = inputRef.current.value;
    try {
      await navigator.clipboard.writeText(text);
      console.log("Text copied to clipboard:", text);
    } catch (error) {
      console.error("Failed to copy text to clipboard:", error);
    }
  };

  return (
    <div>
      {transitions(
        (styles, item) =>
          item && (
            <animated.div style={
              {
                ...styles,
                position: 'fixed',
                top: '50%',
                left: '50%',
                zIndex: 9999,
                background: 'rgba(0, 0, 0, 0.4)',
                backdropFilter: 'blur(2px)',
              }
            }>
              <div className="modal">
                <div className="header">
                  <h3>Copy or scan QR code</h3>
                  <button className="icon-btn" onClick={() => setOpenModal(false)}>
                    <AiOutlineClose size={24} />
                  </button>
                </div>
                <main className="content">
                  <div className="copy-link">
                    <input 
                    ref={inputRef} 
                    type="text" 
                    className="copy-link-url" 
                    value={imageUrl} 
                    readOnly 
                    onFocus={handleFocus} />
                    <button type="button" className="copy-link-btn" onClick={handleCopy}>
                      <span className="copy-link-icon">
                        <FaCopy />
                        copy
                      </span>
                    </button>
                  </div>
                  <div className="image-holder">
                    <h4>Instantly download to your phone</h4>
                    <ImageSrc id={id} />
                  </div>
                </main>
                <div className="footer">
                  <Button onClick={() => setOpenModal(false)} content="Close" contentColor="#fff" bkgColor="rgb(24, 92, 77)" />
                </div>
              </div>
            </animated.div>
          )
      )}
    </div>
  );
};

export default Modal;


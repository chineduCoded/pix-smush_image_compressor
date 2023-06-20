import React, { useEffect, useState, useRef, useCallback  } from "react";
import { animated, useSpring } from "react-spring"
import "../styles/modal.css"
import { AiOutlineClose } from "react-icons/ai"
import axios from "axios"
import Button from "./Button"


const Modal = ({ openModal, setOpenModal, imageUrl, filename, id }) => {
  const [imageSrc, setImageSrc] = useState('');

  const modalRef = useRef()

  const animation = useSpring({
    config: {
      duration: 250
    },
    opacity: openModal ? 1 : 0,
    transform: openModal ? `transform: translateY(0%)` : `transform: translateY(-100%)`
  })

  const closeModal = (e) => {
    if (modalRef.current === e.target) {
        setOpenModal(false)
    }
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

  return (
    <div>
    {openModal ? (
      <animated.div style={animation}>
        <div className="modal" openModal={openModal}>
        <div className="header">
          <h3>Copy or scan QR code</h3>
          <button className="icon-btn" onClick={() => setOpenModal(prev => !prev)}>
            <AiOutlineClose size={24} />
          </button>
        </div>
        <main className="content">
          <div className="url">
            {imageUrl}
          </div>
          <div className="image-holder">
            <h4>Instantly download to your phone</h4>
            <ImageSrc id={id} />
          </div>
        </main>
        <div className="footer">
          <Button 
          onClick={() => setOpenModal(prev => !prev)} 
          content="Close" 
          contentColor="#fff" 
          bkgColor="rgb(24, 92, 77)" />
        </div>
        </div>
      </animated.div>
    ) : null}
    </div>
  );
};

export default Modal;

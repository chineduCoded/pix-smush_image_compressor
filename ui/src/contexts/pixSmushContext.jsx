import React, { createContext, useContext, useState, useRef, useCallback, useEffect } from 'react'

const ModalContext = createContext(null)

const PixSmushContext = ({ children }) => {
    const [openModal, setOpenModal] = useState(false)

    const toggleModal = () => {
        setOpenModal(prev => !prev)
    }

    const modalRef = useRef()

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (modalRef.current === e.target) {
                setOpenModal(false)
            }
        }

        if (openModal) {
            window.addEventListener('click', handleClickOutside)
        }

        return () => {
            window.removeEventListener('click', handleClickOutside)
        }
    }, [openModal, setOpenModal])

    const keyPress = useCallback(e => {
        if(e.key === 'Escape' && openModal) {
            setOpenModal(false)
        }
    }, [setOpenModal, openModal])

    useEffect(() => {
        document.addEventListener('keydown', keyPress)
        return () => document.removeEventListener('keydown', keyPress)
    }, [keyPress])


    const contextValue = {
        openModal,
        setOpenModal,
        toggleModal,
        modalRef
    }
  return (
    <ModalContext.Provider value={contextValue}>
        {children}
    </ModalContext.Provider>
  )
}

export default PixSmushContext

export const usePixSmush = () => {
    return useContext(ModalContext)
}
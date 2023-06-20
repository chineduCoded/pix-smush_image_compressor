import React from "react"
import "../styles/loader.css"


export const Loader = () => {
    return (
        <div className="loader-container">
        <p>Compressing your image<span className="">...</span></p>
        <div className="loading"></div>
        </div>
    )
}
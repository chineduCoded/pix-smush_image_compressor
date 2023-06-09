import React from 'react'
import "../styles/navbarStyle.css"
import Logo from "../images/logo.png"
import { Link } from "react-router-dom"

const Navbar = () => {
    return (
        <nav>
            <div className="nav-content">
                <Link to="/" className='custom-link'>
                    <div className="logo">
                        <img src={Logo} alt='logo' />
                        <h1>PixSmush</h1>
                    </div>
                </Link>
                <div className="auth-btns">
                    <button className='btn sign-up-btn'>Sign up</button>
                    <button className='btn sign-in-btn'>Login</button>
                </div>
            </div>
        </nav>
    )
}

export default Navbar
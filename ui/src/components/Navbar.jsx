import React from 'react'
import "../styles/navbarStyle.css"
import Logo from "../images/logo.png"

const Navbar = () => {
    return (
        <nav>
            <div className="nav-content">
                <div className="logo">
                    <img src={Logo} alt='logo' />
                    <h1>PixSmush</h1>
                </div>
                <div className="auth-btns">
                    <button className='btn sign-up-btn'>Sign up</button>
                    <button className='btn sign-in-btn'>Login</button>
                </div>
            </div>
        </nav>
    )
}

export default Navbar
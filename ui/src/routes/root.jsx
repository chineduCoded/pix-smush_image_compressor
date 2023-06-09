import React from 'react'
import { Outlet } from "react-router-dom"
import Navbar from "../components/Navbar"
import Footer from "../components/Footer"
import "../styles/main.css"

export const Root = () => {
    return (
        <>
            <Navbar />
            <div className='content'>
                <main className='container'>
                    <Outlet />
                </main>
            </div>
            <Footer />
        </>
    )
}

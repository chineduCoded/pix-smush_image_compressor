import React from 'react'
import "../styles/mainContentStyle.css"

const MainContent = ({ children }) => {
    return (
        <div className="content">
            <main className='container'>
                {children}
            </main>
        </div>
    )
}

export default MainContent
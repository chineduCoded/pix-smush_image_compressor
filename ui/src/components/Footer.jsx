import React from 'react'
import TwitterIcon from './TwitterIcon'
import YouTubeIcon from './YoutubeIcon'
import "../styles/footer.css"

const Footer = () => {
    return (
        <footer>
            <div className='footer-content'>
                <h1>PixSmush</h1>
                <div className="copy">
                    &copy; {new Date().getFullYear()} PixSmush. All right reserved.
                </div>
                <div className="social">
                    <TwitterIcon size={24} color="rgb(115, 115, 115)" />
                    <YouTubeIcon size={24} color="rgb(115, 115, 115)" />
                </div>
            </div>
        </footer>
    )
}

export default Footer
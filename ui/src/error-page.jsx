import React from 'react'
import { useRouteError } from "react-router-dom"
import "./styles/error.css"

export const ErrorPage = () => {
    const error = useRouteError()
    console.log(error)
    return (
        <div className='error'>
            <h1>Oops!</h1><p>Sorry, an unexpected error occurred.</p>
            <p>
                <i>{error.statusText || error.message}</i>
            </p>
        </div>
    )
}

import React from 'react'
import './navButton.css'

const NavButton = (props) => {
    return <>
    <div className = "navButton">
        <button><div className="title">{props.name}</div></button>
    </div>
    </>
}

export default NavButton
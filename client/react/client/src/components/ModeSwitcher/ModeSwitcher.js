import React from 'react'
import './modeSwitcher.css'
import controllerIcon from "../../icons/controller.png"
import automaticIcon from "../../icons/automatic.png"

const ModeSwitcher = () => {

    
    return <>
        <div style={{height: "3vh"}} />
            <div class="modeContainer">
                <button>
                <img src= {controllerIcon}/>
                    <div className = "title">Manual Mode</div>
                </button>
                <button>
                    <img src= {automaticIcon}/>
                    <div className = "title">Automatic Mode</div>
                </button>
            </div>
        <div style={{height: "3vh"}} />
    </>
}

export default ModeSwitcher
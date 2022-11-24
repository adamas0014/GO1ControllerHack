import React from 'react'
import './modeSwitcher.css'
import axios from 'axios'
import controllerIcon from "../../icons/controller.png"
import automaticIcon from "../../icons/automatic.png"

const ModeSwitcher = () => {
    
    const SendToServer=(pbdata)=>{ 

        axios( {method: 'post',
                  url: 'http://127.0.0.1:5000/controls', 
                  data: pbdata
              })
          .then(res => {
              console.log(res)
          })
          .catch((e) => {
              console.log("Error", e)
          })
      }
    
    return <>
        <div style={{height: "3vh"}} />
            <div class="modeContainer">
                <button  onClick={() => {console.log("MODE: MANUAL"); SendToServer({MODE: "M"})}}>
                <img src= {controllerIcon}/>
                    <div className = "title">Manual Mode</div>
                </button>
                <button onClick={() => {console.log("MODE: AUTOMATIC"); SendToServer({MODE: "A"})}}>
                    <img src= {automaticIcon}/>
                    <div className = "title">Automatic Mode</div>
                </button>
            </div>
        <div style={{height: "3vh"}} />
    </>
}

export default ModeSwitcher
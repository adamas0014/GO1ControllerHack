import React from 'react'
import axios from 'axios'
import SpeedForm from '../SpeedForm/SpeedForm'
import './controlPad.css'



const ControlPad = () => {
    //const [form, setForm] = useState({mode: 'man', cmd: 'S'})
    

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
    


    return<>
        <div className="controlPad">
            <div style={{gridRow: 'span 3'}}></div>
            <div style={{gridRow: 'span 3', justifySelf: "end"}}><button className="primary" onClick={() => {console.log("LEFT"); SendToServer({cmd: "L"})}}>Left</button></div>
            <div> <button className="primary" onClick={() => {console.log("FORWARD"); SendToServer({cmd: "F"})}}>Forward</button> </div>
            <div style={{gridRow: 'span 3', justifySelf: "start"}}><button className="primary" onClick={() => {console.log("RIGHT"); SendToServer({cmd: "R"})}}>Right</button></div>
            <div style={{gridRow: 'span 3', alignSelf: "start"}}><SpeedForm /></div>
            <div></div>
            <div style={{gridColumn: "span 1"}}> <button className="secondary" onClick={() => {console.log("STOP"); SendToServer({cmd: "S"})}}>Stop</button> </div>
            <div></div>
            <div style={{gridColumn: "span 1"}}> <button className="primary" onClick={() => {console.log("BACKWARD"); SendToServer({cmd: "B"})}}>Backward</button> </div>
         
        </div>
    </>
}





export default ControlPad
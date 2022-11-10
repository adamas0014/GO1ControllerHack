import React from 'react'
import axios from 'axios'

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

        <div>&nbsp;</div>
        <div style={{gridRow: "span 3"}}><button className="secondary" onClick={() => {console.log("LEFT"); SendToServer({cmd: "L"})}}>Left</button></div>
        <div style={{gridColumn: "span 2"}}> <button onClick={() => {console.log("FORWARD"); SendToServer({cmd: "F"})}}>Forward</button> </div>
        <div style={{gridRow: "span 3"}}><button onClick={() => {console.log("RIGHT"); SendToServer({cmd: "R"})}}>Right</button></div>
        <div>&nbsp;</div>

        <div>&nbsp;</div>
        <div style={{gridColumn: "span 2"}}> <button onClick={() => {console.log("STOP"); SendToServer({cmd: "S"})}}>Stop</button> </div>
        <div>&nbsp;</div>

        <div>&nbsp;</div>
        <div style={{gridColumn: "span 2"}}> <button onClick={() => {console.log("BACKWARD"); SendToServer({cmd: "B"})}}>Backward</button> </div>
        <div>&nbsp;</div>
    
    </>
}





export default ControlPad
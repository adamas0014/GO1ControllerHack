import React, {useState} from 'react'
import axios from 'axios'

const Form = (props) => {
    const [form, setForm] = useState({mode: 'man', cmd: 'S'})
    

    const handleSubmit=(event)=>{ 
      event.preventDefault()
      axios( {method: 'post',
                url: 'http://127.0.0.1:5000/controls', 
                data: form
            })
        .then(res => {
            console.log(res)
        })
        .catch((e) => {
            console.log("Error", e)
        })
        setForm({cmd: ''})
    }
    
    const handleChange = (event) => {
        const {id, value} = event.target
        setForm((prevState) =>({...prevState, [id]: value}))
    }


  return (
       <div>
       <form onSubmit={handleSubmit}>
            <button name="fwd" id="fwd" onClick={() => setForm({cmd: 'F'})}>Forward</button>
            <button name="bwd" id="bwd" onClick={() => setForm({cmd: 'B'})}>Backward</button>
            <button name="lft" id="lft" onClick={() => setForm({cmd: 'L'})}>Left</button>
            <button name="rgt" id="rgt" onClick={() => setForm({cmd: 'R'})}>Right</button>
            <button name="stp" id="stp" onClick={() => setForm({cmd: 'S'})}>Stop</button>
            <button name="viewMan" id="viewMan" onClick={() => setForm({mode: 'man', cmd: 'S'})}>Manual Mode</button>
            <button name="viewAuto" id="viewAuto" onClick={() => setForm({mode: 'auto', cmd: 'S'})}>Automatic Mode</button>
            <button name="spd25" id="spd25" onClick={() => setForm({speed: 25, cmd: 'S'})}>Speed 25%</button>
            <button name="spd50" id="spd50" onClick={() => setForm({speed: 50, cmd: 'S'})}>Speed 50%</button>
            <button name="spd75" id="spd75" onClick={() => setForm({speed: 75, cmd: 'S'})}>Speed 75%</button>
            <button name="spd100" id="spd100" onClick={() => setForm({speed: 100, cmd: 'S'})}>Speed 100%</button>
       </form>
       </div>
  )}

export default Form;

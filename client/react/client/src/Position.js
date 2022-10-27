import React, {useState} from 'react'
import axios from 'axios'

const Form = (props) => {
    const [form, setForm] = useState({view: 'man', x: 512, y: 512})
    

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
        setForm({x:'', y:''})
    }
    
    const handleChange = (event) => {
        const {id, value} = event.target
        setForm((prevState) =>({...prevState, [id]: value}))
    }

    const moveFwd = () => {
        setForm({x:768, y: 512})
    }
    const moveBwd = () => {
        setForm({x:256, y: 512})
    }
    const turnLeft = () => {
        setForm({x: 512, y: 256})
    }    
    const turnRight = () => {
        setForm({x: 512, y: 768})
    }
    const moveStop = () => {
        setForm({x: 512, y: 512})
    }
    


  return (
       <div>
       <form onSubmit={handleSubmit}>
            <button name="fwd" id="fwd" onClick={moveFwd}>Forward</button>
            <button name="bwd" id="bwd" onClick={moveBwd}>Backward</button>
            <button name="lft" id="lft" onClick={turnLeft}>Left</button>
            <button name="rgt" id="rgt" onClick={turnRight}>Right</button>
            <button name="stp" id="stp" onClick={moveStop}>Stop</button>
            <button name="viewMan" id="viewMan" onClick={() => setForm({view: 'man', x: 512, y: 512})}>Manual Mode</button>
            <button name="viewAuto" id="viewAuto" onClick={() => setForm({view: 'auto', x: 512, y: 512})}>Automatic Mode</button>
           
       </form>
       </div>
  )}

export default Form;

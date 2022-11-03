import React from 'react'
import './CommandForm.css'


const CommandForm = () => {

    const [form, setForm] = React.useState({past: []})

    const formChange = (event) => {
        const {id, value} = event.target
        setForm((prevState) => ({...prevState, [id]: value}))
    }

    const formSubmit =(event) => {
        event.preventDefault()
        if(form.past.length > 0){
            let formCpy = {...form}
            formCpy.past.shift()
            setForm(formCpy)
        }


        //Make api request


    }

    const getPast = () => {
        let ret = ''
        if(form.past.length > 0){
            for(let i = 0; i < 10; i++){
                ret.push(form.past[i] + '\n')
            }
        }
        return ret
    }

    return <div className="commandForm">
        <br />
        <form onSubmit={formSubmit}>
            <input type="text" id = "cmd" onChange={formChange}></input> <br />
            <button type="submit">Send Command</button>
        </form>
        <br />
        <div className="past">
        <textarea placeholder={getPast} value=" "></textarea>
        </div>
    </div>
}
export default CommandForm
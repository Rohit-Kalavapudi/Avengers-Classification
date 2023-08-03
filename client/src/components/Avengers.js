import React from 'react'
import { useState } from 'react'
import axios from 'axios'

export const Avengers = () => {
    const [image, setImage] = useState("");
    const handleImgChange=(e)=>{
        const file = (e.target.files[0])
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = ()=>{
            const base64String = reader.result.replace("data:", "").replace(/^.+,/, "");
            setImage(base64String)
            // console.log(base64String);
        }
    }
    const sendImage= async() =>{
        // console.log("dsf")
        const data= new FormData();
        data.append("image",image);
        var d="Hey, this is working"
        console.log(data)
        const response = await axios.post(
            "http://localhost:5006/hello1",
            { data: image },
            {
              headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
              },
            }
          );
          const el=document.getElementById('display')
          console.log(response.data[0])
        //   const obj=JSON.parse(response.data[0])
        const name=response.data[0]["class"].toUpperCase()
        const probabilities=response.data[0]['class_probability']
          el.innerHTML=`${name}`
          document.getElementById('bruce').innerHTML="Bruce : "+probabilities[0]
          document.getElementById('clint').innerHTML="Clint : "+probabilities[1]
          document.getElementById('natasha').innerHTML="Natasha : "+probabilities[2]
          document.getElementById('steve').innerHTML="Steve : " + probabilities[3]
          document.getElementById('thor').innerHTML="Thor : "+probabilities[4]
          document.getElementById('tony').innerHTML="Tony : "+probabilities[5]
        console.log(response.data)
    }
    const ff=()=>{
        console.log("ff")
    }
  return (
    <>
    <div>Avengers</div>
    <input type="file" onChange={handleImgChange}/>
    <input type="submit" onClick={sendImage} name="" id="" />
    <p id="display" style={{color:'green'}}></p>
    <div id='probabilities'>
        <p id="bruce"></p>
        <p id="clint"></p>
        <p id="natasha"></p>
        <p id="steve"></p>
        <p id="thor"></p>
        <p id="tony"></p>

    </div>
    </>
  )
}

import React from "react"
import "./python_mini_proj/file_upload.css"
import header from "./python_mini_proj/header"

export default function fun(){

  return(
    <>
    <div>
        <img src="public/clothes.png" alt="icon"/>
        <h1>Style Mate</h1>
    </div>
    <br/>
    <form action="http://127.0.0.1:5000/analyse" method="post" encType="multipart/form-data">
       
        <label>Upload images of your shirts/T-shirts(upper outfits) : </label>
        <br/>
        <input type="file" name="uo" multiple></input> 
        <br/>
        <label>Upload images of your pants/Track pants(lower outfits) : </label>
        <br/>
        <input type="file" name="lo" multiple></input> 
        <br/>
        <br/>
        <button type="submit">Upload</button>
       
    </form>

    </>
  )  
}

import React from "react"
import "./form/file_upload.css"

export default function fun(){

  return(
    <>
    <form action="http://127.0.0.1:5000/analyse" method="post" encType="multipart/form-data"
>
        <fieldset>
        <legend>FILE UPLOAD</legend>
        <label>Upload your files : </label>
        <input type="file" name="file" multiple></input> 
        <button type="submit">Upload</button>
        </fieldset>
    </form>
    </>
  )  
}

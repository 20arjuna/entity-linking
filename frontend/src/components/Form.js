import React from "react";
import '../mystyle.css';

function Form()
{
    return(
            <div>
                <form className = "center" id="myForm" action ="/link" method ="POST" enctype="multipart/form-data">
                    <textarea className = "center" placeholder="Enter question here" id="textInput" name ="textInput" rows="4" cols="50"></textarea>
                    <h5></h5>
                    <input className = "center" type="submit" name="my-form" value="Link Entities"></input>
                </form>
                <h5></h5>
                <textarea className = "center" placeholder = "Linked Entities will display here" rows="4" cols="50" id="entityDisplay"></textarea>
            </div>
    );
}
export default Form

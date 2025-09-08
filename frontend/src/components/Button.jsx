import React from "react";
import classes from "./Button.module.css"

export function Button(props){
    return(
        <button className={classes.button} onClick={onClick}>
            <span className={classes["actual-text"]}>&nbsp;{props.button_text}&nbsp;</span>
            <span aria-hidden="true" className={classes["hover-text"]}>&nbsp;{props.button_text}&nbsp;</span>
        </button>
    )
}
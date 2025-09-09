import React from "react";
import classes from "./Button.module.css"

export function Button({ button_text, onClick }) {
    return (
        <button
            className={classes.button}
            data-text="Awesome"
            onClick={onClick}
        >
            <span className={classes["actual-text"]}>&nbsp;{button_text}&nbsp;</span>
            <span aria-hidden="true" className={classes["hover-text"]}>&nbsp;{button_text}&nbsp;</span>
        </button>
    );
}

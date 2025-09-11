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

export function ButtonSubmit({ button_text, onClick}) {
    return (
        <button 
        className={classes.buttonSubmit}
        data-text="Awesome"
        onClick={onClick}
        >
            <span className={classes.buttonSubmit_text}>{button_text}</span>
        </button>
    )
}
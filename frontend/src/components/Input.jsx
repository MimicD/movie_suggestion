import classes from "./Input.module.css"

export function TextInput({ label="text", type="text", value, onChange, placeholder }) {
    return (
        <input className={classes.textInput} label={label} type={type} value={value} onChange={onChange} placeholder={placeholder}/>
    );
}


export function PromptInput({ prompt }) {
    return (
        <input className={classes.promptInput}/>
    )
}
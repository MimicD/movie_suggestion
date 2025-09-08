// Header.jsx
import classes from "./Header.module.css";

export function Header({ children }) {
    return (
        <div className={classes.header}>
            <h3 className={classes.logo}>MovieSuggestor</h3>
            <div className={classes["header-right"]}>
                {children}
            </div>
        </div>
    );
}

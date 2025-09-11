import classes from "./Header.module.css";
import { useAuth } from "./AuthContext";
import { Link } from "react-router-dom";
import { Button } from "./Button";
import logo from "../assets/Logo.png";

export function Header() {
    const { isAuth, logout } = useAuth();

    return (
        <div className={classes.header}>
            <img className={classes.logo} src={logo}/>
            <div className={classes["header-right"]}>
                {isAuth ? (
                    <>
                        <Button button_text="Logout" onClick={() => {
                            logout();
                            console.log("Clicked logout");
                            }}
                        />
                        
                        {
                        //<Link to={"/"}><Button button_text="Go Home" /></Link>
                        }
                    </>
                ) : (
                    <>
                        <Link to="/login"><Button button_text="Sign In" /></Link>
                        <Link to="/register"><Button button_text="Sign Up" /></Link>
                    </>
                )}
            </div>
        </div>
    );
}

//import './MainPage.css'
import { useAuth } from "../components/AuthContext";
import { Header } from "../components/Header";
import { ButtonSubmit } from "../components/Button.jsx";
import { PromptInput } from "../components/Input.jsx";
import classes from "./MainPage.module.css";

export function MainPage() {
    const { isAuth } = useAuth();

    return (
        <>
            <Header />
            {isAuth ? (
                <div className={classes.centerForm}>
                    <h1>Welcome!</h1>
                    <span>Find your movie just typing a prompt</span>
                    <PromptInput />
                    <ButtonSubmit />
                </div>
            ) : (
                <div>
                    <div>Hel</div>
                </div>
            )}
        </>
    );
}



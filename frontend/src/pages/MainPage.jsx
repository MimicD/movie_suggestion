//import './MainPage.css'
import { Link } from "react-router-dom";

import { Header } from "../components/Header";
import { ManyButtons } from "../components/ManyButtons";
import { Button } from "../components/Button";

export function MainPage() {
    return (
        <>
            <Header>
                <ManyButtons>
                    <Link to={"/login"}><Button button_text="Sign In" /></Link>
                    <Link to={"/register"}><Button button_text="Sign Up" /></Link>
                </ManyButtons>
            </Header>
            <h1>Main Page</h1>
        </>
    );
}



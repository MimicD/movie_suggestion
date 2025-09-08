

import { Link } from "react-router-dom";

import { Header } from "../components/Header.jsx";
import { ManyButtons } from "../components/ManyButtons";
import { Button } from "../components/Button";

export function LoginPage(){
    return (
        <>
            <Header>
                <ManyButtons>
                    <Link to={"/"}>
                        <Button button_text="Go Home" />
                    </Link>
                </ManyButtons>
            </Header>
            <h1>Login</h1>
        </>
    );
}
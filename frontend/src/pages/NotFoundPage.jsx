import { Link } from "react-router-dom";
import { Button } from "../components/Button.jsx"
import { ManyButtons } from "../components/ManyButtons.jsx";

export function NotFoundPage(){
    return (
        <>
            <ManyButtons>
                <Link to={"/"}>
                    <Button button_text="Go Home" />
                </Link>
            </ManyButtons>
            <h1>Not Found Page</h1>
        </>
    )
}

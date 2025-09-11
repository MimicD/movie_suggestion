import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/AuthContext";
import { Header } from "../components/Header.jsx";
import { ButtonSubmit } from "../components/Button";
import { TextInput } from "../components/Input.jsx";

import classes from "./RegisterPage.module.css";


export function RegisterPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { login } = useAuth();

    async function handleRegister(e) {
        e.preventDefault();

        if (password !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/api/users/register/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) throw new Error("Registration failed");

            const data = await response.json();

            // Auto Login
            login(data.access, data.refresh);
            navigate("/");


        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <>
            <Header />
            <div className={classes.centerForm}>
                <form className={classes.inputFrom} onSubmit={handleRegister}>
                    <TextInput type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username"/>
                    <TextInput type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password"/>
                    <TextInput type="text" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} placeholder="Confirm Password"/>
                    <ButtonSubmit button_text="Register" />
                </form>
            </div>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </>
    );
}
import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../components/AuthContext";
import { Header } from "../components/Header.jsx";
import { Button } from "../components/Button";

export function LoginPage() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const navigate = useNavigate();
    const { login } = useAuth();

    async function handleLogin(e) {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/api/users/login/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) throw new Error("Invalid credentials");

            const data = await response.json();
            login(data.access, data.refresh); // call login() from context
            navigate("/");
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <>
            <Header />
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} placeholder="Username" />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" />
                <Button button_text="Login" />
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
        </>
    );
}

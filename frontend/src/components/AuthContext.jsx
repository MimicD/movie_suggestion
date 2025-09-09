import { createContext, useContext, useState, useEffect } from "react";

// Create the context itself
const AuthContext = createContext();

// Hook to easily access the context
export function useAuth() {
    return useContext(AuthContext);
}

// Provider (wrapper) that will store the authentication state
export function AuthProvider({ children }) {
    // Check if there is a token in localStorage
    const [isAuth, setIsAuth] = useState(!!localStorage.getItem("access"));

    // Function to log in
    function login(access, refresh) {
        localStorage.setItem("access", access);
        localStorage.setItem("refresh", refresh);
        setIsAuth(true);
    }

    // Function to log out
    function logout() {
        localStorage.removeItem("access");
        localStorage.removeItem("refresh");
        setIsAuth(false);
    }

    useEffect(() => {
        const interval = setInterval(async () => {
            const refresh = localStorage.getItem("refresh");
            if (!refresh) return;

            try {
                const res = await fetch("http://localhost:8000/api/token/refresh/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ refresh }),
                });
                if (!res.ok) throw new Error("Refresh failed");
                const data = await res.json();
                localStorage.setItem("access", data.access);
                setIsAuth(true);
                } catch (err) {
                    logout();
                }
        }, 4 * 60 * 1000); // each 4 minutes

        return () => clearInterval(interval);
    }, []);


    return (
        <AuthContext.Provider value={{ isAuth, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

import { createContext, useContext, useState } from "react";

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

    return (
        <AuthContext.Provider value={{ isAuth, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
}

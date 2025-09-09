import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext.jsx";

export function PrivateRoute({ children }) {
    const { isAuth } = useAuth();

    if (!isAuth) {
        // Если юзер не авторизован → редиректим на /login
        return <Navigate to="/login" replace />;
    }

    return children;
}

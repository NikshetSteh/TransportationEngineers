import CircularProgressWithStyle from "../CircularProgressWithStyle.tsx";
import { useNavigate, useLocation } from "react-router";
import { useAuth } from "react-oidc-context"

const Login = () => {
    const auth = useAuth()
    const navigate = useNavigate();
    const location = useLocation();

    if (!auth.isLoading && !auth.isAuthenticated) {
        void auth.signinRedirect({
            "redirect_uri": "/login",
            "state": "/profile"
        })
    }

    if (!auth.isLoading) {
        // noinspection TypeScriptUnresolvedReference
        const redirectTo = location.state?.from?.pathname || '/profile';
        navigate(redirectTo, { replace: true });
    }

    return <CircularProgressWithStyle />
}

export default Login

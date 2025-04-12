import {createRoot} from 'react-dom/client'
import App from './App.tsx'
import 'bootstrap/dist/css/bootstrap.min.css'
import './index.css'
import {BrowserRouter} from "react-router";
import {AuthProvider} from "react-oidc-context";

const oidcConfig = {
    authority: "https://cufar.space/keycloak/realms/ai_site",
    client_id: "ai_site",
    redirect_uri: "https://cufar.space/login",
    // redirect_uri: "http://localhost:5173/profile",
    loadUserInfo: true,
    silent_redirect_uri: "/login"
};

createRoot(document.getElementById('root')!).render(
    <BrowserRouter>
        <AuthProvider {...oidcConfig}>
            <App/>
        </AuthProvider>
    </BrowserRouter>,
)

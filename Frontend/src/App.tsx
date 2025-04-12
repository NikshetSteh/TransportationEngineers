import './App.css'
import {Route, Routes} from 'react-router';
import Index from "./components/pages/Index.tsx";
import Profile from "./components/pages/Profile.tsx";
import {useAuth} from "react-oidc-context";
import {JSX} from "react";
import Login from "./components/pages/Login.tsx";


function PrivateRoute({children}: { children: JSX.Element }) {
    const auth = useAuth();

    console.log("Auth:", auth)

    if (!auth.isLoading && !auth.isAuthenticated) {
        console.log("Signing in...")
        auth.signinRedirect().then(
            () => console.log("Signed in"),
            () => console.log("Error signing in")
        )
    }

    return children
}

function App() {
    return (
        <Routes>
            <Route index element={<Index/>}/>

            <Route path="/profile" element={
                <PrivateRoute>
                    <Profile/>
                </PrivateRoute>
            }/>

            <Route path="/login" element={<Login/>}/>
        </Routes>
    )
}

export default App

// import logo from "../assets/icon.svg";
// import Button from "react-bootstrap/Button";
// import {JSX} from "react/jsx-runtime";
//
// import {useAuth} from "react-oidc-context";
//
// function Header(): JSX.Element {
//     const auth = useAuth();
//
//     const onSignIn = () => {
//         void auth.signinRedirect({
//             state: window.location.pathname,
//             redirect_uri: window.origin + "/login"
//         });
//     };
//
//     const onSignUp = onSignIn;
//
//     const onSignOut = () => {
//         void auth.signoutRedirect({
//             post_logout_redirect_uri: window.location.origin
//         });
//     };
//
//     return (
//         <header
//             className="padding-0 d-flex justify-content-between align-items-center bg-secondary text-white flex-wrap">
//             <div
//                 className="align-self-stretch w-auto base-background d-flex justify-content-center align-items-center icon-container">
//                 <img src={logo} alt="Robot Logo" className="img-fluid" style={{maxHeight: '60px'}}/>
//             </div>
//             <div className="p-3 d-flex flex-wrap gap-2 justify-content-end">
//                 {auth.isLoading || (
//                     !auth.isAuthenticated ? (
//                         <>
//                             <Button variant="primary" onClick={onSignIn}>Войти</Button>
//                             <Button variant="secondary" onClick={onSignUp}>Зарегистрироваться</Button>
//                         </>
//                     ) : (
//                         <>
//                             <Button variant="outline-light" href="/profile">Профиль</Button>
//                             <Button variant="secondary" onClick={onSignOut}>Выйти</Button>
//                         </>
//                     )
//                 )}
//             </div>
//         </header>
//     );
// }
//
//
// export default Header


import logo from "../assets/icon.svg";
import Button from "react-bootstrap/Button";
import Dropdown from "react-bootstrap/Dropdown";
import {JSX, useEffect, useState} from "react";

import {useAuth} from "react-oidc-context";

function Header(): JSX.Element {
    const auth = useAuth();
    const [isMobile, setIsMobile] = useState(window.innerWidth < 400);

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth < 400);
        };
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const onSignIn = () => {
        void auth.signinRedirect({
            state: window.location.pathname,
            redirect_uri: window.origin + "/login",
        });
    };

    const onSignUp = onSignIn;

    const onSignOut = () => {
        void auth.signoutRedirect({
            post_logout_redirect_uri: window.location.origin,
        });
    };

    const renderAuthButtons = () => {
        if (auth.isLoading) return null;

        if (isMobile) {
            return (
                <Dropdown>
                    <Dropdown.Toggle
                        as="button"
                        className="without-after bg-transparent border-0 p-0 m-0 d-flex align-items-center"
                        style={{
                            boxShadow: "none",
                            backgroundColor: "transparent",
                            border: "none",
                            content: "none"
                        }}
                    >
                        <span className="material-icons fs-1 text-white">menu</span>
                    </Dropdown.Toggle>
                    <Dropdown.Menu align="end">
                        {!auth.isAuthenticated ? (
                            <>
                                <Dropdown.Item onClick={onSignIn}>Войти</Dropdown.Item>
                                <Dropdown.Item onClick={onSignUp}>Зарегистрироваться</Dropdown.Item>
                            </>
                        ) : (
                            <>
                                <Dropdown.Item href="/profile">Профиль</Dropdown.Item>
                                <Dropdown.Item onClick={onSignOut}>Выйти</Dropdown.Item>
                            </>
                        )}
                    </Dropdown.Menu>
                </Dropdown>
            );
        } else {
            return !auth.isAuthenticated ? (
                <>
                    <Button variant="primary" onClick={onSignIn}>Войти</Button>
                    <Button variant="secondary" onClick={onSignUp}>Зарегистрироваться</Button>
                </>
            ) : (
                <>
                    <Button variant="outline-light" href="/profile">Профиль</Button>
                    <Button variant="secondary" onClick={onSignOut}>Выйти</Button>
                </>
            );
        }
    };

    return (
        <header
            className="padding-0 d-flex justify-content-between align-items-center bg-secondary text-white flex-wrap">
            <div
                className="align-self-stretch w-auto base-background d-flex justify-content-center align-items-center icon-container">
                <img src={logo} alt="Robot Logo" className="img-fluid" style={{maxHeight: '60px'}}/>
            </div>
            <div className="p-3 d-flex flex-wrap gap-2 justify-content-end">
                {renderAuthButtons()}
            </div>
        </header>
    );
}

export default Header;


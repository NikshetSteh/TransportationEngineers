// Props for Header Component
import logo from "../assets/icon.svg";
import Button from "react-bootstrap/Button";
import {JSX} from "react/jsx-runtime";

import {useAuth} from "react-oidc-context";


// Header Component
function Header(): JSX.Element {
    const auth = useAuth();

    const onSignIn = () => {
        void auth.signinRedirect(
            {
                state: window.location.pathname,
                redirect_uri: window.origin + "/login"
            }
        );
    }

    const onSignUp = onSignIn

    const onSignOut = () => {
        void auth.signoutRedirect({
            post_logout_redirect_uri: window.location.origin
        });
    }

    return <header className="padding-0 d-flex justify-content-between align-items-center bg-secondary text-white">
        {/* auto width */}
        <div
            className="align-self-stretch w-auto base-background d-flex justify-content-center align-items-cente icon-container">
            <img src={logo} alt="Robot Logo" className="base-background"/>
        </div>
        <div className="p-3 h-auto">
            {auth.isLoading ||
                (
                    !auth.isAuthenticated ?
                        <>
                            <Button variant="primary" className="me-2" onClick={onSignIn}>Войти</Button>
                            <Button variant="secondary" onClick={onSignUp}>Зарегистрироваться</Button>
                        </> :
                        <>
                            <Button variant="secondary" onClick={onSignOut}>Выйти</Button>
                        </>
                )
            }
            {/*<Button variant="primary" className="me-2">Войти</Button>*/}
            {/*<Button variant="secondary">Зарегистрироваться</Button>*/}
        </div>
    </header>
}


export default Header

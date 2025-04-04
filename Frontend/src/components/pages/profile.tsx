import logo from "../../assets/icon.svg";
import Button from "react-bootstrap/Button";
import axios from "axios";
import React, {useState, useEffect} from "react";

// Define types for API responses
interface BiometricsResponse {
    available: boolean;
}

interface TicketsResponse {
    tickets: string[];
}

// Define types for user data
interface UserData {
    fullName: string;
    email: string;
}

const ProfilePage: React.FC = () => {
    // State for user data
    const [userData, setUserData] = useState<UserData>({
        fullName: "John Doe",
        email: "john.doe@example.com",
    });

    const [editMode, setEditMode] = useState(false);
    const [newEmail, setNewEmail] = useState<string>(userData.email);

    // State for password update
    const [oldPassword, setOldPassword] = useState<string>("");
    const [newPassword, setNewPassword] = useState<string>("");

    // State for biometrics
    const [biometricsAvailable, setBiometricsAvailable] = useState<boolean>(false);
    const [loadingBiometrics, setLoadingBiometrics] = useState<boolean>(true);

    // State for tickets
    const [tickets, setTickets] = useState<string[]>([]);

    // Fetch biometrics availability
    useEffect(() => {
        const fetchBiometrics = async () => {
            try {
                const response = await axios.get<BiometricsResponse>("/api/biometrics");
                setBiometricsAvailable(response.data.available);
            } catch (error) {
                console.error("Error fetching biometrics:", error);
            } finally {
                setLoadingBiometrics(false);
            }
        };

        fetchBiometrics();
    }, []);

    // Fetch current tickets
    useEffect(() => {
        const fetchTickets = async () => {
            try {
                const response = await axios.get<TicketsResponse>("/api/tickets");
                if (response.data.tickets) {
                    setTickets(response.data.tickets);
                }
            } catch (error) {
                console.error("Error fetching tickets:", error);
            }
        };

        fetchTickets();
    }, []);

    // Handle email update
    const handleEmailUpdate = () => {
        setUserData((prev) => ({...prev, email: newEmail}));
        setEditMode(false);
        alert("Email updated successfully!");
    };

    // Handle password update
    const handlePasswordUpdate = () => {
        if (!oldPassword || !newPassword) {
            alert("Please fill in both old and new passwords.");
            return;
        }

        // Simulate API call to update password
        axios
            .post("/api/update-password", {oldPassword, newPassword})
            .then(() => {
                alert("Password updated successfully!");
                setOldPassword("");
                setNewPassword("");
            })
            .catch((error) => {
                alert("Failed to update password. Please check your old password.");
                console.error(error);
            });
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            {/* Header */}
            <header className="padding-0 d-flex justify-content-between align-items-center bg-secondary text-white">
                {/* Logo */}
                <div
                    className="align-self-stretch w-auto base-background d-flex justify-content-center align-items-center icon-container">
                    <img src={logo} alt="Robot Logo" className="base-background"/>
                </div>
                <div className="p-3 h-auto">
                    {/*<Button variant="primary" className="me-2">Войти</Button>*/}
                    {/*<Button variant="secondary">Зарегистрироваться</Button>*/}
                </div>
            </header>

            {/* Hero Section */}
            {/*<section*/}
            {/*    className="position-relative text-white"*/}
            {/*    style={{height: "30vh"}}*/}
            {/*>*/}
            {/*    /!* Background Image *!/*/}
            {/*    <img*/}
            {/*        src={background}*/}
            {/*        alt="Высокоскоростные поезда"*/}
            {/*        className="position-absolute top-0 start-0 w-100 h-100 object-fit-cover"*/}
            {/*    />*/}

            {/*    /!* Adjusted Text Position *!/*/}
            {/*    <div*/}
            {/*        className="position-absolute d-flex flex-column justify-content-center text-center"*/}
            {/*        style={{*/}
            {/*            top: "50%",*/}
            {/*            left: "50%",*/}
            {/*            transform: "translate(-50%, -50%)",*/}
            {/*        }}*/}
            {/*    >*/}
            {/*        <h1 className="display-4 base-background p-1 m-0">Профиль пользователя</h1>*/}
            {/*    </div>*/}
            {/*</section>*/}

            {/* Profile Content */}
            <div className="container py-5">
                {/* User Data Section */}
                <div className="card mb-4">
                    <div className="card-body">
                        <h2 className="card-title fs-3 fw-bold">Информация о пользователе</h2>
                        <p>
                            <strong>ФИО:</strong> {userData.fullName}
                        </p>
                        {editMode ? (
                            <div>
                                <input
                                    type="email"
                                    value={newEmail}
                                    onChange={(e) => setNewEmail(e.target.value)}
                                    className="form-control mb-2"
                                    placeholder="Введите новый email"
                                />
                                <Button onClick={handleEmailUpdate} variant="primary" className="me-2">
                                    Сохранить Email
                                </Button>
                                <Button onClick={() => setEditMode(false)} variant="secondary">
                                    Отмена
                                </Button>
                            </div>
                        ) : (
                            <p>
                                <strong>Email:</strong> {userData.email}
                                <Button
                                    onClick={() => setEditMode(true)}
                                    variant="link"
                                    className="ms-2 p-0 text-decoration-none"
                                >
                                    Редактировать
                                </Button>
                            </p>
                        )}

                        <hr/>

                        <h3 className="fs-5 fw-bold">Обновление пароля</h3>
                        <div className="mb-3">
                            <input
                                type="password"
                                placeholder="Старый пароль"
                                value={oldPassword}
                                onChange={(e) => setOldPassword(e.target.value)}
                                className="form-control mb-2"
                            />
                            <input
                                type="password"
                                placeholder="Новый пароль"
                                value={newPassword}
                                onChange={(e) => setNewPassword(e.target.value)}
                                className="form-control mb-2"
                            />
                            <Button onClick={handlePasswordUpdate} variant="primary">
                                Обновить пароль
                            </Button>
                        </div>
                    </div>
                </div>

                {/* Biometrics Section */}
                <div className="card mb-4">
                    <div className="card-body">
                        <h2 className="card-title fs-3 fw-bold">Биометрия</h2>
                        {loadingBiometrics ? (
                            <p>Загрузка информации о биометрии...</p>
                        ) : biometricsAvailable ? (
                            <p>Биометрия доступна.</p>
                        ) : (
                            <Button href="/upload-biometrics" variant="success">
                                Загрузить биометрию
                            </Button>
                        )}
                    </div>
                </div>

                {/* Tickets Section */}
                <div className="card mb-4">
                    <div className="card-body">
                        <h2 className="card-title fs-3 fw-bold">Ваши билеты</h2>
                        {tickets.length > 0 ? (
                            <ul className="list-group">
                                {tickets.map((ticket, index) => (
                                    <li key={index} className="list-group-item">
                                        {ticket}
                                    </li>
                                ))}
                            </ul>
                        ) : (
                            <p>
                                У вас нет билетов.{" "}
                                <Button href="/buy-tickets" variant="primary">
                                    Купить билеты
                                </Button>
                            </p>
                        )}
                        <Button href="/all-tickets" variant="secondary" className="mt-3">
                            Посмотреть полную историю билетов
                        </Button>
                    </div>
                </div>
            </div>

            {/* Footer */}
            <footer className="py-3 bg-secondary text-white text-center mt-auto">
                <p className="mb-1">© 2025 Высокоскоростные железные дороги</p>
                <ul className="list-unstyled">
                    <li>
                        <a href="#" className="text-white text-decoration-none">
                            Политика конфиденциальности
                        </a>
                    </li>
                    <li>
                        <a href="#" className="text-white text-decoration-none">
                            Пользовательское соглашение
                        </a>
                    </li>
                </ul>
            </footer>
        </div>
    );
};

export default ProfilePage;
import Button from "react-bootstrap/Button";
import axios from "axios";
import React, {useState, useEffect} from "react";
import {useAuth} from "react-oidc-context";
import Header from "../Header.tsx";
import Footer from "../Footer.tsx";

interface UserInfoProps {
    fullName: string;
    email: string;
}


function UserInfo({fullName, email}: UserInfoProps) {
    return <div className="card mb-4">
        <div className="card-body">
            <h2 className="card-title fs-3 fw-bold">Информация о пользователе</h2>
            <p>
                <strong>ФИО:</strong> {fullName}
            </p>
            <p>
                <strong>Email:</strong> {email}
            </p>
        </div>
    </div>
}

interface BiometricsResponse {
    available: boolean;
}

interface TicketsResponse {
    tickets: string[];
}

interface UserData {
    fullName: string;
    email: string;
}

const ProfilePage: React.FC = () => {
    const auth = useAuth()

    const [userData, setUserData] = useState<UserData>({
        fullName: "Unknown",
        email: "Unknown",
    });

    const [biometricsAvailable, setBiometricsAvailable] = useState<boolean>(false);
    const [loadingBiometrics, setLoadingBiometrics] = useState<boolean>(true);

    const [tickets, setTickets] = useState<string[]>([]);

    useEffect(() => {
        if (auth.isLoading) {
            return
        }

        const fetchBiometrics = async () => {
            const response = await axios.get<BiometricsResponse>("/base_api/v1/frontend/faces", {
                headers: {
                    Authorization: `Bearer ${auth.user?.access_token}`,
                },
                validateStatus: (status: number) => status == 200 || status == 404,
            });
            if (response.status == 200) {
                setBiometricsAvailable(true);
            } else if (response.status == 404) {
                setBiometricsAvailable(false);
            } else {
                throw new Error("Unexpected status code");
            }
            setLoadingBiometrics(false);
        };

        void fetchBiometrics();
    }, [auth.isLoading, auth.user?.access_token]);

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

        void fetchTickets();
    }, [auth.isLoading]);

    useEffect(
        () => {
            setUserData({
                fullName: (auth.user?.profile?.fullname as string) || "Unknown",
                email: (auth.user?.profile?.email as string) || "Unknown",
            })
        },
        [auth.isLoading, auth.user?.profile?.email, auth.user?.profile?.fullname]
    );

    if (auth.isLoading) {
        return <div>Loading...</div>;
    }

    return (
        <div className="d-flex flex-column min-vh-100">
            <Header/>

            {/* Profile Content */}
            <div className="container py-5">
                {/* User Data Section */}
                <UserInfo fullName={userData.fullName} email={userData.email}/>

                {/* Biometrics Section */}
                <div className="card mb-4">
                    <div className="card-body">
                        <h2 className="card-title fs-3 fw-bold">Биометрия</h2>
                        {loadingBiometrics ? (
                            <p>Загрузка информации о биометрии...</p>
                        ) : biometricsAvailable ? (
                            <p>Биометрия доступна.</p>
                        ) : (
                            <Button href="/profile/biometrics/upload" variant="success">
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

            <Footer/>
        </div>
    );
};

export default ProfilePage;
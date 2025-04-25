import {useAuth} from "react-oidc-context";
import {useEffect, useState} from "react";
import axios from "axios";
import {QRCodeSVG} from "qrcode.react";
import {Modal, Button} from "react-bootstrap";

interface Ticket {
    id: string;
    user_id: string;
    train_number: number;
    wagon_number: number;
    place_number: number;
    station_id: string;
    destination: string;
    date: string;
    start_date: string;
}

interface PaginatedResponse<T> {
    page: number;
    size: number;
    pages: number;
    total: number;
    items: T[];
}

interface TicketProps {
    ticket: Ticket;
    onShowQR: (ticket: Ticket) => void;
}

function formatDate(iso: string): string {
    return new Date(iso).toLocaleString("ru-RU", {
        dateStyle: "medium",
        timeStyle: "short",
    });
}

function addHours(date: string, hours: number): string {
    const d = new Date(date);
    d.setTime(d.getTime() + hours * 60 * 60 * 1000);
    return d.toISOString();
}

function TicketCard({ticket, onShowQR}: TicketProps) {
    const departureTime = ticket.date;
    const arrivalTime = addHours(ticket.date, 1.5);

    return (
        <div className="card mb-3 shadow-sm">
            <div className="card-body">
                <h5 className="card-title mb-3 fw-semibold text-primary">
                    🚆 Направление: {ticket.destination}
                </h5>
                <div className="row">
                    <div className="col-md-6">
                        <p className="mb-1">🚉 Станция: <strong>{ticket.station_id}</strong></p>
                        <p className="mb-1">📅 Дата отправления: <strong>{formatDate(departureTime)}</strong></p>
                        <p className="mb-1">📅 Дата прибытия: <strong>{formatDate(arrivalTime)}</strong></p>
                    </div>
                    <div className="col-md-6">
                        <p className="mb-1">🚋 Вагон: <strong>{ticket.wagon_number}</strong></p>
                        <p className="mb-1">💺 Место: <strong>{ticket.place_number}</strong></p>
                        <p className="mb-1">🧾 Номер поезда: <strong>{ticket.train_number}</strong></p>
                    </div>
                </div>
                <div className="d-flex justify-content-between align-items-center mt-3">
                    <small className="text-muted">Ticket ID: {ticket.id} | User ID: {ticket.user_id}</small>
                    <button className="btn btn-outline-primary btn-sm" onClick={() => onShowQR(ticket)}>
                        📲 Показать QR-код
                    </button>
                </div>
            </div>
        </div>
    );
}

function Tickets() {
    const auth = useAuth();
    const [tickets, setTickets] = useState<Ticket[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [qrTicket, setQrTicket] = useState<Ticket | null>(null);

    useEffect(() => {
        const fetchTickets = async () => {
            try {
                const response = await axios.get<PaginatedResponse<Ticket>>(
                    "/base_api/v1/frontend/tickets",
                    {
                        headers: {
                            Authorization: `Bearer ${auth.user?.access_token}`,
                        },
                    }
                );
                setTickets(response.data.items ?? []);
            } catch (error) {
                console.error("Error fetching tickets:", error);
            } finally {
                setIsLoading(false);
            }
        };

        if (!auth.isLoading && auth.user?.access_token) {
            void fetchTickets();
        }
    }, [auth.isLoading, auth.user?.access_token]);

    return (
        <>
            <div className="card shadow-sm">
                <div className="card-body">
                    {/*<h2 className="card-title fs-4 fw-bold mb-4">📄 Мои билеты</h2>*/}
                    <div className="d-flex justify-content-between align-items-center mb-4">
                        <h2 className="card-title fs-4 fw-bold">📄 Мои билеты</h2>
                        <Button variant="primary" href={"/tickets/buy"}>
                            Купить билеты
                        </Button>
                    </div>

                    {auth.isLoading || isLoading ? (
                        <p>🔄 Загрузка...</p>
                    ) : tickets.length > 0 ? (
                        tickets.map((ticket) => (
                            <TicketCard key={ticket.id} ticket={ticket} onShowQR={setQrTicket}/>
                        ))
                    ) : (
                        <p className="text-muted">Билеты не найдены.</p>
                    )}
                </div>
            </div>

            {/* QR Modal */}
            <Modal show={qrTicket !== null} onHide={() => setQrTicket(null)} centered>
                <Modal.Header closeButton>
                    <Modal.Title>🎫 QR-код билета</Modal.Title>
                </Modal.Header>
                <Modal.Body className="text-center">
                    {qrTicket && (
                        <>
                            <QRCodeSVG value={qrTicket.id} size={256}/>
                            <p className="mt-3 text-muted">ID билета: {qrTicket.id}</p>
                        </>
                    )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setQrTicket(null)}>
                        Закрыть
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}

export default Tickets;

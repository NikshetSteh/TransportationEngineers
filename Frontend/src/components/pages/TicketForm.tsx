import {useState, ChangeEvent, FormEvent, useEffect} from "react";
import Header from "../Header.tsx";
import Footer from "../Footer.tsx";
import {useAuth} from "react-oidc-context";
import {Link} from "react-router";
import axios from "axios";

interface TicketFormData {
    date: string;
    time: string;
    direction: string;
    wagon: string;
    place: string;
}

const timeOptions: string[] = ["05:00", "08:00", "13:00", "17:00"];

function TrainTicketForm() {
    const [formData, setFormData] = useState<TicketFormData>({
        date: "",
        time: "",
        direction: "Moscow",
        wagon: "",
        place: ""
    });

    const [submitting, setSubmitting] = useState(false);
    const [message, setMessage] = useState("");
    const [submitSuccess, setSubmitSuccess] = useState(false);

    const auth = useAuth();

    // Utility function to convert time in GMT+3 to local time
    const convertToLocalTime = (time: string): string => {
        const [hour, minute] = time.split(":").map(Number);
        const gmtPlus3Time = new Date();
        gmtPlus3Time.setUTCHours(hour - 3, minute); // Shift time to GMT+3
        return gmtPlus3Time.toLocaleTimeString([], {hour: "2-digit", minute: "2-digit", hour12: false});
    };


    useEffect(() => {
        const today = new Date();
        const isoDate = today.toISOString().split("T")[0];

        const getTimeInGMTPlus3 = (): { hours: number; minutes: number } => {
            const formatter = new Intl.DateTimeFormat('en-GB', {
                timeZone: 'Etc/GMT-3',
                hour: '2-digit',
                minute: '2-digit',
                hour12: false,
            });

            const parts = formatter.formatToParts(new Date());
            const hours = Number(parts.find(p => p.type === 'hour')?.value);
            const minutes = Number(parts.find(p => p.type === 'minute')?.value);

            return { hours, minutes };
        };

        const { hours, minutes } = getTimeInGMTPlus3();

        const currentTimeMinutes = hours * 60 + minutes;

        // Find the next available time from the options
        const closestTime = timeOptions.find((timeStr) => {
            const [h, m] = timeStr.split(":").map(Number);
            const optionMinutes = h * 60 + m;
            return optionMinutes > currentTimeMinutes;
        }) || timeOptions[0]; // Default to the first option if it's already past time

        setFormData((prev) => ({
            ...prev,
            date: isoDate,
            time: closestTime,
        }));
    }, []);

    const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const {name, value} = e.target;
        setFormData({...formData, [name]: value});
    };

    const handleSubmit = async (e: FormEvent) => {
        e.preventDefault();
        setSubmitting(true);
        setMessage("");
        setSubmitSuccess(false);

        try {
            const datetimeString = `${formData.date}T${formData.time}:00+03:00`;
            const date = new Date(datetimeString);

            const payload = {
                wagon_number: parseInt(formData.wagon, 10),
                place_number: parseInt(formData.place, 10),
                station_id: formData.direction === "Moscow" ? "SPB" : "MOSCOW",
                destination_id: formData.direction === "Moscow" ? "MOSCOW" : "SPB",
                // date: gmtPlus3Time,
                date: date.toISOString(),
            };

            const response = await axios.post("/base_api/v1/frontend/tickets", payload, {
                headers: {
                    authorization: `Bearer ${auth.user?.access_token}`,
                },
            });

            if (response.status === 200) {
                setMessage("Билет успешно куплен.");
                setSubmitSuccess(true);
            } else {
                setMessage("Ошибка при покупке билета.");
            }
        } catch (error: any) {
            console.error(error);
            if (error.response && error.response.data && error.response.data.message) {
                setMessage(error.response.data.message);
            } else {
                setMessage("Произошла ошибка при отправке.");
            }
        }

        setSubmitting(false);
    };

    return (
        <div className="d-flex flex-column min-vh-100 bg-light">
            <Header/>

            <main className="container my-5 flex-grow-1">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card shadow">
                            <div className="card-body">
                                {!submitSuccess ? (
                                    <>
                                        <h2 className="card-title text-center mb-4">Покупка билета на поезд</h2>

                                        <form onSubmit={handleSubmit}>
                                            <div className="mb-3">
                                                <label htmlFor="date" className="form-label">Дата</label>
                                                <input
                                                    type="date"
                                                    id="date"
                                                    name="date"
                                                    className="form-control"
                                                    value={formData.date}
                                                    onChange={handleChange}
                                                    required
                                                    min={new Date().toISOString().split("T")[0]}
                                                />
                                            </div>

                                            <div className="mb-3">
                                                <label htmlFor="time" className="form-label">Время</label>
                                                <select
                                                    id="time"
                                                    name="time"
                                                    className="form-select"
                                                    value={formData.time}
                                                    onChange={handleChange}
                                                    required
                                                >
                                                    <option value="" disabled>Выберите время</option>
                                                    {timeOptions.map((time) => (
                                                        <option key={time} value={time}>
                                                            {convertToLocalTime(time)} {/* Show in local time */}
                                                        </option>
                                                    ))}
                                                </select>
                                            </div>

                                            <div className="mb-3">
                                                <label htmlFor="direction" className="form-label">Направление</label>
                                                <select
                                                    id="direction"
                                                    name="direction"
                                                    className="form-select"
                                                    value={formData.direction}
                                                    onChange={handleChange}
                                                >
                                                    <option value="Moscow">Москва</option>
                                                    <option value="SPB">Санкт-Петербург</option>
                                                </select>
                                            </div>

                                            <div className="mb-3">
                                                <label htmlFor="wagon" className="form-label">Вагон</label>
                                                <input
                                                    type="number"
                                                    id="wagon"
                                                    name="wagon"
                                                    className="form-control"
                                                    min="1"
                                                    value={formData.wagon}
                                                    onChange={handleChange}
                                                    required
                                                />
                                            </div>

                                            <div className="mb-3">
                                                <label htmlFor="place" className="form-label">Место</label>
                                                <input
                                                    type="number"
                                                    id="place"
                                                    name="place"
                                                    className="form-control"
                                                    min="1"
                                                    value={formData.place}
                                                    onChange={handleChange}
                                                    required
                                                />
                                            </div>

                                            <div className="d-grid">
                                                <button type="submit" className="btn btn-primary" disabled={submitting}>
                                                    {submitting ? "Покупка..." : "Купить билет"}
                                                </button>
                                            </div>
                                        </form>
                                    </>
                                ) : (
                                    <>
                                        <div className="alert alert-success text-center" role="alert">
                                            {message}
                                        </div>
                                        <div className="d-grid mt-3">
                                            <Link to="/profile" className="btn btn-success">
                                                Вернуться в профиль
                                            </Link>
                                        </div>
                                    </>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            <Footer/>
        </div>
    );
}

export default TrainTicketForm;

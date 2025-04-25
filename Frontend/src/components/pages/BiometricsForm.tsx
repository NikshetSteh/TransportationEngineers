import React, { useState } from "react";
import Header from "../Header.tsx";
import Footer from "../Footer.tsx";
import axios from "axios";
import { useAuth } from "react-oidc-context";
import {Link} from "react-router";

function BiometricsForm() {
    const [photo, setPhoto] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");
    const [uploadSuccess, setUploadSuccess] = useState(false);

    const auth = useAuth();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        setPhoto(file ?? null);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!photo) {
            setMessage("Пожалуйста, выберите фото.");
            return;
        }

        const formData = new FormData();
        formData.append("file", photo);

        setUploading(true);
        setMessage("");
        setUploadSuccess(false);

        try {
            const response = await axios.post("/base_api/v1/frontend/faces", formData, {
                headers: {
                    authorization: `Bearer ${auth.user?.access_token}`,
                },
            });

            if (response.status === 200) {
                setMessage("Загрузка успешна");
                setUploadSuccess(true);
            } else {
                setMessage("Ошибка при загрузке файла.");
            }
        } catch (error) {
            console.error(error);
            setMessage("Произошла ошибка при загрузке.");
        }

        setUploading(false);
    };

    return (
        <div className="d-flex flex-column min-vh-100 bg-light">
            <Header />

            <main className="container my-5 flex-grow-1">
                <div className="row justify-content-center">
                    <div className="col-md-6">
                        <div className="card shadow">
                            <div className="card-body">
                                <h2 className="card-title text-center mb-4">Загрузите ваше фото</h2>

                                <form onSubmit={handleSubmit}>
                                    <div className="mb-3">
                                        <label htmlFor="photo" className="form-label">
                                            Выберите изображение:
                                        </label>
                                        <input
                                            id="photo"
                                            type="file"
                                            accept="image/*"
                                            onChange={handleFileChange}
                                            className="form-control"
                                        />
                                    </div>

                                    <div className="d-grid">
                                        <button
                                            type="submit"
                                            className="btn btn-primary"
                                            disabled={uploading}
                                        >
                                            {uploading ? "Загрузка..." : "Отправить"}
                                        </button>
                                    </div>
                                </form>

                                {message && (
                                    <div className="alert alert-info mt-4 text-center" role="alert">
                                        {message}
                                    </div>
                                )}

                                {uploadSuccess && (
                                    <div className="d-grid mt-3">
                                        <Link to="/profile" className="btn btn-success">
                                            Вернуться в профиль
                                        </Link>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}

export default BiometricsForm;

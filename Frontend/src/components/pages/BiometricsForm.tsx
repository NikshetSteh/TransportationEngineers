import React, { useState } from "react";
import Header from "../Header.tsx";
import Footer from "../Footer.tsx";
import axios from "axios";
import {useAuth} from "react-oidc-context";

function BiometricsForm() {
    const [photo, setPhoto] = useState<File | null>(null);
    const [uploading, setUploading] = useState(false);
    const [message, setMessage] = useState("");

    const auth = useAuth();

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        setPhoto(file ?? null);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!photo) {
            setMessage("Please select a photo.");
            return;
        }

        const formData = new FormData();
        formData.append("file", photo);

        setUploading(true);
        setMessage("");

        // try {
        //     const response = await fetch("/base_api/v1/frontend/faces", {
        //         method: "POST",
        //         body: formData,
        //     });
        //
        //     if (!response.ok) {
        //         throw new Error("Upload failed");
        //     }
        //
        //     const data = await response.json();
        //     setMessage("Upload successful: " + data.filename);
        // } catch (error) {
        //     setMessage("Error uploading file.");
        // } finally {
        //     setUploading(false);
        // }
        const response = await axios.post("/base_api/v1/frontend/faces", formData, {
            headers: {
                authorization: `Bearer ${auth.user?.access_token}`,
            },
        })

        if (response.status === 200) {
            setMessage("Upload successful: " + response.data.filename);
        } else {
            setMessage("Error uploading file.");
        }
        setUploading(false);
    };

    return (
        <div className="d-flex flex-column min-vh-100">
            <Header/>

            <div className="container my-4 flex-grow-1">
                <h2>Upload your photo</h2>
                <form onSubmit={handleSubmit}>
                    <div className="mb-3">
                        <input type="file" accept="image/*" onChange={handleFileChange} />
                    </div>
                    <button type="submit" className="btn btn-primary" disabled={uploading}>
                        {uploading ? "Uploading..." : "Submit"}
                    </button>
                </form>
                {message && <div className="mt-3 alert alert-info">{message}</div>}
            </div>

            <Footer/>
        </div>
    );
}

export default BiometricsForm;

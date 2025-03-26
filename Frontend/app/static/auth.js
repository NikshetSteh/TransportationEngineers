function getCookie(name) {
    const cookieArr = document.cookie.split(";"); // Split cookies into an array
    for (let cookie of cookieArr) {
        cookie = cookie.trim(); // Remove whitespace
        if (cookie.startsWith(name + "=")) {
            return cookie.substring((name + "=").length);
        }
    }
    return null;
}

async function refreshAccessToken() {
    try {
        const response = await fetch("/api/refresh", {
            method: "POST",
            credentials: "include", // Include cookies for authentication
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`Failed to refresh token: ${response.status}`);
        }

        const data = await response.json();

        document.cookie = `access_token=${data.access_token}; expires=${
            new Date(Date.now() + data.expire_in * 1000).toUTCString()
        }; path=/`;
        document.cookie = `refresh_token=${data.refresh_token}; expires=${
            new Date(Date.now() + data.refresh_expire_in * 1000).toUTCString()
        }; path=/`;
    } catch (error) {
        console.error("Error refreshing access token:", error);
        window.location.href = "/login";
    }
}

function checkAndRefreshToken() {
    const accessToken = getCookie("access_token");
    const refreshToken = getCookie("refresh_token");

    if (!accessToken) {
        console.log("Access token is missing. Attempting to refresh...");
        if (refreshToken) {
            refreshAccessToken();
        } else {
            window.location.href = "/login";
        }
    }
}

setInterval(checkAndRefreshToken, 5000);
function getCookie(name) {
    const cookieArr = document.cookie.split(";");
    for (let cookie of cookieArr) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
            return cookie.substring((name + "=").length);
        }
    }
    return null;
}

const accessToken = getCookie("access_token");

if (accessToken) {
    fetch("http://localhost:8080/base_api/v1/frontend/get_ticket", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json",
        },
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Parse the response as JSON
        })
        .then(data => {
            wagon_number_html = document.getElementById("wagon_number");
            wagon_number_html.innerHTML = data.wagon_number;

            seat_number_html = document.getElementById("seat_number");
            seat_number_html.innerHTML = data.place_number;

            const all = document.getElementsByClassName('authorized');
            for (let i = 0; i < all.length; i++) {
                all[i].style.display = 'block';
            }
        })
        .catch(error => {
            console.error("Error:", error); // Handle errors
        });
} else {
    console.error("Access token not found in cookies.");
}

function decodeBase64Unicode(encodedStr) {
    try {
        // Decode base64 and handle Unicode characters
        return decodeURIComponent(
            Array.from(atob(encodedStr))
                .map(c => `%${c.charCodeAt(0).toString(16).padStart(2, '0')}`)
                .join("")
        );
    } catch (e) {
        console.error("Failed to decode base64 string with Unicode:", e);
        return null;
    }
}

const encodedUsername = getCookie("given_name");
if (encodedUsername) {
    const username = decodeBase64Unicode(encodedUsername);
    if (username) {
        document.getElementById("name").textContent = `Здравствуйте, ${username}!`;
    } else {
        console.error("Failed to decode username.");
    }
} else {
    console.error("Username cookie not found.");
}




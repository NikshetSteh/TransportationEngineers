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
    fetch(window.ROBOT_API + "/frontend/get_ticket", {
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

            const dateObj = new Date(data.date);

            const formattedDate = dateObj.toLocaleString("ru-RU", {
                weekday: "long",  // "Monday"
                year: "numeric",  // "2024"
                month: "long",    // "March"
                day: "numeric",   // "27"
                hour: "2-digit",  // "2"
                minute: "2-digit",// "30"
                hour12: false      // "PM" (can be false for 24-hour format)
            });


            departure_time_html = document.getElementById("departure_time");
            departure_time_html.innerHTML = formattedDate;

            train_number_html = document.getElementById("train_number");
            train_number_html.innerHTML = data.train_number;


            const ticket_block = document.getElementById('ticket');
            ticket_block.style.display = 'block';
        })
        .catch(error => {
            console.error("Error:", error); // Handle errors
        });
} else {
    console.error("Access token not found in cookies.");
}


fetch("/api/v1/users", {
    method: "GET",
    headers: {
        "Content-Type": "application/json",
    },
})
    .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return response.json();
        }
    )
    .then(data => {
        document.getElementById("name").textContent = `Здравствуйте, ${data.username}!`;
    })
    .catch(error => {
        console.error("Error:", error);
    });

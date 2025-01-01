// Function to get a specific cookie value by name
function getCookie(name) {
    const cookieArr = document.cookie.split(";"); // Split cookies into an array
    for (let cookie of cookieArr) {
        cookie = cookie.trim(); // Remove whitespace
        if (cookie.startsWith(name + "=")) {
            return cookie.substring((name + "=").length);
        }
    }
    return null; // Return null if the cookie is not found
}

// Retrieve the access token from the cookie
const accessToken = getCookie("access_token");

if (accessToken) {
    // Send a request to the API
    fetch("http://localhost:8080/base_api/v1/frontend/get_ticket", {
        method: "GET", // or "POST", "PUT", etc.
        headers: {
            "Authorization": `Bearer ${accessToken}`, // Add token to the Authorization header
            "Content-Type": "application/json", // Specify the content type if sending JSON data
        },
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json(); // Parse the response as JSON
    })
    .then(data => {
        console.log("API Response:", data); // Handle the response data
    })
    .catch(error => {
        console.error("Error:", error); // Handle errors
    });
} else {
    console.error("Access token not found in cookies.");
}

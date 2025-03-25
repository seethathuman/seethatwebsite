// thank you chatgpt
document.addEventListener('DOMContentLoaded', async function () {
    const dropdownButton = document.getElementById('dropdownButton');
    const dropdownContent = document.getElementById('dropdownContent');

    // Toggle dropdown visibility on button click
    dropdownButton.addEventListener('click', function (event) {
        event.stopPropagation(); // Prevent click from bubbling up to the document
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    // Hide dropdown when clicking anywhere else
    document.addEventListener('click', function () {
        dropdownContent.style.display = 'none';
    });

    // Check login status
    if (getCookie('username')) { // If logged into user, check if it exists
        const isLoggedIn = await checkLogin();
        if (!isLoggedIn) { // If it doesn't exist, delete cookies and refresh the page
            location.reload();
        }
    }
    document.getElementById("username").textContent = getCookie('username') || 'guest';
});

// Function to set a cookie
function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000)); // Set expiration date
    const expires = "expires=" + d.toUTCString();
    document.cookie = name + "=" + value + ";" + expires + ";path=/"; // Set cookie
    console.log("Saved cookie | name: " + name + ", value: " + value + ", expires: " + expires);
}

// Function to get a cookie by name
function getCookie(name) {
    console.log("Getting cookie: " + name);
    const nameEQ = name + "="; // Create a string to search for
    const ca = document.cookie.split(';'); // Split all cookies into an array
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i].trim(); // Trim whitespace
        if (c.indexOf(nameEQ) === 0) {
            console.log("Cookie value: " + c.substring(nameEQ.length));
            return c.substring(nameEQ.length); // Return the cookie value
        }
    }
    return null; // Return null if cookie is not found
}

// Function to delete a cookie
function deleteCookie(name) {
    setCookie(name, "", -1); // Set the cookie to expire in the past
}

// Function to check login status
async function checkLogin() {
    const data = {
        'password': getCookie('password'),
        'username': getCookie('username')
    };

    try {
        const response = await fetch('https://seethathuman.alwaysdata.net/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        if (response.status !== 200) {
            deleteCookie("username");
            deleteCookie("password");
            return false;
        }
        return true;
    } catch (error) {
        console.error("Login check failed:", error);
        return false;
    }
}

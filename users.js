document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const passwordForm = document.getElementById('passwordForm');
    const logoutBtn = document.getElementById('logoutbtn');
    const deleteBtn = document.getElementById('deletebtn');
    const changeBtn = document.getElementById('changebtn');

    if (registerForm) {
        registerForm.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            try {
                const response = await fetch('https://seethathuman.alwaysdata.net/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                alert(result.message);
            } catch (error) {
                console.error("Registration error:", error);
                alert("An error occurred during registration.");
            }
        };
    }

    if (passwordForm) {
        passwordForm.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);
            const entries = {
                "username": getCookie("username"),
                "password": getCookie("password"),
                "usernameConfirm": data["username-confirm"],
                "passwordNew": data["password-new"],
                "passwordConfirm": data["password-confirm"]
            };
            try {
                const response = await fetch('https://seethathuman.alwaysdata.net/api/change-password', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(entries)
                });
                const result = await response.json();
                if (response.status === 200) {
                    setCookie('password', data["password-new"], 30);
                    location.reload();
                }
                alert(result.message);
            } catch (error) {
                console.error("Password Error:", error);
                alert("An error occurred while changing your password.");
            }
        };
    }

    if (loginForm) {
        loginForm.onsubmit = async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData);

            try {
                const response = await fetch('https://seethathuman.alwaysdata.net/api/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                alert(result.message);

                if (response.status === 200) {
                    setCookie('username', data.username, 30);
                    setCookie('password', data.password, 30);
                    location.reload();
                }
            } catch (error) {
                console.error("Login error:", error);
                alert("An error occurred during login.");
            }
        };
    }

    if (logoutBtn) logoutBtn.addEventListener("click", logout);
    if (deleteBtn) deleteBtn.addEventListener("click", confirmDelete);
    if (changeBtn) changeBtn.addEventListener("click", changePassword);
});

function logout() {
    deleteCookie("username");
    deleteCookie("password");
    alert("Logged out!");
    window.location.replace("login.html");
}

function changePassword() {
    window.location.href = "change-password.html";
}

async function deleteAccount() {
    const data = {
        'password': getCookie('password'),
        'username': getCookie('username')
    };
    try {
        const response = await fetch('https://seethathuman.alwaysdata.net/api/delete', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        alert(result.message);
        if (response.status === 200) logout();
    } catch (error) {
        console.error("Account deletion error:", error);
        alert("An error occurred while deleting your account.");
    }
}

function confirmDelete() {
    showAlert("Are you sure you want to delete this account?", deleteAccount);
}
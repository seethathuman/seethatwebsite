let callbackFunction = null;

function showAlert(message, callback) {
    document.getElementById('alertBox').style.display = 'flex'
    document.getElementById("alertText").textContent = message;
    callbackFunction = callback;
}

function closeAlert() {
    document.getElementById('alertBox').style.display = 'none';
}

function confirmAction() {
    if (callbackFunction) callbackFunction();
    closeAlert();
}
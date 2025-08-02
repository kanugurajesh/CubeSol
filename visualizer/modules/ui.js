import { duration } from "./animations.js";

export function showAlert(strong_message, long_message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-warning fade show';
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
            <strong>${strong_message}</strong> ${long_message}
    `;
    // Append the alert to the messages container
    const messagesContainer = document.getElementById('messages-container');
    messagesContainer.appendChild(alertDiv);

    // Fade out after 100ms
    setTimeout(() => {
        alertDiv.classList.add('fade-out');
    }, 100);

    // Remove the alert from the DOM after the fade-out transition ends
    alertDiv.addEventListener('transitionend', () => {
        alertDiv.remove();
    });
}
  
// Displays the move given in Rubik's notation
export function displayMove(move) {
    const actionDisplay = document.getElementById("action-display");
    actionDisplay.textContent = ""; // reset the display
    actionDisplay.textContent = move;

    setTimeout(() => {
        actionDisplay.textContent = "";
    }, duration * 1000 + 100); // display for a 100ms longer than animation duration
}

// Takes a boolean and updates the toggle button to show the current direction
export function toggleShowDirection(clockwise) {
    const clockwiseIcon = document.getElementById("clockwise-icon");
    const counterClockwiseIcon = document.getElementById("counter-clockwise-icon");

    if (clockwise) {
        clockwiseIcon.style.display = "block";
        counterClockwiseIcon.style.display = "none";
    } else {
        clockwiseIcon.style.display = "none";
        counterClockwiseIcon.style.display = "block";
    }
}

// Takes a boolean. True to disable manual buttons, false to enable.
export function disableManualButtons(disable) {
    document.getElementById("solve-button").disabled = disable;
    document.getElementById("undo-button").disabled = disable;
    document.getElementById("clockwise-icon").disabled = disable;
    document.getAnimations("counter-clockwise-icon").disabled = disable;
}

export function clearAllDisplays() {
    const actionDisplay = document.getElementById("action-display");
    const solutionDisplay = document.getElementById("solution-display");
    actionDisplay.textContent = "";
    solutionDisplay.textContent = "";
}
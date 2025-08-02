import { initMotions } from './animations.js';
import { disableManualButtons, toggleShowDirection } from "./ui.js";

let mode = {
    autoSolve: false, // default false (i.e. manual mode)
    reverse: false // default clockwise rotations
};

export function isAutoSolveMode() {
    return mode.autoSolve === true;
}

export function isReverseMode() {
    return mode.reverse === true;
}

export function resetMode() {
    setAutoSolve(false);
    setReverse(false);
}

export function setAutoSolve(autoSolve) {
    mode.autoSolve = autoSolve;
    // disable/enable manual moves based on mode
    disableManualButtons(autoSolve);
}

// Helper function to toggle reverse and update motions
// Takes a boolean reverse and sets reverse mode to that value
// If param is null, toggles to opposite of current state
export function setReverse(reverse = null) {
    mode.reverse = reverse === null ? !mode.reverse : reverse;
    let clockwise = !mode.reverse;
    initMotions(clockwise);
    if (!mode.autoSolve) toggleShowDirection(!mode.reverse);
}
window.setReverse = setReverse;



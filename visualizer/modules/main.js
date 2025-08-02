import './modes.js'; // defines the different operational modes of the app
import {initMotions, updateAnimations} from './animations.js'; // defines face rotation animations
import {initCanvas} from './sceneManager.js'; // sets up the canvas and asynchronously renders the scene using an update callback
import { resetCubeObject} from './rubik.js'; // defines the cube and its actions
import './action_utils.js'; // manages user interactions, performs moves, and displays action info on the GUI
import { initKeyHandler } from './keyHandler.js';
import './solutionService.js'; // implements functions for autosolve mode
import './scramble.js'; // implements scramble functionality
import { render } from './sceneManager.js';
import { resetMode } from './modes.js';
import { resetBackendState } from './api.js';
import { clearAllDisplays } from './ui.js';


initCanvas();
resetState();

// update callback
async function update() {
    updateAnimations();
    requestAnimationFrame(update); // requests the next update call; this creates a loop
    render();
}
update();

export function resetState() {
    resetBackendState();
    sessionStorage.clear();
    resetCubeObject();
    initMotions(true);
    initKeyHandler();
    resetMode();
    clearAllDisplays();
}
window.resetState = resetState;
import { displayMove, showAlert } from "./ui.js";
import { saveMove, undoLastMove } from "./action_utils.js";
import { isAutoSolveMode, isReverseMode, setReverse } from "./modes.js";
import { animate, Faces } from "./animations.js";


const keyActions = {
    82: { // "R".charCodeAt()
      action: async () => {
        await animate(Faces.RIGHT);
      }, // rotate right clockwise wrt x
      face: "R"
    },
    76: { // "L".charCodeAt()
      action: async () => {
        await animate(Faces.LEFT);
      }, // rotate left counterclockwise wrt x
      face: "L"
    },
    77: { // "M".charCodeAt()
      action: async () => {
        await animate(Faces.MID);
      }, // rotate middle clockwise wrt x
      face: "M"
    },
    85: { // "U".charCodeAt()
      action: async () => {
        await animate(Faces.UP);
      }, // rotate top clockwise wrt y
      face: "U"
    },
    68: { // "D".charCodeAt()
      action: async () => {
        await animate(Faces.DOWN);
      }, // rotate bottom counterclockwise wrt y
      face: "D"
    },
    70: { // "F".charCodeAt()
      action: async () => {
        await animate(Faces.FRONT);
      }, // rotate front clockwise wrt z
      face: "F"
    },
    66: { // "B".charCodeAt()
      action: async () => {
        await animate(Faces.BACK);
      }, // rotate back counterclockwise wrt z
      face: "B"
    },
    49: { // "1".charCodeAt()
      action: () => { setReverse(false); }
    },
    50: { // "2".charCodeAt()
      action: () => { setReverse(true); }
    },
    90: { action: () => {}} // "z".charCodeAt()
};
  
let lastKeyTime = 0;
const keyCooldown = 100;
async function onDocumentKeyDown(event) {
    var keyCode = event.which;
    if (!keyActions[keyCode]) return; // ignore non-relevant keys

    // Enforce cooldown period except for key combinations with ctrl, or 1 and 2 (direction change)
    const currentTime = Date.now();
    if (!event.ctrlKey && keyCode != 49 && keyCode != 50 && (currentTime - lastKeyTime < keyCooldown)) {
        showAlert("Too quick!", "in cooldown.");
        return;
    }
    lastKeyTime = currentTime;
    // Ignore manual moves when in autosolve mode
    if (isAutoSolveMode()) {
        showAlert("In autosolve mode:", "manual moves are temporarily disabled.");
        return;
    }
    const { action, face } = keyActions[keyCode];
    // special combo for undo: ctrl+z
    if (event.ctrlKey && keyCode == 90) Promise.resolve(undoLastMove());
    if (face != null) {
      let move = face;
      if (isReverseMode()) { // add apostrophe
          move += "'";
      }
      Promise.all([
        displayMove(move),
        await action(),
        await saveMove(move, true)
      ])
      .catch((error) => {
        console.error("Error handling keyboard move actions:", error);
      });
    } else Promise.resolve(action());
    
};

export function initKeyHandler() {
  document.addEventListener("keydown", onDocumentKeyDown, false);
}

export async function handleMove(move, saveSession) {
  const keyCode = move.charAt(0).charCodeAt();
  setReverse(move.charAt(1) === "'");
  if (keyActions[keyCode]) {
      const { action } = keyActions[keyCode];
      Promise.all([
        await action(),
        await saveMove(move, saveSession)
      ])
      .catch((error) => {
        console.error("Error handling move actions:", error);
        return false;
      });
  }
  return true; // success
}
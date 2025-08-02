import { isReverseMode, setAutoSolve, setReverse } from './modes.js';
import { postMove } from './api.js';
import { handleMove } from './keyHandler.js'

// Saves actions to persistent storage and possibly session storage, for undo/redo and solve functionality
// move is a string in Rubik notation, session is a boolean
// sessionStorage["keyEventHistory"] is already initialized and is a list of moves in Rubik notation (string)
// reverse is the most recent state of the reverse toggle, after the effects of the key event is applied
export async function saveMove(move, session) {
  if (session) {
    let historyString = sessionStorage.getItem("keyEventHistory");
    let history = historyString ? JSON.parse(historyString) : [];
    if (history.length > 10) // set a limit to the number of saved moves
        history.shift() // get rid of oldest move
    history.push(move)
    sessionStorage.setItem("keyEventHistory", JSON.stringify(history));
  }
  await postMove(move);
}

// Undo the previous action by reversing the move
export async function undoLastMove() {
    let historyString = sessionStorage.getItem("keyEventHistory");
    if (!historyString) return; // nothing to undo
    let history = JSON.parse(historyString);
    if (history.length > 0) {
        let lastMove = history.pop();
        let oppMove = lastMove.endsWith("'") ? lastMove.slice(0, -1) : lastMove + "'";
        sessionStorage.setItem("keyEventHistory", JSON.stringify(history));
        try {
          const success = await makeAutoMove(oppMove, false);
          return success;
        } catch {
          sessionStorage.setItem("keyEventHistory", JSON.stringify(history.push(lastMove))); // restore history
          return false;
        }
    }
}
window.undoLastMove = undoLastMove;


// Called by the autosolver / undo/redo.
// Takes in move (string) in Rubik's notation, both forward and reverse e.g. R, R'
// saveSession is a boolean: whether to save move to session history
export async function makeAutoMove(move, saveSession) {
  const prevReverseMode = isReverseMode();
  let success;
  try {
    setAutoSolve(true);
    await handleMove(move, saveSession);
    setReverse(prevReverseMode);
    setAutoSolve(false);
  }
  catch (error) {
    console.error("Error executing move:", error);
    success = false;
  }
  return success;
}
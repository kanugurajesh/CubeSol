// Updated solutionService.js - Works with local tracking

import { resetMode } from './modes.js';
import { makeAutoMove } from './action_utils.js'; 
import { getSolution } from './api.js';

async function handleSolve() {
    const solutionDisplay = document.getElementById("solution-display");
    solutionDisplay.textContent = "";

    let data = await getSolution();
    let solutionMoves = data.solutionString.split(" ").filter(m => m); // Filter empty strings
    let parsedMoves = data.parsedMoves;

    if (parsedMoves.length === 0) {
        solutionDisplay.textContent = "Already solved!";
        setTimeout(() => {
            solutionDisplay.textContent = "";
        }, 2000);
        return;
    }

    const solveButton = document.getElementById("solve-button");
    const originalContent = solveButton.innerHTML;
    
    // Show analyzing phase
    solveButton.innerHTML = '<span class="loading-spinner"></span>Analyzing...';
    solveButton.disabled = true;
    
    await new Promise(resolve => setTimeout(resolve, 600));
    
    solveButton.innerHTML = '<span class="loading-spinner"></span>Solving...';

    let i = 0;
    async function nextMove() {
        if (i < parsedMoves.length) {
            const move = parsedMoves[i];
            if (typeof move === "string") {
                solutionDisplay.textContent += " " + solutionMoves[i];
                await makeAutoMove(move, false); // Don't save solution moves
            } else if (Array.isArray(move) && move.length === 2) {
                solutionDisplay.textContent += " " + solutionMoves[i];
                await makeAutoMove(move[0], false);
                await makeAutoMove(move[1], false);
            }
            i++;
            nextMove();
        } else {
            resetMode();
            
            // Restore button
            solveButton.innerHTML = originalContent;
            solveButton.disabled = false;
            
            // Show completion
            solutionDisplay.textContent = "Solved!";
            setTimeout(() => {
                solutionDisplay.textContent = "";
            }, 2000);
        }
    }
    
    nextMove();
}

window.handleSolve = handleSolve;
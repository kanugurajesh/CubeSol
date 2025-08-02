import { handleMove } from './keyHandler.js';
import { isAutoSolveMode } from './modes.js';
import { displayMove } from './ui.js';

// All possible cube moves
const CUBE_MOVES = ['R', 'L', 'U', 'D', 'F', 'B', 'M'];
const MOVE_MODIFIERS = ['', "'"];  // Normal and reverse moves

let isScrambling = false;

/**
 * Generates a random sequence of cube moves
 * @param {number} count - Number of moves to generate
 * @returns {string[]} Array of move strings
 */
function generateRandomMoves(count) {
    const moves = [];
    let lastMove = null;
    
    for (let i = 0; i < count; i++) {
        let move, face, modifier;
        
        // Avoid consecutive moves on the same face
        do {
            face = CUBE_MOVES[Math.floor(Math.random() * CUBE_MOVES.length)];
            modifier = MOVE_MODIFIERS[Math.floor(Math.random() * MOVE_MODIFIERS.length)];
            move = face + modifier;
        } while (lastMove && lastMove.charAt(0) === face);
        
        moves.push(move);
        lastMove = move;
    }
    
    return moves;
}

/**
 * Executes a scramble sequence
 * @param {number} minMoves - Minimum number of moves
 * @param {number} maxMoves - Maximum number of moves
 */
export async function executeScramble(minMoves, maxMoves) {
    // Prevent scrambling during auto-solve or another scramble
    if (isAutoSolveMode() || isScrambling) {
        console.log("Scramble blocked: already in autosolve mode or scrambling");
        return;
    }
    
    isScrambling = true;
    
    // Generate random number of moves within range
    const moveCount = Math.floor(Math.random() * (maxMoves - minMoves + 1)) + minMoves;
    const moves = generateRandomMoves(moveCount);
    
    console.log(`Starting scramble with ${moveCount} moves:`, moves.join(' '));
    
    // Update scramble button to show progress
    const scrambleButton = document.getElementById('scramble-button');
    const originalContent = scrambleButton.innerHTML;
    scrambleButton.innerHTML = '<span class="loading-spinner"></span>Scrambling...';
    scrambleButton.disabled = true;
    
    // Show scramble info
    const actionDisplay = document.getElementById('action-display');
    actionDisplay.textContent = `Scrambling: ${moveCount} moves`;
    
    try {
        // Execute moves one by one with delay
        for (let i = 0; i < moves.length; i++) {
            const move = moves[i];
            
            // Update progress display
            actionDisplay.textContent = `Scrambling: ${i + 1}/${moveCount}`;
            
            // Execute the move (this will update cube state and track the move)
            await handleMove(move, true);
            
            // Small delay between moves to make it visible
            await new Promise(resolve => setTimeout(resolve, 200));
        }
        
        // Show completion message
        actionDisplay.textContent = `Scramble complete: ${moveCount} moves`;
        setTimeout(() => {
            actionDisplay.textContent = '';
        }, 2000);
        
        console.log("Scramble completed successfully");
        
    } catch (error) {
        console.error("Error during scramble:", error);
        actionDisplay.textContent = 'Scramble failed';
        setTimeout(() => {
            actionDisplay.textContent = '';
        }, 2000);
    } finally {
        // Restore scramble button
        scrambleButton.innerHTML = originalContent;
        scrambleButton.disabled = false;
        isScrambling = false;
    }
}

/**
 * Check if currently scrambling
 * @returns {boolean}
 */
export function isScrambleMode() {
    return isScrambling;
}

// Make executeScramble available globally for HTML onclick
window.executeScramble = executeScramble;
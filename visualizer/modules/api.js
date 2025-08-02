// Local move tracker
const LocalMoveTracker = {
    moves: [],
    
    addMove(move) {
        this.moves.push(move);
    },
    
    reset() {
        this.moves = [];
    },
    
    getSolution() {
        const solution = [];
        // Reverse the moves
        for (let i = this.moves.length - 1; i >= 0; i--) {
            const move = this.moves[i];
            // Invert the move
            if (move.endsWith("'")) {
                solution.push(move.slice(0, -1));
            } else if (move.endsWith("2")) {
                solution.push(move);
            } else {
                solution.push(move + "'");
            }
        }
        return this.optimizeSequence(solution);
    },
    
    optimizeSequence(moves) {
        const optimized = [];
        
        for (let i = 0; i < moves.length; i++) {
            if (optimized.length === 0) {
                optimized.push(moves[i]);
                continue;
            }
            
            const last = optimized[optimized.length - 1];
            const current = moves[i];
            
            if (last[0] === current[0]) {
                const combined = this.combineMoves(last, current);
                if (combined === null) {
                    optimized.pop();
                } else if (combined) {
                    optimized[optimized.length - 1] = combined;
                } else {
                    optimized.push(current);
                }
            } else {
                optimized.push(current);
            }
        }
        
        return optimized;
    },
    
    combineMoves(move1, move2) {
        const face = move1[0];
        const rules = {
            [`${face},${face}`]: `${face}2`,
            [`${face},${face}'`]: null,
            [`${face}',${face}`]: null,
            [`${face}',${face}'`]: `${face}2`,
            [`${face}2,${face}`]: `${face}'`,
            [`${face}2,${face}'`]: `${face}`,
            [`${face},${face}2`]: `${face}'`,
            [`${face}',${face}2`]: `${face}`,
            [`${face}2,${face}2`]: null
        };
        
        const key = `${move1},${move2}`;
        return rules.hasOwnProperty(key) ? rules[key] : false;
    }
};

export async function postMove(move) {
    // Just track the move locally
    LocalMoveTracker.addMove(move);
    return Promise.resolve();
}

export async function getSolution() {
    const solution = LocalMoveTracker.getSolution();
    
    // Format the response like the backend would
    const parsedMoves = solution.map(move => {
        if (move.endsWith("2")) {
            // Double moves need to be split into two single moves
            const base = move.slice(0, -1);
            return [base, base];
        }
        return move;
    });
    
    return {
        solutionString: solution.join(" "),
        parsedMoves: parsedMoves
    };
}

export function resetBackendState() {
    // Just reset the local tracker
    LocalMoveTracker.reset();
    return Promise.resolve();
}
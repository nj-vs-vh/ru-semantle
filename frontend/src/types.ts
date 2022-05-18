export interface WordGuess {
    word: string,
    similarity: number,
    rating?: number,
    local_coords?: [number, number],
}


type WordGuessError = string;


export type WordGuessResult = WordGuess | WordGuessError;

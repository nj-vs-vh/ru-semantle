export interface WordGuessInput {
    word: string;
    idx?: number;
}

export interface WordGuess extends WordGuessInput {
    similarity: number,
    rating?: number,
    local_coords?: [number, number],
    guessedAt?: string,
}

type WordGuessError = string;

export type WordGuessResult = WordGuess | WordGuessError;


interface GameConfig {
    n_top_words: number,
    local_dimensions: number,
}

interface GameClues {
    next_to_answer_similarity: number,
    word_10_similarity: number,
    word_100_similarity: number,
    last_top_word_similarity: number,
}

export interface GameMetadata {
    game_number: number,
    config: GameConfig,
    clues: GameClues,
}


export enum GameState {
    IN_PROGRESS = 1,
    WON,
    LOST,
}

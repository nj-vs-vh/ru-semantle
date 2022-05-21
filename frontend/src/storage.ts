import type { WordGuess } from "./types";


const STORED_GAME_NUMBER_KEY = "storedGameNumber";
const STORED_WORD_GUESSES_KEY = "storedGuesses";


export function ensureUpToDateStoredData(gameNumber: number) {
    const storedGameNumber = parseInt(window.localStorage.getItem(STORED_GAME_NUMBER_KEY));
    if (storedGameNumber != gameNumber) {
        window.localStorage.setItem(STORED_GAME_NUMBER_KEY, gameNumber.toString());
        window.localStorage.setItem(STORED_WORD_GUESSES_KEY, JSON.stringify([]));
    }
}


export function loadStoredWordGuesses(): WordGuess[] {
    const wordGuessesDump = window.localStorage.getItem(STORED_WORD_GUESSES_KEY);
    return JSON.parse(wordGuessesDump)
}


export function addWordGuessToStorage(wordGuess: WordGuess) {
    const storedWordGuesses = loadStoredWordGuesses();
    storedWordGuesses.push(wordGuess);
    const wordGuessesDump = JSON.stringify(storedWordGuesses);
    window.localStorage.setItem(STORED_WORD_GUESSES_KEY, wordGuessesDump);
}

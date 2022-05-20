import type { WordGuess, WordGuessResult } from "./types";


// @ts-ignore
const baseUrl = buildTimeReplacedIsProduction ? "https://ru-semantle.herokuapp.com" : "http://localhost:8088";


export async function guessWord(word: string): Promise<WordGuessResult> {
    console.log(`Guessing "${word}" (${baseUrl})...`)
    try {
        const resp = await fetch(
            `${baseUrl}/guess`,
            {
                method: "POST",
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ guess: word })
            }
        )
        if (resp.ok) {
            const wg: WordGuess = JSON.parse(await resp.text());
            return wg;
        } else {
            return await resp.text();
        }
    } catch (error) {
        console.warn(`Error fetching data: ${error}`)
        return "Network error, please check your connection!";
    }
}


export async function getRandomWords(): Promise<string[] | null> {
    console.log(`Fetching random words (${baseUrl})...`)
    try {
        const resp = await fetch(`${baseUrl}/random-words`)
        if (resp.ok) {
            console.log("OK")
            return JSON.parse(await resp.text());
        } else {
            console.log(`Error: ${await resp.text()}`)
            return null;
        }
    } catch (error) {
        console.warn(`Error fetching data: ${error}`)
        return null;
    }
}

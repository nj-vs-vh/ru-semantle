import type { WordGuess, WordGuessResult } from "./types";

const baseUrl = "https://ru-semantle.herokuapp.com";


export async function guess(word: string): Promise<WordGuessResult> {
    const resp = await fetch(
        `${baseUrl}/guess`,
        {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ guess: word })
        }
    )
    if (!resp.ok) {
        const wg: WordGuess = JSON.parse(await resp.text());
        return wg;
    } else {
        return await resp.text();
    }
}

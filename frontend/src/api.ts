import type { GameMetadata, WordGuess, WordGuessResult } from "./types";


// @ts-ignore
const baseUrl = buildTimeReplacedIsProduction ? "https://ru-semantle.herokuapp.com" : "http://localhost:8088";

const networkErrorMessage = "Ошибка подключения, попробуйте обновить страницу!";


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
        const respText = await resp.text();
        if (resp.ok) {
            const wg: WordGuess = JSON.parse(respText);
            return wg;
        } else {
            return respText;
        }
    } catch (error) {
        console.warn(`Error fetching data: ${error}`)
        return networkErrorMessage;
    }
}


export async function getRandomWords(): Promise<string[] | null> {
    console.log(`Fetching random words (${baseUrl})...`)
    try {
        const resp = await fetch(`${baseUrl}/random-words`)
        const respText = await resp.text();
        if (resp.ok) {
            console.log("OK")
            return JSON.parse(respText);
        } else {
            console.log(`Error: ${respText}`)
            return null;
        }
    } catch (error) {
        console.warn(`Error fetching data: ${error}`)
        return null;
    }
}


export async function getMetadata(): Promise<GameMetadata | string> {
    console.log(`Fetching metadata (${baseUrl})...`)
    try {
        const resp = await fetch(`${baseUrl}/metadata`)
        const respText = await resp.text();
        if (resp.ok) {
            console.log("OK")
            return JSON.parse(respText);
        } else {
            console.log(`Error: ${respText}`)
            return respText;
        }
    } catch (error) {
        console.warn(`Error fetching data: ${error}`)
        return networkErrorMessage;
    }
}

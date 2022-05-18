import { Word } from "./types";

const baseUrl = "https://ru-semantle.herokuapp.com";


export async function guess(word: string) {
    const resp = await fetch(
        `${baseUrl}/guess`,
        {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ guess: word })
        }
    )
    if (!resp.ok) {
        // TODO
    }
}


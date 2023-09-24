import type { GameMetadata, WordGuess, WordGuessResult } from "./types";
import { sleep, toIsoStringTz } from "./utils";

let baseUrl: string;
try {
  // @ts-ignore
  baseUrl = buildTimeReplacedBaseUrl;
} catch {
  // @ts-ignore
  baseUrl = "http://localhost:8088";
}

const networkErrorMessage = "Ошибка подключения, попробуйте обновить страницу!";

export async function guessWord(
  word: string,
  guessIdx?: number
): Promise<WordGuessResult> {
  // await sleep(5);   // for loading spinner test
  console.log(`Guessing "${word}" (${baseUrl})...`);
  try {
    const resp = await fetch(`${baseUrl}/guess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ guess: word }),
    });
    const respText = await resp.text();
    if (resp.ok) {
      const wg: WordGuess = JSON.parse(respText);
      wg.guessedAt = toIsoStringTz(new Date());
      wg.idx = guessIdx;
      return wg;
    } else {
      return respText;
    }
  } catch (error) {
    console.warn(`Error fetching data: ${error}`);
    return networkErrorMessage;
  }
}

export async function getRandomWords(): Promise<string[] | null> {
  console.log(`Fetching random words (${baseUrl})...`);
  try {
    const resp = await fetch(`${baseUrl}/random-words`);
    const respText = await resp.text();
    if (resp.ok) {
      console.log("OK");
      return JSON.parse(respText);
    } else {
      console.log(`Error: ${respText}`);
      return null;
    }
  } catch (error) {
    console.warn(`Error fetching data: ${error}`);
    return null;
  }
}

export async function getMetadata(): Promise<GameMetadata | string> {
  // await sleep(5);   // for loading spinner test
  // return "Example error message";  // for error display test
  console.log(`Fetching metadata (${baseUrl})...`);
  try {
    const resp = await fetch(`${baseUrl}/metadata`);
    const respText = await resp.text();
    if (resp.ok) {
      console.log("OK");
      return JSON.parse(respText);
    } else {
      console.log(`Error: ${respText}`);
      return respText;
    }
  } catch (error) {
    console.warn(`Error fetching data: ${error}`);
    return networkErrorMessage;
  }
}

export async function getHint(
  currentBestRating: number | null
): Promise<WordGuess | null> {
  console.log(`Fetching hint (better than ${currentBestRating})...`);
  try {
    const resp = await fetch(`${baseUrl}/hint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ current_best_rating: currentBestRating }),
    });
    const respText = await resp.text();
    if (resp.ok) {
      console.log("OK");
      return JSON.parse(respText);
    } else {
      console.log(`Error: ${respText}`);
      return null;
    }
  } catch (error) {
    console.warn(`Error fetching data: ${error}`);
    return null;
  }
}

export async function getTopWords(): Promise<WordGuess[] | null> {
  // await sleep(5);   // for loading spinner test
  // return "Example error message";  // for error display test
  console.log(`Fetching top words (${baseUrl})...`);
  try {
    const resp = await fetch(`${baseUrl}/give-up`);
    const respText = await resp.text();
    if (resp.ok) {
      console.log("OK");
      return JSON.parse(respText);
    } else {
      console.log(`Error: ${respText}`);
      return null;
    }
  } catch (error) {
    console.warn(`Error fetching data: ${error}`);
    return null;
  }
}

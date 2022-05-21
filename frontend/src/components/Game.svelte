<script lang="ts">
    import GuessInput from "./GuessInput.svelte";
    import GameIntro from "./GameIntro.svelte";
    import WordRow from "./WordRow.svelte";
    import NewGuessedWord from "./NewGuessedWord.svelte";
    
    import { setContext } from "svelte";

    import {
        ensureUpToDateStoredData,
        loadStoredWordGuesses,
        saveWordGuessesToStorage,
    } from "../storage";
    import type { GameMetadata, WordGuess } from "../types";
import WordTable from "./WordTable.svelte";

    export let metadata: GameMetadata;

    setContext("metadata", metadata);

    let currentWordGuesses: WordGuess[] = [];

    $: sortedWordGuesses = [...currentWordGuesses].sort(
        (wg1, wg2) => wg2.similarity - wg1.similarity
    );

    ensureUpToDateStoredData(metadata.game_number);

    // TEMP
    currentWordGuesses.push({ word: "пример", similarity: 0.1142514 });
    currentWordGuesses.push({
        word: "пыриться",
        similarity: 0.3011,
        rating: 523,
    });
    currentWordGuesses.push({
        word: "глаза",
        similarity: 0.2455,
        rating: 1000,
    });
    currentWordGuesses.push({
        word: "глядеть",
        similarity: 0.6945,
        rating: 46,
    });
    currentWordGuesses.push({
        word: "смотреть",
        similarity: 0.7254,
        rating: 2,
    });
    currentWordGuesses.push({
        word: "наблюдать",
        similarity: 1.0,
        rating: 1,
    });
    currentWordGuesses.push({ word: "картошка", similarity: 0.021111 });
    saveWordGuessesToStorage(currentWordGuesses);
    // END TEMP

    currentWordGuesses = loadStoredWordGuesses();

    let newGuessedWord: string = null;

    function onWordGuessed(e: CustomEvent<{ word: string }>) {
        newGuessedWord = e.detail.word;
    }
</script>

<div class="page-text-block top-margin">
    <GameIntro />
    <GuessInput on:guess={onWordGuessed} />
    {#if newGuessedWord != null}
        <NewGuessedWord guessedWord={newGuessedWord} />
    {/if}
    <WordTable>
        {#each sortedWordGuesses as wordGuess (wordGuess.word)}
            <WordRow {wordGuess} />
        {/each}
    </WordTable>
</div>

<style>
    .top-margin {
        margin-top: 10vh;
    }
</style>

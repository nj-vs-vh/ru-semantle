<script lang="ts">
    import GuessInput from "./GuessInput.svelte";
    import GameIntro from "./GameIntro.svelte";
    import WordRow from "./WordRow.svelte";

    import { getMetadata } from "../api";
    import {
        ensureUpToDateStoredData,
        loadStoredWordGuesses,
        saveWordGuessesToStorage,
    } from "../storage";
    import type { GameMetadata, WordGuess } from "../types";

    export let metadata: GameMetadata;

    let currentWordGuesses: WordGuess[] = [];

    $: sortedWordGuesses = [...currentWordGuesses].sort(
        (wg1, wg2) => wg2.similarity - wg1.similarity
    );

    ensureUpToDateStoredData(metadata.game_number);

    // TEMP
    currentWordGuesses.push({ word: "пример", similarity: 0.1 });
    currentWordGuesses.push({
        word: "пыриться",
        similarity: 0.3,
        rating: 523,
    });
    currentWordGuesses.push({
        word: "глядеть",
        similarity: 0.6,
        rating: 46,
    });
    currentWordGuesses.push({ word: "картошка", similarity: 0.02 });
    saveWordGuessesToStorage(currentWordGuesses);
    // END TEMP

    currentWordGuesses = loadStoredWordGuesses();

    // let guessedWord = "";
    function onWordGuessed(e: CustomEvent<{ word: string }>) {
        // guessedWord = e.detail.word;
        // window.alert(guessedWord);
    }
</script>

<div class="page-text-block top-margin">
    <GameIntro gameMetadata={metadata} />
    <GuessInput on:guess={onWordGuessed} />
    <!-- TODO: GuessedWordElement -->
    <table>
        {#each sortedWordGuesses as wordGuess (wordGuess.word)}
            <WordRow {wordGuess} />
        {/each}
    </table>
</div>

<style>
    .top-margin {
        margin-top: 10vh;
    }

    table {
        margin-top: 20px;
        width: 100%;
        font-size: large;
        border-collapse: collapse;
    }
</style>

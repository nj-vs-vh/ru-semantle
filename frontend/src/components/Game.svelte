<script lang="ts">
    import UserInput from "./UserInput.svelte";
    import GameIntro from "./GameIntro.svelte";
    import NewGuessedWord from "./NewGuessedWord.svelte";
    import WordRow from "./words/WordRow.svelte";
    import WordTable from "./words/WordTable.svelte";

    import { setContext } from "svelte";

    import {
        ensureUpToDateStoredData,
        loadStoredWordGuesses,
        saveWordGuessesToStorage,
    } from "../storage";
    import type { GameMetadata, WordGuess } from "../types";

    export let metadata: GameMetadata;

    setContext("metadata", metadata);

    let currentWordGuesses: WordGuess[] = [];

    $: sortedWordGuesses = [...currentWordGuesses].sort(
        (wg1, wg2) => wg2.similarity - wg1.similarity
    );

    ensureUpToDateStoredData(metadata.game_number);

    currentWordGuesses = loadStoredWordGuesses();
    console.log(currentWordGuesses);

    let newGuessedWord: string = null;

    function onNewWordGuessed(e: CustomEvent<{ word: string }>) {
        newGuessedWord = e.detail.word;
    }

    function onSuccessfulWordGuess(e: CustomEvent<{ wg: WordGuess }>) {
        const newWordGuess = e.detail.wg;
        const currentWords = currentWordGuesses.map((wg) => wg.word)
        if (!currentWords.includes(newWordGuess.word)) {
            currentWordGuesses = [...currentWordGuesses, e.detail.wg];
            saveWordGuessesToStorage(currentWordGuesses);
        }
    }
</script>

<div class="page-text-block top-margin">
    <GameIntro />
    <UserInput on:guess={onNewWordGuessed} />
    {#if newGuessedWord != null}
        <NewGuessedWord
            guessedWord={newGuessedWord}
            on:successfulWordGuess={onSuccessfulWordGuess}
        />
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

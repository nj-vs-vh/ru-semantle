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
    import { getHint, getTopWords } from "../api";
import { gameWonStore } from "../stores";

    export let metadata: GameMetadata;
    setContext("metadata", metadata);

    let currentWordGuesses: WordGuess[] = [];
    $: sortedWordGuesses = [...currentWordGuesses].sort(
        (wg1, wg2) => wg2.similarity - wg1.similarity
    );
    ensureUpToDateStoredData(metadata.game_number);
    currentWordGuesses = loadStoredWordGuesses();
    if (currentWordGuesses.length > 0 && Math.min.apply(Math, currentWordGuesses.map(wg => wg.rating)) === 1)
        gameWonStore.set(true);

    let newGuessedWord: string = null;
    function onNewWordGuessed(e: CustomEvent<{ word: string }>) {
        newGuessedWord = e.detail.word;
    }

    function onSuccessfulWordGuess(newWordGuess: WordGuess) {
        const currentWords = currentWordGuesses.map((wg) => wg.word);
        if (!currentWords.includes(newWordGuess.word)) {
            currentWordGuesses = [...currentWordGuesses, newWordGuess];
            saveWordGuessesToStorage(currentWordGuesses);
        }
    }

    function onHint(e: CustomEvent<null>) {
        let currentBestRating: number | undefined | null;
        try {
            currentBestRating = sortedWordGuesses[0].rating;
        } catch {
            currentBestRating = null;
        }
        getHint(currentBestRating).then((wg) => {
            if (wg !== null) onSuccessfulWordGuess(wg);
        });
    }

    function giveUp(allTopWords: boolean) {
        gameWonStore.set(true);
        getTopWords().then((topWords) => {
            if (topWords !== null) {
                if (allTopWords)
                    for (let tw of topWords) {
                        onSuccessfulWordGuess(tw);
                    }
                else onSuccessfulWordGuess(topWords[0]);
            }
        });
    }
</script>

<div class="page-text-block top-margin">
    <GameIntro />
    <UserInput
        on:guess={onNewWordGuessed}
        on:hint={onHint}
        on:giveUp={() => giveUp(false)}
        on:showAllTop={() => giveUp(true)}
    />
    {#if newGuessedWord != null}
        <NewGuessedWord
            guessedWord={newGuessedWord}
            on:successfulWordGuess={(e) => onSuccessfulWordGuess(e.detail.wg)}
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

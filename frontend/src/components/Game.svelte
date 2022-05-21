<script lang="ts">
    import UserInput from "./UserInput.svelte";
    import GameIntro from "./GameInfo.svelte";
    import NewGuessedWord from "./NewGuessedWord.svelte";
    import WordRow from "./words/WordRow.svelte";
    import WordTable from "./words/WordTable.svelte";
    import MapModal from "./modals/MapModal.svelte";
    
    import { getContext } from "svelte";

    import {
        ensureUpToDateStoredData,
        loadStoredWordGuesses,
        addWordGuessToStorage,
    } from "../storage";
    import type { GameMetadata, WordGuess } from "../types";
    import { getHint, getTopWords } from "../api";
    import { isGameWonStore } from "../stores";
import HistoryModal from "./modals/HistoryModal.svelte";

    let metadata: GameMetadata = getContext("metadata");

    const { open } = getContext("simple-modal");

    let currentWordGuesses: WordGuess[] = [];
    $: sortedWordGuesses = [...currentWordGuesses].sort(
        (wg1, wg2) => wg2.similarity - wg1.similarity
    );
    ensureUpToDateStoredData(metadata.game_number);
    currentWordGuesses = loadStoredWordGuesses();
    if (
        currentWordGuesses.length > 0 &&
        Math.min.apply(
            Math,
            currentWordGuesses
                .map((wg) => wg.rating)
                .filter((r) => r !== undefined)
        ) === 1
    )
        isGameWonStore.set(true);

    let newGuessedWord: string = null;
    function onNewWordGuessed(e: CustomEvent<{ word: string }>) {
        newGuessedWord = e.detail.word;
    }

    function onSuccessfulWordGuess(
        newWordGuess: WordGuess,
        persist: boolean = true
    ) {
        const currentWords = currentWordGuesses.map((wg) => wg.word);
        if (!currentWords.includes(newWordGuess.word)) {
            currentWordGuesses = [...currentWordGuesses, newWordGuess];
            if (persist) {
                addWordGuessToStorage(newWordGuess);
            }
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
        isGameWonStore.set(true);
        getTopWords().then((topWords) => {
            if (topWords !== null) {
                if (allTopWords)
                    for (let tw of topWords) {
                        onSuccessfulWordGuess(tw, false);
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
        on:map={() => open(MapModal, {words: currentWordGuesses})}
        on:history={() => open(HistoryModal, {words: currentWordGuesses})}
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
        margin-top: 3vh;
    }
</style>

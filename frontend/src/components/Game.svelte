<script lang="ts">
    import UserInput from "./UserInput.svelte";
    import GameIntro from "./GameInfo.svelte";
    import NewGuessedWord from "./NewGuessedWord.svelte";
    import WordRow from "./words/WordRow.svelte";
    import WordTable from "./words/WordTable.svelte";
    import MapModal from "./modals/MapModal.svelte";
    import HistoryModal from "./modals/HistoryModal.svelte";

    import { getContext } from "svelte";

    import {
        ensureUpToDateStoredData,
        loadStoredWordGuesses,
        addWordGuessToStorage,
    } from "../storage";
    import {
        GameMetadata,
        GameState,
        WordGuess,
        WordGuessInput,
    } from "../types";
    import { getHint, getTopWords } from "../api";
    import { gameStateStore } from "../stores";

    let metadata: GameMetadata = getContext("metadata");

    const { open } = getContext("simple-modal");

    // main app state: list of current WordGuess object
    let currentWordGuesses: WordGuess[] = [];
    $: sortedWordGuesses = [...currentWordGuesses].sort(
        (wg1, wg2) => wg2.similarity - wg1.similarity
    );
    ensureUpToDateStoredData(metadata.game_number);
    currentWordGuesses = loadStoredWordGuesses();
    let withHints =
        currentWordGuesses.filter((wg) => wg.idx === undefined).length > 0;

    // inferring game state from word guesses
    if (currentWordGuesses.length > 0) {
        const wgs = [...currentWordGuesses].sort(
            (wg1, wg2) => wg2.similarity - wg1.similarity
        );
        if (wgs[0].rating === 1)
            gameStateStore.set(
                wgs[0].idx !== undefined ? GameState.WON : GameState.LOST
            );
    }

    let nGuessesUntilAnswer: number;
    $: {
        let nextToAnswerIdx =
            currentWordGuesses.findIndex((wg) => wg.rating === 1) + 1;
        if (nextToAnswerIdx === 0) nextToAnswerIdx = currentWordGuesses.length;

        nGuessesUntilAnswer = currentWordGuesses
            .slice(0, nextToAnswerIdx)
            .filter((wg) => wg.idx !== undefined).length;
    }

    // current user input state storage
    let wordGuessInput: WordGuessInput | null = null;
    let alreadyExistingWordGuess: WordGuess | null = null;
    let nextGuessIdx: number =
        1 +
        Math.max.apply(
            Math,
            currentWordGuesses
                .map((wg) => wg.idx)
                .filter((idx) => idx !== undefined)
        );
    if (nextGuessIdx < 1) {
        nextGuessIdx = 1;
    }

    function onNewWordGuessInput(e: CustomEvent<{ word: string }>) {
        const newGuessedWord = e.detail.word;
        alreadyExistingWordGuess =
            currentWordGuesses.filter(
                (wg) => wg.word == newGuessedWord.toLowerCase()
            )[0] || null;
        wordGuessInput = { word: newGuessedWord, idx: nextGuessIdx };
    }

    function onSuccessfulWordGuess(
        newWordGuess: WordGuess,
        persist: boolean = true
    ) {
        console.log("Successfull word guess fired")
        const currentWords = currentWordGuesses.map((wg) => wg.word);
        if (!currentWords.includes(newWordGuess.word)) {
            console.log("New word not met before")
            nextGuessIdx += 1;
            currentWordGuesses = [...currentWordGuesses, newWordGuess];
            if (persist) {
                console.log("Presisting")
                addWordGuessToStorage(newWordGuess);
            }
        }
    }

    function fakeWordGuessInput(wg: WordGuess) {
        alreadyExistingWordGuess = wg;
        wordGuessInput = { word: wg.word };
    }

    function onHint(e: CustomEvent<null>) {
        let currentBestRating: number | undefined | null;
        try {
            currentBestRating = sortedWordGuesses[0].rating;
        } catch {
            currentBestRating = null;
        }
        getHint(currentBestRating).then((wg) => {
            if (wg !== null) fakeWordGuessInput(wg);
        });
    }

    function giveUp(allTopWords: boolean) {
        getTopWords().then((topWords) => {
            if (topWords !== null) {
                if (allTopWords)
                    for (let tw of topWords) {
                        onSuccessfulWordGuess(tw, false);
                    }
                else fakeWordGuessInput(topWords[0]);
            }
        });
    }
</script>

<div class="page-text-block">
    <GameIntro nGuesses={nGuessesUntilAnswer} {withHints} />
    <UserInput
        on:guess={onNewWordGuessInput}
        on:hint={onHint}
        on:giveUp={() => giveUp(false)}
        on:showAllTop={() => giveUp(true)}
        on:map={() => open(MapModal, { words: currentWordGuesses })}
        on:history={() => open(HistoryModal, { words: currentWordGuesses })}
    />
    {#if wordGuessInput != null}
        <NewGuessedWord
            input={wordGuessInput}
            {alreadyExistingWordGuess}
            on:successfulWordGuess={(e) => onSuccessfulWordGuess(e.detail.wg)}
        />
    {/if}
    <WordTable header={true}>
        {#each sortedWordGuesses as wordGuess (wordGuess.word)}
            <WordRow {wordGuess} />
        {/each}
    </WordTable>
</div>

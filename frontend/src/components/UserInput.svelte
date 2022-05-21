<script lang="ts">
    import { getRandomWords } from "../api";
    import { sleep } from "../utils";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher<{ guess: { word: string } }>();

    let currentGuess = "";
    let suggestion = "";

    async function typeSuggestion(newSuggestion: string) {
        const betweenStrokesSec = 0.1;
        while (!newSuggestion.includes(suggestion)) {
            suggestion = suggestion.slice(0, suggestion.length - 1);
            await sleep(betweenStrokesSec);
        }
        let idx = suggestion.length;
        while (idx < newSuggestion.length) {
            suggestion += newSuggestion[idx];
            await sleep(betweenStrokesSec);
            idx += 1;
        }
    }

    let suggestionsLoopRunning = true;

    async function suggestWords() {
        let randomWords: string[] = [];
        while (true) {
            await sleep(60);
            suggestionsLoopRunning = true;
            while (true) {
                // suggestions loop, interrupted by new guesses
                await sleep(10);
                if (randomWords.length == 0) {
                    randomWords = await getRandomWords();
                    if (randomWords === null) {
                        return; // error occured, something's wrong
                    }
                }
                if (!suggestionsLoopRunning) {
                    break;
                }
                await typeSuggestion(`например, ${randomWords.pop()}`);
            }
        }
    }

    suggestWords();

    function wordGuessed() {
        if (currentGuess.length > 0) {
            dispatch("guess", {
                word: currentGuess,
            });
            currentGuess = "";
            suggestion = "";
            suggestionsLoopRunning = false;
        }
    }
</script>

<div class="container">
    <input
        type="text"
        id="lname"
        name="guess"
        bind:value={currentGuess}
        on:keyup={({ key }) => key === "Enter" && wordGuessed()}
        placeholder={suggestion}
    />
    <div id="buttons-container">
        <button
            class="btn-primary"
            id="guessButton"
            type="submit"
            on:click|preventDefault={wordGuessed}
        >
            Проверить
        </button>
        <button id="unwrapOptionsButton">▼</button>
    </div>
</div>

<style>
    .container {
        display: flex;
        flex-wrap: wrap;
        width: 100%;
    }

    input {
        flex-grow: 50;
        min-height: 1.5em;
        margin-top: 10px;
        font-size: large;
        margin-right: 4px;
        min-width: 0;
        text-overflow: ellipsis;
    }

    input::placeholder {
        color: rgb(179, 179, 179);
    }

    #buttons-container {
        margin-top: 10px;
        font-size: medium;
        min-width: 20%;
        display: flex;
        flex-wrap: nowrap;
        flex-grow: 10;
    }

    button {
        margin-right: 4px;
    }
    #guessButton {
        min-width: 70%;
        flex-grow: 3;
    }

    #unwrapOptionsButton {
        border: none;
        background-color: transparent;
        color: #1d2ad5;
        border: #1d2ad5 1px solid;
        border-radius: 5px;
    }
</style>

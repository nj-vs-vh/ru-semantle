<script lang="ts">
    import UserMenu from "./menu/UserMenu.svelte";
    import { createEventDispatcher } from "svelte";
    import { sleep } from "../utils";
    import { getRandomWords } from "../api";

    const dispatch =
        createEventDispatcher<{ guess: { word: string }; hint: null }>();

    let currentGuess = "";
    let suggestion = "";
    let suggestionsLoopRunning = true;

    async function typeSuggestion(newSuggestion: string) {
        const betweenStrokesSec = 0.1;
        while (!newSuggestion.includes(suggestion)) {
            suggestion = suggestion.slice(0, suggestion.length - 1);
            if (!suggestionsLoopRunning) {
                suggestion = "";
                return;
            }
            await sleep(betweenStrokesSec);
            if (!suggestionsLoopRunning) {
                suggestion = "";
                return;
            }
        }
        let idx = suggestion.length;
        while (idx < newSuggestion.length) {
            suggestion += newSuggestion[idx];
            if (!suggestionsLoopRunning) {
                suggestion = "";
                return;
            }
            await sleep(betweenStrokesSec);
            if (!suggestionsLoopRunning) {
                suggestion = "";
                return;
            }
            idx += 1;
        }
    }

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

    let userMenuWrapped = true;
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
        <button
            id="unwrapOptionsButton"
            class="btn-secondary"
            on:click={() => {
                userMenuWrapped = !userMenuWrapped;
            }}>{userMenuWrapped ? "▽" : "△"}</button
        >
    </div>
</div>
<UserMenu wrapped={userMenuWrapped} on:hint on:giveUp on:showAllTop on:history on:map />

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
</style>

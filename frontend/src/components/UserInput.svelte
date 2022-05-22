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

    const checkSuggestionsLoopRunning = () => {
        if (!suggestionsLoopRunning) {
            suggestion = "";
            throw Error;
        }
    };

    async function typeSuggestion(newSuggestion: string) {
        const betweenStrokesSec = 0.1;
        while (!newSuggestion.includes(suggestion)) {
            suggestion = suggestion.slice(0, suggestion.length - 1);
            checkSuggestionsLoopRunning();
            await sleep(betweenStrokesSec);
            checkSuggestionsLoopRunning();
        }
        let idx = suggestion.length;
        while (idx < newSuggestion.length) {
            suggestion += newSuggestion[idx];
            checkSuggestionsLoopRunning();
            await sleep(betweenStrokesSec);
            checkSuggestionsLoopRunning();
            idx += 1;
        }
    }

    async function suggestWords() {
        let randomWords: string[] = [];
        while (true) {
            await sleep(90);
            suggestionsLoopRunning = true;
            try {
                while (true) {
                    await sleep(15);
                    if (randomWords.length == 0) {
                        randomWords = await getRandomWords();
                        if (randomWords === null) {
                            return;
                        }
                    }
                    checkSuggestionsLoopRunning();
                    await typeSuggestion(`например, ${randomWords.pop()}`);
                    checkSuggestionsLoopRunning();
                }
            } catch (Error) {
                continue;
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
<UserMenu
    wrapped={userMenuWrapped}
    on:hint
    on:giveUp
    on:showAllTop
    on:history
    on:map
/>

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
        padding-left: 0.5em;
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
        margin-right: 6px;
    }
    #guessButton {
        min-width: 70%;
        min-height: 5vh;
        flex-grow: 3;
    }
</style>

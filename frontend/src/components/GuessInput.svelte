<script lang="ts">
    import { getRandomWords } from "../api";
    import { sleep } from "../utils";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher<{guess:{word:string}}>();

    let currentGuess = "";
    let suggestion = "";

    async function typeSuggestion(newSuggestion: string) {
        const betweenStrokesSec = 0.1;
        while (!newSuggestion.includes(suggestion)) {
            suggestion = suggestion.slice(0, suggestion.length - 1);
            await sleep(betweenStrokesSec);
        };
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
            await sleep(10);
            suggestionsLoopRunning = true;
            while (true) {  // suggestions loop, interrupted by new guesses
                await sleep(10);
                if (randomWords.length == 0) {
                    randomWords = await getRandomWords();
                    if (randomWords === null) {
                        return;  // error occured, something's wrong
                    }
                }
                if (!suggestionsLoopRunning)  {
                    break;
                }
                await typeSuggestion(`например, ${randomWords.pop()}`)
            }
        }
    }
    
    suggestWords();

    function guessWordClicked(event: MouseEvent) {
        dispatch("guess", {
            word: currentGuess,
        });
        currentGuess = "";
        suggestion = "";
        suggestionsLoopRunning = false;
    }

</script>

<form class="container">
    <input
        type="text"
        id="lname"
        name="guess"
        bind:value={currentGuess}
        placeholder={suggestion}
    />
    <button
        class="btn-primary"
        type="submit"
        on:click|preventDefault={guessWordClicked}
    >
        Проверить
    </button>
</form>

<style>
    .container {
        display: flex;
        flex-wrap: wrap;
    }
    input {
        flex-grow: 10;
        min-height: 1.5em;
        margin-top: 10px;
        font-size: larger;
        margin-right: 5px;
        min-width: 0;
        text-overflow: ellipsis;
    }

    input::placeholder {
        color: rgb(179, 179, 179);
    }

    button {
        flex-grow: 3;
        margin-top: 10px;
        font-size: medium;
        margin-right: 5px;
        min-width: 20%;
    }
</style>

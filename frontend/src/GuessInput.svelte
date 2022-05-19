<script lang="ts">
    import { getRandomWords, guessWord } from "./api";
    import { sleep } from "./utils";

    let currentGuess = "";
    let suggestion = "";
    const GUESS_BUTTON_READY_TEXT = "Проверить";
    let guessButtonText = GUESS_BUTTON_READY_TEXT;

    async function suggestWords() {
        await sleep(30);
        let randomWords: string[] = [];
        // let randomWords: string[] = ["раз", "два", "пример"];
        while (true) {
            await sleep(10);
            if (randomWords.length == 0) {
                randomWords = await getRandomWords();
                if (randomWords === null) {
                    return;
                }
            }
            const newSuggestion = randomWords.pop();
            suggestion = "например, ";
            for (let ch of newSuggestion) {
                suggestion += ch;
                await sleep(0.1);
            }
        }
    }

    function animateLoading() {
        guessButtonText = " ";
        return setInterval(() => {
            guessButtonText =
                guessButtonText.length < 3 ? guessButtonText + "." : " ";

        }, 0.2 * 1000);
    }

    function guessWordClicked(event: MouseEvent) {
        const timerId = animateLoading();
        guessWord(currentGuess).then(
            () => {
                clearInterval(timerId);
            }
        );
    }

    suggestWords();
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
        {guessButtonText}
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

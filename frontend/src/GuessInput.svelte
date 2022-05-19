<script lang="ts">
    import { getRandomWords } from "./api";
    import { sleep } from "./utils";
    
    let guess = "";

    let suggestion = "";

    async function suggestWords() {
        await sleep(1);
        let randomWords: string[] = [];
        while (true) {
            await sleep(5);
            if (randomWords.length == 0) {
                randomWords = await getRandomWords();
                if (randomWords === null) {
                    return;
                }
            }
            suggestion = randomWords.pop();
        }
    }

    function alert(event: MouseEvent) {
        window.alert(guess);
    }

    suggestWords();
</script>

<form class="container">
    <input type="text" id="lname" name="guess" bind:value={guess} placeholder={suggestion}>
    <button class="btn-primary" type="submit" on:click|preventDefault={alert}>Проверить</button>
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
        margin-right: 10px;
    }

    input::placeholder {
        color: rgb(179, 179, 179);
    }

    button {
        margin-top: 10px;
        font-size: medium;
    }
</style>

<script lang="ts">
    import { guessWord } from "../api";
    import Error from "./Error.svelte";
    import Spinner from "./Spinner.svelte";
    import WordRow from "./WordRow.svelte";
    import WordTable from "./WordTable.svelte";

    export let guessedWord: string;

    $: wordGuessPromise = guessWord(guessedWord);
</script>

{#await wordGuessPromise}
    <Spinner sizeEm={1} />
{:then wordGuessResult}
    {#if typeof wordGuessResult === "string"}
        <Error errorMessage={wordGuessResult} />
    {:else}
        <WordTable>
            <WordRow wordGuess={wordGuessResult} />
        </WordTable>
    {/if}
{/await}

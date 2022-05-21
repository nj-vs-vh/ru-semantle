<script lang="ts">
    import { guessWord } from "../api";
    import Error from "./Error.svelte";
    import Spinner from "./Spinner.svelte";
    import WordRow from "./WordRow.svelte";
    import WordTable from "./WordTable.svelte";
    import { createEventDispatcher } from "svelte";
    import type { WordGuess } from "../types";

    const dispatch =
        createEventDispatcher<{ successfulWordGuess: { wg: WordGuess } }>();

    export let guessedWord: string;

    $: wordGuessPromise = guessWord(guessedWord).then((wgr) => {
        console.log(wgr);
        if (typeof wgr !== "string") {
            dispatch("successfulWordGuess", { wg: wgr });
        }
        return wgr;
    });
</script>

{#await wordGuessPromise}
    <Spinner sizeEm={1} />
{:then wordGuessResult}
    {#if typeof wordGuessResult === "string"}
        <Error errorMessage={wordGuessResult} />
    {:else if wordGuessResult.rating != 1}
        <WordTable>
            <WordRow wordGuess={wordGuessResult} />
        </WordTable>
    {/if}
{/await}

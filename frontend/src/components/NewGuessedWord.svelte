<script lang="ts">
    import Error from "./shared/Error.svelte";
    import Spinner from "./shared/Spinner.svelte";
    import WordRow from "./words/WordRow.svelte";
    import WordTable from "./words/WordTable.svelte";

    import { guessWord } from "../api";
    import { createEventDispatcher } from "svelte";
    import type { WordGuess } from "../types";
    import { gameWonStore } from "../stores";

    const dispatch =
        createEventDispatcher<{ successfulWordGuess: { wg: WordGuess } }>();

    export let guessedWord: string;

    $: wordGuessPromise = guessWord(guessedWord).then((wgr) => {
        if (typeof wgr !== "string") {
            dispatch("successfulWordGuess", { wg: wgr });
        }
        return wgr;
    });

    async function gameWon() {
        gameWonStore.set(true);
        // @ts-ignore
        return window.confetti({ particleCount: 100, spread: 70 });
    }
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
    {:else}
        {#await gameWon()}
            <div />
        {/await}
    {/if}
{/await}

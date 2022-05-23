<script lang="ts">
    import Error from "./shared/Error.svelte";
    import Spinner from "./shared/Spinner.svelte";
    import WordRow from "./words/WordRow.svelte";
    import WordTable from "./words/WordTable.svelte";

    import { guessWord } from "../api";
    import { createEventDispatcher } from "svelte";
    import { GameState, WordGuess } from "../types";
    import { gameStateStore } from "../stores";

    const dispatch =
        createEventDispatcher<{ successfulWordGuess: { wg: WordGuess } }>();

    export let guessedWord: string;
    export let currentGuessIdx: number;
    export let alreadyExistingWordGuess: WordGuess | null = null;

    $: wordGuessPromise =
        alreadyExistingWordGuess === null
            ? guessWord(guessedWord, currentGuessIdx).then((wgr) => {
                  if (typeof wgr !== "string") {
                      dispatch("successfulWordGuess", { wg: wgr });
                  }
                  return wgr;
              })
            : new Promise<WordGuess>((resolve, reject) =>
                  resolve(alreadyExistingWordGuess)
              );

    async function answerFound(byUser: boolean) {
        gameStateStore.set(byUser ? GameState.WON : GameState.LOST);
        if (byUser) {
            // @ts-ignore
            return window.confetti({ particleCount: 100, spread: 70 });
        }
    }
</script>

{#await wordGuessPromise}
    <Spinner sizeEm={1} />
{:then wordGuessResult}
    {#if typeof wordGuessResult === "string"}
        <Error errorMessage={wordGuessResult} />
    {:else if wordGuessResult.rating != 1}
        <WordTable header={false}>
            <WordRow wordGuess={wordGuessResult} />
        </WordTable>
    {:else}
        {#await answerFound(wordGuessResult.idx !== undefined)}
            <div />
        {/await}
    {/if}
{/await}

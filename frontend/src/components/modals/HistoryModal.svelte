<script lang="ts">
    import { onMount } from "svelte";
    import Plotly from "plotly.js-dist";
    import type { WordGuess } from "../../types";

    export let words: WordGuess[];
    $: timestampedWords = words.filter((wg) => wg.guessedAt !== undefined);
    let plotlyCanvas: HTMLDivElement;

    onMount(() => {
        if (timestampedWords.length === 0) return;
        let dataset = {
            x: timestampedWords.map((wg) => wg.guessedAt),
            y: timestampedWords.map((wg) => wg.similarity),
            mode: "markers+text",
            type: "scatter",
            textposition: "bottom center",
            text: timestampedWords.map((wg) => `${wg.word}`),
            marker: { size: 12, color: "#1d2ad5" },
        };
        Plotly.newPlot(plotlyCanvas, [dataset], {
            margin: { b: 0, l: 0, r: 0, t: 0 },
        });
    });
</script>

<div>
    <h3>История</h3>
    {#if timestampedWords.length > 0}
        <div id="plotly" bind:this={plotlyCanvas} />
    {:else}
        <p>
            После того как вы проверите несколько догадок, здесь будет график
            изменения их подобия со временем.
        </p>
    {/if}
</div>

<style>
    #plotly {
        width: 100%;
        min-height: 600px;
    }
</style>

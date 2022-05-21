<script lang="ts">
    import { getContext, onMount } from "svelte";
    import Plotly from "plotly.js-dist";
    import type { GameMetadata, WordGuess } from "../../types";
    import { formatSimilarity } from "../../utils";

    export let words: WordGuess[];
    $: topWords = words
        .filter((wg) => wg.local_coords !== undefined)
        .sort((wg1, wg2) => wg1.rating - wg2.rating);
    let gameMetadata: GameMetadata = getContext("metadata");
    let plotlyCanvas: HTMLDivElement;

    onMount(() => {
        let datasets = [];
        if (topWords.length === 0 || topWords[0].rating > 1) {
            datasets.push({
                x: [0],
                y: [0],
                mode: "markers+text",
                type: "scatter",
                textposition: 'bottom center',
                text: ["???"],
                marker: { size: 12 },
            });
        }
        if (topWords.length > 0) {
            datasets.push({
                x: topWords.map((wg) => wg.local_coords[0]),
                y: topWords.map((wg) => wg.local_coords[1]),
                mode: "markers+text",
                type: "scatter",
                textposition: 'bottom center',
                text: topWords.map(
                    (wg) => `${wg.word} (${formatSimilarity(wg.similarity)})`
                ),
                marker: { size: 12 },
            });
        }
        Plotly.newPlot(plotlyCanvas, datasets, {
            xaxis: {
                range: [-1, 1],
            },
            yaxis: {
                range: [-1, 1],
            },
            // margin: { t: 0 },
        });
    });
</script>

<h3>Семантическая карта</h3>
<p>
    Слова из топ-{gameMetadata.config.n_top_words} наносятся на семантическую карту.
    С помощью PCA из семантических 300-векторов этих слов выделяются две
    главные компоненты и строятся в евклидовом пространстве (в узком конусе гиперсферы
    косинусная близость почти эквивалентна евклидовой). Такое радикальное снижение размерности
    объясняет всего порядка 10% вариации данных, но (иногда) позволяет визуализировать
    семантические кластеры слов.
</p>
<div id="plotly" bind:this={plotlyCanvas} />

<style>
    #plotly {
        width: 100%;
        min-height: 600px;
    }
</style>

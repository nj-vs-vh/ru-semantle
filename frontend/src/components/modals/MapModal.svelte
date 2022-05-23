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
        const isAnswerGuessed = topWords.length > 0 && topWords[0].rating === 1;
        let datasets = [];
        datasets.push({
            x: [0],
            y: [0],
            mode: "markers+text",
            name: "Загаданное слово",
            type: "scatter",
            showlegend: false,
            textposition: "bottom center",
            text: [isAnswerGuessed ? topWords[0].word : "?????"],
            marker: { size: 12, color: "black" },
        });
        if (topWords.length > 0) {
            const notAnswer = (wg: WordGuess) => wg.rating !== 1;
            datasets.push({
                x: topWords.filter(notAnswer).map((wg) => wg.local_coords[0]),
                y: topWords.filter(notAnswer).map((wg) => wg.local_coords[1]),
                type: "scatter",
                name: "",
                mode: "markers+text",
                showlegend: false,
                textposition: "bottom center",
                text: topWords
                    .filter(notAnswer)
                    .map(
                        (wg) =>
                            `${wg.word} (${formatSimilarity(wg.similarity, 0)})`
                    ),
                marker: { size: 10, color: "#1d2ad5" },
            });
        }
        Plotly.newPlot(plotlyCanvas, datasets, {
            xaxis: {
                range: [-1, 1],
            },
            yaxis: {
                range: [-1, 1],
            },
            margin: { b: 0, l: 0, r: 0, t: 0 },
        });
    });
</script>

<h3>Семантическая карта</h3>
<p>
    Слова из топ-{gameMetadata.config.n_top_words} наносятся на семантическую карту.
    С помощью PCA из семантических 300-векторов этих слов выделяются две главные
    компоненты и строятся в евклидовом пространстве (в узком конусе гиперсферы косинусная
    близость почти эквивалентна евклидовой). Такое радикальное снижение размерности
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

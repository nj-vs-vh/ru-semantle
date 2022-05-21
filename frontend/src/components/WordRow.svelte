<script lang="ts">
    import WordRating from "./WordRating.svelte";
    import type { WordGuess } from "../types";
    import { formatSimilarity } from "../utils";

    export let wordGuess: WordGuess;
</script>


<tr>
    <td>
        {wordGuess.word}
    </td>
    <td class="align-right">
        {formatSimilarity(wordGuess.similarity)}
    </td>
    <td class="last-col">
        <WordRating rating={wordGuess.rating} />
    </td>
</tr>

<style>
	tr:nth-child(even) {background-color: #f5f5ff;}

    td {
        border-right: solid #ddd 1px;
        padding: 0 2vw;
        text-align: left;
    }

    td.last-col {
        border: none;
    }

    td.align-right {
        text-align: right;
    }
</style>

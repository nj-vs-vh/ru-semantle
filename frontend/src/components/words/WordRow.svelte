<script lang="ts">
    import WordRating from "./WordRating.svelte";
    import type { WordGuess } from "../../types";
    import { formatSimilarity } from "../../utils";

    export let wordGuess: WordGuess;
</script>


<tr>
    <td id="index">
        {wordGuess.idx || "×"}
    </td>
    <td id="word">
        {wordGuess.word}
    </td>
    <td id="similarity">
        {formatSimilarity(wordGuess.similarity)}
    </td>
    <td id="rating">
        <WordRating rating={wordGuess.rating} />
    </td>
</tr>

<style>
	tr:nth-child(even) {background-color: #fafaff;}

    td {
        border-right: solid #ddd 1px;
        padding: 0 1vw;
        text-align: left;
        font-size: 1rem;
    }

    #index {
        width: 10%;
        text-overflow: clip;
        overflow-wrap: break-word;
        text-align: center;
    }

    #word {
        width: 40%;
    }

    #similarity {
        width: 20%;
        text-align: right;
    }
    #rating {
        border: none;
    }

</style>

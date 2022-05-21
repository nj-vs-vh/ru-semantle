<script lang="ts">
    import type { WordGuess } from "../types";

    export let wordGuess: WordGuess;
</script>


<tr>
    <td>
        {wordGuess.word}
    </td>
    <td>
        {wordGuess.similarity}
    </td>
</tr>

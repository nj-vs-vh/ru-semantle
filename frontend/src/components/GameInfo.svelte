<script lang="ts">
    import { getContext } from "svelte";

    import type { GameMetadata } from "../types";
    import { formatSimilarity } from "../utils";

    let gameMetadata: GameMetadata = getContext("metadata");
</script>

<div>
    <h2>
        Игра #{gameMetadata.game_number}
    </h2>
    <p>
        Ранжировано топ-<strong>{gameMetadata.config.n_top_words}</strong> слов.
    </p>
    <p>
        Ближайшее к правильному ответу слово расположено на расстоянии
        <strong>
            {formatSimilarity(
                gameMetadata.clues.next_to_answer_similarity
            )}</strong
        >, десятое —
        <strong>
            {formatSimilarity(gameMetadata.clues.word_10_similarity)}</strong
        >, сотое —
        <strong>
            {formatSimilarity(gameMetadata.clues.word_100_similarity)}</strong
        >,
        последнее ({gameMetadata.config.n_top_words}-e) —
        <strong>
            {formatSimilarity(
                gameMetadata.clues.last_top_word_similarity
            )}</strong
        >.
    </p>
</div>

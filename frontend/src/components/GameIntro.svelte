<script lang="ts">
    import type { GameMetadata } from "../types";
    import { formatSimilarity } from "../utils";

    export let gameMetadata: GameMetadata;
</script>

<div>
    <h2>
        #{gameMetadata.game_number}
    </h2>
    <p>
        Ранжирование приводится для топ-<strong>{gameMetadata.config.n_top_words}</strong> слов.
    </p>
    <p>
        Ближайшее к правильному ответу слово расположено на расстоянии
        <strong>{formatSimilarity(gameMetadata.clues.next_to_answer_similarity)}</strong>, 10-e —
        <strong>{formatSimilarity(gameMetadata.clues.word_10_similarity)}</strong>,
        100-e —
        <strong>{formatSimilarity(gameMetadata.clues.word_100_similarity)}</strong>,
        {gameMetadata.config.n_top_words}-e —
        <strong>{formatSimilarity(gameMetadata.clues.last_top_word_similarity)}</strong>.
    </p>
</div>

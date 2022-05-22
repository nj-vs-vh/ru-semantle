<script lang="ts">
    import { getContext } from "svelte";

    import { gameStateStore } from "../stores";
    import { GameMetadata, GameState } from "../types";
    import { formatSimilarity } from "../utils";

    let gameMetadata: GameMetadata = getContext("metadata");

    let gameState: GameState;
    gameStateStore.subscribe((newGameState) => {
        gameState = newGameState;
    });

    export let nGuesses: number | null;
    export let withHints: boolean | null;
</script>

<div>
    <h2>
        <span>Слово #{gameMetadata.game_number}</span>
        {#if gameState === GameState.WON}
            <span class="game-result win">
                отгадано с <strong>{nGuesses}</strong> попытки {withHints
                    ? "(хотя и с подсказками)"
                    : ""}
            </span>
        {:else if gameState === GameState.LOST}
            <span class="game-result lose">
                не отгадано с <strong>{nGuesses}</strong> попытки
            </span>
        {/if}
    </h2>
    <p>
        Ранжирован топ-<strong>{gameMetadata.config.n_top_words}</strong> слов.
    </p>
    <p>
        Ближайшее к правильному ответу слово имеет сходство
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
        >, {gameMetadata.config.n_top_words}-e —
        <strong>
            {formatSimilarity(
                gameMetadata.clues.last_top_word_similarity
            )}</strong
        >.
    </p>
</div>

<style>
    .game-result {
        font-weight: 300;
        margin-left: 0.5em;
        border: 1px solid black;
        padding: 0.2em 0.6em;
        border-radius: 5px;
    }

    .win {
        border-color: #3fa83a;
        background-color: #edfbf7;
    }

    .lose {
        border-color: #ff6c89;
        background-color: #fffaf9;
    }
</style>

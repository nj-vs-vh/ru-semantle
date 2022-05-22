<script lang="ts">
    import { createEventDispatcher, getContext } from "svelte";
    import { gameStateStore } from "../../stores";
    import { GameMetadata, GameState } from "../../types";

    export let wrapped: boolean;

    let metadata: GameMetadata = getContext("metadata");
    let isGameFinished: boolean;
    gameStateStore.subscribe((gameState) => {
        isGameFinished = gameState !== GameState.IN_PROGRESS;
    });

    const dispatch = createEventDispatcher<{
        hint: null;
        giveUp: null;
        showAllTop: null;
        history: null;
        map: null;
    }>();

    $: additionalClass = wrapped ? "wrapped" : "unwrapped";
</script>

<div class="container {additionalClass}">
    <button class="btn-secondary" on:click={() => dispatch("hint")}
        >Подсказка</button
    >
    <button
        class="btn-secondary"
        on:click={() => dispatch(isGameFinished ? "showAllTop" : "giveUp")}
    >
        {isGameFinished
            ? `Топ-${metadata.config.n_top_words}`
            : "Сдаться"}
    </button>
    <button class="btn-secondary" on:click={() => dispatch("history")}
        >История</button
    >
    <button class="btn-secondary" on:click={() => dispatch("map")}>Карта</button
    >
</div>

<style>
    .wrapped {
        max-height: 0;
    }

    .unwrapped {
        max-height: 10vh;
    }

    .container {
        overflow-y: hidden;
        width: 100%;
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        transition: max-height 0.3s linear;
    }

    button {
        width: 23%;
        min-height: 5vh;
    }
</style>

<script lang="ts">
    import { createEventDispatcher, getContext } from "svelte";
import { gameWonStore } from "../../stores";
    import type { GameMetadata } from "../../types";

    export let wrapped: boolean;

    let metadata: GameMetadata = getContext("metadata");
    let isGameWon;
    gameWonStore.subscribe(v => {isGameWon = v});

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
    <button class="btn-secondary" on:click={() => dispatch(isGameWon ? "showAllTop" : "giveUp")}>
        {isGameWon
            ? `Посмотреть топ-${metadata.config.n_top_words}`
            : "Сдаться"
        }
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
    }
</style>

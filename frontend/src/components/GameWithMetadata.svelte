<script lang="ts">
    import Game from "./Game.svelte";
    import Modal from "svelte-simple-modal";

    import { setContext } from "svelte";
    
    import type { GameMetadata } from "../types";

    export let metadata: GameMetadata;
    setContext("metadata", metadata);
</script>

<Modal styleCloseButton={{ boxShadow: "none" }}>
    <Game />
</Modal>

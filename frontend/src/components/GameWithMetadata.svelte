<script lang="ts">
    import Game from "./Game.svelte";
    import Modal from "svelte-simple-modal";

    import { setContext } from "svelte";

    export let metadata;
    setContext("metadata", metadata);
</script>

<Modal styleCloseButton={{ boxShadow: "none" }}>
    <Game />
</Modal>

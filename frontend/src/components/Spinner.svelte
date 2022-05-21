<script lang="ts">
    import { Shadow } from "svelte-loading-spinners";

    export let sizeEm: number;
</script>

<div class="container">
    <Shadow color={"#1d2ad5"} size={sizeEm} unit="rem" />
</div>

<style>
    .container {
        margin-top: 30px;
    }
</style>

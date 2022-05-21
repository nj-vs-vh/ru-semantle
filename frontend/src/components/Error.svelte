<script lang="ts">
    export let errorMessage: string;
</script>

<div>
    <span>{errorMessage}</span>
</div>

<style>
    div {
        padding: 10px 15px;
        margin: 5px;
        background-color: rgb(255, 239, 238);
        border: 2px solid rgb(254, 121, 114);
        border-radius: 5px;
    }
</style>

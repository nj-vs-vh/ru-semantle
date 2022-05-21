<script lang="ts">
    export let header: boolean;
</script>

<table>
    {#if header}
        <tr>
            <th style="text-align: center;">№</th>
            <th style="text-align: left;">слово</th>
            <th style="text-align: right;">сходство</th>
            <th style="text-align: center; border: none;">ранг</th>
        </tr>
    {/if}
    <slot />
</table>

<style>
    th {
        border-right: solid #ddd 1px;
        padding: 0 2vw;
        text-overflow: ellipsis;
        font-weight: 300;
        font-size: small;
        padding-bottom: 5px;
    }
    table {
        margin-top: 30px;
        width: 100%;
        font-size: large;
        border-collapse: collapse;
        overflow-wrap: anywhere;
    }
</style>

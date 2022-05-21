<script lang="ts">
	import { getMetadata } from "./api";
	import Game from "./components/Game.svelte";

	let metadataPromise = getMetadata();
</script>

<div class="page">
	{#await metadataPromise}
		Loading...
		<!-- TODO: nice spinner here -->
	{:then metadataResult}
		{#if typeof metadataResult === "string"}
			{metadataResult}
			<!-- TODO: error banner component -->
		{:else}
			<Game metadata={metadataResult} />
		{/if}
	{/await}
</div>

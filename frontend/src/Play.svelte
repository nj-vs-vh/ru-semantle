<script lang="ts">
	import Game from "./components/Game.svelte";
	import Spinner from "./components/Spinner.svelte";
	import Screen from "./components/Screen.svelte";
	import Error from "./components/Error.svelte";
	import { getMetadata } from "./api";

	let metadataPromise = getMetadata();
</script>

<div class="page">
	{#await metadataPromise}
		<Screen>
			<Spinner sizeEm={3}/>
		</Screen>
	{:then metadataResult}
		{#if typeof metadataResult === "string"}
			<Screen>
				<Error errorMessage={metadataResult}/>
			</Screen>
		{:else}
			<Game metadata={metadataResult} />
		{/if}
	{/await}
</div>

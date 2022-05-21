<script lang="ts">
	import Spinner from "./components/shared/Spinner.svelte";
	import Screen from "./components/shared/Screen.svelte";
	import Error from "./components/shared/Error.svelte";
	import GameWithMetadata from "./components/GameWithMetadata.svelte";

	import { getMetadata } from "./api";

	let metadataPromise = getMetadata();
</script>

<div class="page">
	{#await metadataPromise}
		<Screen>
			<Spinner sizeEm={3} />
		</Screen>
	{:then metadataResult}
		{#if typeof metadataResult === "string"}
			<Screen>
				<Error errorMessage={metadataResult} />
			</Screen>
		{:else}
			<GameWithMetadata metadata={metadataResult} />
		{/if}
	{/await}
</div>

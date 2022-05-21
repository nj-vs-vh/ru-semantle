<script lang="ts">
	import Game from "./components/Game.svelte";
	import Spinner from "./components/shared/Spinner.svelte";
	import Screen from "./components/shared/Screen.svelte";
	import Error from "./components/shared/Error.svelte";
	import Modal from "svelte-simple-modal";

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
			<Modal styleCloseButton={{boxShadow: "none"}}>
				<Game metadata={metadataResult} />
			</Modal>
		{/if}
	{/await}
</div>

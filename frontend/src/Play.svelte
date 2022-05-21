<script lang="ts">
	import GuessInput from "./components/GuessInput.svelte";
	import GameIntro from "./components/GameIntro.svelte";
	import { getMetadata } from "./api";

	let metadataPromise = getMetadata();

	// let guessedWord = "";
	function onWordGuessed(e: CustomEvent<{ word: string }>) {
		// guessedWord = e.detail.word;
		// window.alert(guessedWord);
	}
</script>

<div class="page">
	{#await metadataPromise}
		Loading...
		<!-- TODO: nice spinner here -->
	{:then metadataResult}
		{#if typeof(metadataResult) === 'string'}
			{metadataResult}
			<!-- TODO: error banner component -->
		{:else}
			<div class="page-text-block adaptive-top-margin">
				<GameIntro gameMetadata={metadataResult} />
				<GuessInput on:guess={onWordGuessed} />
			</div>
		{/if}
	{/await}
</div>

<style>
	.adaptive-top-margin {
		margin-top: 10vh;
	}
</style>

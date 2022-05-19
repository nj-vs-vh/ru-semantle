<script lang="ts">
	import GuessInput from "./GuessInput.svelte";

	let guessedWord = "";
	function onWordGuessed(e: CustomEvent<{word: string;}>) {
		guessedWord = e.detail.word;
		window.alert(guessedWord);
	}
</script>

<div class="page">
	<div class="page-text-block adaptive-top-margin">
		<GuessInput on:guess={onWordGuessed}/>
	</div>
	<span>{guessedWord}</span>
</div>

<style>
	.adaptive-top-margin {
		margin-top: 10vh;
	}
</style>

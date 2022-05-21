<script lang="ts">
    import { getContext } from "svelte";
    import type { GameMetadata } from "../types";
    import { pickRandom } from "../utils";

    export let rating: number | undefined;
    let gameMetadata: GameMetadata = getContext("metadata");

    const nEmojiInBackground = 6;
    let message = "холодно";
    let emojis = "❄️".repeat(nEmojiInBackground);
    let emojiSpanClass = "background";
    if (rating != undefined) {
        if (rating == 1) {
            message = "";
            emojis = pickRandom(["🎉", "✨", "💅", "💡"]).repeat(
                nEmojiInBackground
            );
            emojiSpanClass = "";
        } else {
            let ratingStr = rating.toString();
            // ratingStr = ratingStr.padStart(
            //     gameMetadata.config.n_top_words.toString().length,
            //     "_"
            // );
            message = `#${ratingStr}`;
            const fireness = (gameMetadata.config.n_top_words - rating + 1) / gameMetadata.config.n_top_words;
            const nFireEmoji = Math.ceil((nEmojiInBackground - 1) * fireness);
            emojis = "🔥".repeat(nFireEmoji) + "❄️".repeat(nEmojiInBackground - nFireEmoji);
        }
    }
</script>

<div class="container">
    <span class="{emojiSpanClass}">{emojis}</span>
    <span class="foreground">{message}</span>
</div>

<style>
    .container {
        position: relative;
        text-align: center;
        text-overflow: ellipsis;
    }
    .background {
        color: rgba(0, 0, 0, 0.2);
    }
    .foreground {
        width: 100%;
        position: absolute;
        top: 0;
        left: 0;
        bottom: 0;
        z-index: 1;
    }
</style>

import Play from './Play.svelte';
import Version from './Version.svelte';


const versionEl = document.getElementById("versionSpan");
if (versionEl !== null)
    new Version({target: versionEl})

const playPageEl = document.getElementById("playPageBody");
if (playPageEl !== null)
    new Play({target: playPageEl});

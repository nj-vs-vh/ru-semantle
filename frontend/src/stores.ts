import { writable } from 'svelte/store';
import { GameState } from './types';

export const gameStateStore = writable(GameState.IN_PROGRESS);

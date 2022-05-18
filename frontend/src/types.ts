export interface Word {
    word: string,
    similarity: number,
    rating?: number,
    local_coords?: [number, number],
}

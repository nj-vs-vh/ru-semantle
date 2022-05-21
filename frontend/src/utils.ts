export async function sleep(delaySec: number): Promise<undefined> {
    return new Promise(resolve => setTimeout(resolve, delaySec * 1000));
}


export function formatSimilarity(f: number): string {
    return (100 * f).toFixed(2)
}

export async function sleep(delaySec: number): Promise<undefined> {
    return new Promise(resolve => setTimeout(resolve, delaySec * 1000));
}


export function formatSimilarity(f: number): string {
    const symbolsAftreDecimalPoint = 2;
    return (100 * f).toFixed(symbolsAftreDecimalPoint);
}


export function pickRandom<T>(variants: T[]): T {
    const index = Math.floor(Math.random() * variants.length);
    return variants[index];
  }
  
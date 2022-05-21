export async function sleep(delaySec: number): Promise<undefined> {
    return new Promise(resolve => setTimeout(resolve, delaySec * 1000));
}


export function formatSimilarity(f: number, symbolsAfterDecimal: number = 2): string {
    return (100 * f).toFixed(symbolsAfterDecimal);
}


export function pickRandom<T>(variants: T[]): T {
    const index = Math.floor(Math.random() * variants.length);
    return variants[index];
}

export function toIsoStringTz(date: Date): string {
    const tzo = -date.getTimezoneOffset();
    const dif = tzo >= 0 ? '+' : '-';
    const pad = (num: number) => (num < 10 ? '0' : '') + num;

    return date.getFullYear() +
        '-' + pad(date.getMonth() + 1) +
        '-' + pad(date.getDate()) +
        'T' + pad(date.getHours()) +
        ':' + pad(date.getMinutes()) +
        ':' + pad(date.getSeconds()) +
        dif + pad(Math.floor(Math.abs(tzo) / 60)) +
        ':' + pad(Math.abs(tzo) % 60);
}


export async function sleep(delaySec: number): Promise<undefined> {
    return new Promise(resolve => setTimeout(resolve, delaySec * 1000));
}

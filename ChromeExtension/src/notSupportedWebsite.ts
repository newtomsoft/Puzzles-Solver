export function NotSupportedWebsite(urlHostName: string): void {
    const url = new URL(urlHostName);
    console.log(`${url.hostname} is not supported yet`);
    alert(`${url.hostname} is not supported yet`);
}
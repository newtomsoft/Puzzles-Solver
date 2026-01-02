export interface GridProvider {
    extract(html: string): any;
    [key: string]: any;
}

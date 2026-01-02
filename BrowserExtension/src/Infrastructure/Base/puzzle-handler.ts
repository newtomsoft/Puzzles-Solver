export interface PuzzleHandler {
    getType(): string;
    detect(url: string, html: string): boolean;
    extract(html: string, url: string): ExtractionResult;
    solve(extractionResult: ExtractionResult): Promise<any>;
    getSolutionDisplay(puzzleType: string, extractionResult: ExtractionResult, solution: any): string;
    getOrderedPath(solver: any, solution: any): any[] | null;
    getBlackCells(solution: any): any[] | null;
}

export interface ExtractionResult {
    grid: any;
    url?: string;
    extra?: any;
    [key: string]: any;
}

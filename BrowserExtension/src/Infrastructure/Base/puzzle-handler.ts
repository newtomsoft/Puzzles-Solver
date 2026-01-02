export interface PuzzleHandler {
    getType(): string;
    detect(url: string, html: string): boolean;
    extract(html: string, url: string): any;
    solve(ctx: any, extractionResult: any): Promise<any>;
    getSolutionDisplay(puzzleType: string, extractionResult: any, solution: any): string;
    getOrderedPath(solver: any, solution: any): any[] | null;
    getBlackCells(solution: any): any[] | null;
}

export interface ExtractionResult {
    grid: any;
    extra?: any;
}

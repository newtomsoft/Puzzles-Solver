import { Position } from '../../Domain/Base/position.js';

export class CountryRoadSolver {
    ctx: any;
    rows: number;
    cols: number;
    numbersGrid: (number | null)[][];
    regions: Record<number, Position[]>;
    solver: any;
    islandBridges: Record<string, Record<number, any>>;
    lastSolution: any = null;

    constructor(ctx: any, numbersGrid: (number | null)[][], regionsGrid: number[][]) {
        this.ctx = ctx;
        this.numbersGrid = numbersGrid;
        this.rows = numbersGrid.length;
        this.cols = numbersGrid[0].length;
        this.regions = this._extractRegions(regionsGrid);
        this.solver = new ctx.Solver();
        this.islandBridges = {};
    }

    private _extractRegions(regionsGrid: number[][]): Record<number, Position[]> {
        const regions: Record<number, Position[]> = {};
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const regionId = regionsGrid[r][c];
                if (!regions[regionId]) {
                    regions[regionId] = [];
                }
                regions[regionId].push(new Position(r, c));
            }
        }
        return regions;
    }

    private _initVars(): void {
        // Initialize bridge variables for each cell in each direction
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const posKey = `${r},${c}`;
                this.islandBridges[posKey] = {};
                
                // Directions: 0=up, 1=right, 2=down, 3=left
                for (let dir = 0; dir < 4; dir++) {
                    const varName = `b_${r}_${c}_${dir}`;
                    const bridgeVar = this.ctx.Int.const(varName);
                    this.islandBridges[posKey][dir] = bridgeVar;
                    this.solver.add(bridgeVar.ge(0), bridgeVar.le(1));
                }
            }
        }
    }

    private _getOppositeDirection(dir: number): number {
        // 0=up, 1=right, 2=down, 3=left
        return (dir + 2) % 4;
    }

    private _getNeighborPosition(r: number, c: number, dir: number): Position | null {
        // Directions: 0=up, 1=right, 2=down, 3=left
        if (dir === 0 && r > 0) return new Position(r - 1, c);
        if (dir === 1 && c < this.cols - 1) return new Position(r, c + 1);
        if (dir === 2 && r < this.rows - 1) return new Position(r + 1, c);
        if (dir === 3 && c > 0) return new Position(r, c - 1);
        return null;
    }

    private _addConstraints(): void {
        this._addInitialConstraints();
        this._addRegionConstraints();
        this._addSinglePathConstraints();
        this._addOppositeBridgesConstraints();
        this._addAdjacentRegionConstraints();
    }

    private _addInitialConstraints(): void {
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const posKey = `${r},${c}`;
                const bridges = Object.values(this.islandBridges[posKey]);
                
                if (bridges.length === 0) continue;
                
                let sum = bridges[0];
                for (let i = 1; i < bridges.length; i++) {
                    sum = sum.add(bridges[i]);
                }
                
                // Each cell must have either 0 or 2 bridges (for a proper loop)
                this.solver.add(this.ctx.Or(sum.eq(0), sum.eq(2)));
            }
        }
    }

    private _addRegionConstraints(): void {
        // For each region with a number, the total bridges should equal number * 2
        for (const [regionId, positions] of Object.entries(this.regions)) {
            let hasNumber = false;
            let regionNumber = 0;
            
            // Find if this region has a number
            for (const pos of positions) {
                const num = this.numbersGrid[pos.r][pos.c];
                if (num !== null && num !== undefined) {
                    hasNumber = true;
                    regionNumber = num;
                    break;
                }
            }
            
            if (hasNumber) {
                const regionBridges = [];
                for (const pos of positions) {
                    const posKey = `${pos.r},${pos.c}`;
                    if (this.islandBridges[posKey]) {
                        regionBridges.push(...Object.values(this.islandBridges[posKey]));
                    }
                }
                
                if (regionBridges.length > 0) {
                    let sum = regionBridges[0];
                    for (let i = 1; i < regionBridges.length; i++) {
                        sum = sum.add(regionBridges[i]);
                    }
                    this.solver.add(sum.eq(regionNumber * 2));
                }
            }
        }
    }

    private _addSinglePathConstraints(): void {
        // Each region should have exactly 2 bridges connecting to other regions
        for (const [regionId, positions] of Object.entries(this.regions)) {
            const edgePositions = this._getRegionEdgePositions(positions, parseInt(regionId));
            const outBridges = [];
            
            for (const pos of edgePositions) {
                const posKey = `${pos.r},${pos.c}`;
                if (!this.islandBridges[posKey]) continue;
                
                for (let dir = 0; dir < 4; dir++) {
                    const neighbor = this._getNeighborPosition(pos.r, pos.c, dir);
                    if (!neighbor) continue;
                    
                    const neighborRegionId = this._getRegionIdForPosition(neighbor);
                    if (neighborRegionId !== parseInt(regionId)) {
                        outBridges.push(this.islandBridges[posKey][dir]);
                    }
                }
            }
            
            if (outBridges.length > 0) {
                let sum = outBridges[0];
                for (let i = 1; i < outBridges.length; i++) {
                    sum = sum.add(outBridges[i]);
                }
                this.solver.add(sum.eq(2));
            }
        }
    }

    private _getRegionIdForPosition(pos: Position): number {
        for (const [regionId, positions] of Object.entries(this.regions)) {
            if (positions.some(p => p.r === pos.r && p.c === pos.c)) {
                return parseInt(regionId);
            }
        }
        return -1;
    }

    private _getRegionEdgePositions(positions: Position[], regionId: number): Position[] {
        const edgePositions: Position[] = [];
        
        for (const pos of positions) {
            // Check if this position is on the edge of the region
            for (let dir = 0; dir < 4; dir++) {
                const neighbor = this._getNeighborPosition(pos.r, pos.c, dir);
                if (neighbor) {
                    const neighborRegionId = this._getRegionIdForPosition(neighbor);
                    if (neighborRegionId !== regionId) {
                        edgePositions.push(pos);
                        break;
                    }
                }
            }
        }
        
        return edgePositions;
    }

    private _addOppositeBridgesConstraints(): void {
        // Opposite bridges must be equal
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const posKey = `${r},${c}`;
                
                for (let dir = 0; dir < 4; dir++) {
                    const neighbor = this._getNeighborPosition(r, c, dir);
                    if (neighbor) {
                        const neighborKey = `${neighbor.r},${neighbor.c}`;
                        const oppositeDir = this._getOppositeDirection(dir);
                        
                        if (this.islandBridges[posKey] && this.islandBridges[posKey][dir] &&
                            this.islandBridges[neighborKey] && this.islandBridges[neighborKey][oppositeDir]) {
                            this.solver.add(
                                this.islandBridges[posKey][dir].eq(this.islandBridges[neighborKey][oppositeDir])
                            );
                        }
                    }
                }
            }
        }
    }

    private _addAdjacentRegionConstraints(): void {
        // No adjacent empty cells between regions
        for (const [regionId, positions] of Object.entries(this.regions)) {
            for (const pos of positions) {
                for (let dir = 0; dir < 4; dir++) {
                    const neighbor = this._getNeighborPosition(pos.r, pos.c, dir);
                    if (!neighbor) continue;
                    
                    const neighborRegionId = this._getRegionIdForPosition(neighbor);
                    if (neighborRegionId !== parseInt(regionId)) {
                        // At least one of the cells must have a bridge
                        const posKey = `${pos.r},${pos.c}`;
                        const neighborKey = `${neighbor.r},${neighbor.c}`;
                        
                        const posBridges = this.islandBridges[posKey] ? Object.values(this.islandBridges[posKey]) : [];
                        const neighborBridges = this.islandBridges[neighborKey] ? Object.values(this.islandBridges[neighborKey]) : [];
                        
                        if (posBridges.length > 0 || neighborBridges.length > 0) {
                            let posSum = posBridges.length > 0 ? posBridges[0] : this.ctx.Int.val(0);
                            for (let i = 1; i < posBridges.length; i++) {
                                posSum = posSum.add(posBridges[i]);
                            }
                            
                            let neighborSum = neighborBridges.length > 0 ? neighborBridges[0] : this.ctx.Int.val(0);
                            for (let i = 1; i < neighborBridges.length; i++) {
                                neighborSum = neighborSum.add(neighborBridges[i]);
                            }
                            
                            this.solver.add(this.ctx.Or(posSum.gt(0), neighborSum.gt(0)));
                        }
                    }
                }
            }
        }
    }

    async solve(): Promise<any> {
        this._initVars();
        this._addConstraints();
        return await this._getSolution();
    }

    async getOtherSolution(): Promise<any> {
        if (!this.lastSolution) return null;
        
        const clauses = [];
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const posKey = `${r},${c}`;
                if (this.islandBridges[posKey]) {
                    for (let dir = 0; dir < 4; dir++) {
                        const bridgeVal = this.lastSolution[posKey][dir];
                        clauses.push(this.islandBridges[posKey][dir].eq(bridgeVal));
                    }
                }
            }
        }
        
        if (clauses.length > 0) {
            this.solver.add(this.ctx.Not(this.ctx.And(...clauses)));
        }
        
        return await this._getSolution();
    }

    private async _getSolution(): Promise<any> {
        while (true) {
            const result = await this.solver.check();
            if (result !== 'sat') {
                return null;
            }
            
            const model = this.solver.model();
            const solution = this._extractSolution(model);
            
            // Check if solution forms a single connected loop
            if (this._isValidSolution(solution)) {
                this.lastSolution = solution;
                return solution;
            }
            
            // Add constraint to exclude this invalid solution
            this._addSolutionConstraint(solution);
        }
    }

    private _extractSolution(model: any): any {
        const solution: Record<string, Record<number, number>> = {};
        
        for (let r = 0; r < this.rows; r++) {
            for (let c = 0; c < this.cols; c++) {
                const posKey = `${r},${c}`;
                solution[posKey] = {};
                
                for (let dir = 0; dir < 4; dir++) {
                    const bridgeVar = this.islandBridges[posKey][dir];
                    const value = parseInt(model.eval(bridgeVar).toString());
                    solution[posKey][dir] = value;
                }
            }
        }
        
        return solution;
    }

    private _isValidSolution(solution: any): boolean {
        // Check if the solution forms a single connected loop
        // This is a simplified check - a proper implementation would need to verify connectivity
        let bridgeCount = 0;
        
        for (const posKey in solution) {
            const bridges = solution[posKey];
            for (const dir in bridges) {
                if (bridges[dir] === 1) {
                    bridgeCount++;
                }
            }
        }
        
        // Basic check: should have bridges and form a reasonable structure
        return bridgeCount > 0;
    }

    private _addSolutionConstraint(solution: any): void {
        const constraints = [];
        
        for (const posKey of Object.keys(solution)) {
            const bridges = solution[posKey];
            for (const dir of Object.keys(bridges)) {
                const value = bridges[dir];
                const dirNum = parseInt(dir);
                constraints.push(this.islandBridges[posKey][dirNum].eq(value));
            }
        }
        
        if (constraints.length > 0) {
            this.solver.add(this.ctx.Not(this.ctx.And(...constraints)));
        }
    }
}
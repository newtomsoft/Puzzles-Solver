import { Position } from '../../Domain/Base/position.js';

export class CanvasPlayer {
    static getCanvas(): HTMLCanvasElement | null {
        return document.querySelector('canvas');
    }

    private static getCellDimensions(canvas: HTMLCanvasElement, rows: number, cols: number) {
        const rect = canvas.getBoundingClientRect();
        return {
            rect,
            cellW: rect.width / cols,
            cellH: rect.height / rows
        };
    }

    private static getX(rect: DOMRect, cellW: number, position: Position) {
        return rect.left + cellW / 2 + position.c * cellW;
    }

    private static getY(rect: DOMRect, cellH: number, position: Position) {
        return rect.top + cellH / 2 + position.r * cellH;
    }

    private static simulateEvent(canvas: HTMLCanvasElement, x: number, y: number, type: string, buttons: number = 0) {
        const common = {
            bubbles: true,
            cancelable: true,
            clientX: x,
            clientY: y,
            screenX: x,
            screenY: y,
            button: 0,
            buttons: buttons,
            view: window
        };

        canvas.dispatchEvent(new PointerEvent(type.replace('mouse', 'pointer'), {
            ...common,
            pointerId: 1,
            isPrimary: true,
            pressure: buttons ? 0.5 : 0,
            width: 1,
            height: 1
        }));

        canvas.dispatchEvent(new MouseEvent(type, common));
    }

    static async drawPath(path: Position[], rows: number, cols: number = rows): Promise<void> {
        if (path.length === 0) return;

        const canvas = this.getCanvas();
        if (!canvas) {
            console.error("CanvasPlayer: Canvas NOT FOUND");
            return;
        }

        const { rect, cellW, cellH } = this.getCellDimensions(canvas, rows, cols);

        const startPosition = path[0];
        const startX = this.getX(rect, cellW, startPosition);
        const startY = this.getY(rect, cellH, startPosition);

        this.simulateEvent(canvas, startX, startY, 'mousedown', 1);

        for (let i = 0; i < path.length - 1; i++) {
            const currentPoint = path[i + 1];
            const x = this.getX(rect, cellW, currentPoint);
            const y = this.getY(rect, cellH, currentPoint);
            this.simulateEvent(canvas, x, y, 'mousemove', 1);
            await new Promise(r => setTimeout(r, 60));
        }

        const endPosition = path[path.length - 1];
        const endX = this.getX(rect, cellW, endPosition);
        const endY = this.getY(rect, cellH, endPosition);
        this.simulateEvent(canvas, endX, endY, 'mouseup', 0);
    }

    static async clickCells(cells: Position[], rows: number, cols: number = rows): Promise<void> {
        if (cells.length === 0) return;

        const canvas = this.getCanvas();
        if (!canvas) {
            console.error("CanvasPlayer: Canvas NOT FOUND");
            return;
        }

        const { rect, cellW, cellH } = this.getCellDimensions(canvas, rows, cols);

        for (const pos of cells) {
            const x = this.getX(rect, cellW, pos);
            const y = this.getY(rect, cellH, pos);

            this.simulateEvent(canvas, x, y, 'mousedown', 1);
            this.simulateEvent(canvas, x, y, 'mouseup', 0);
            await new Promise(r => setTimeout(r, 100));
        }
    }

    static edgesToPath(h: (boolean|number)[][], v: (boolean|number)[][], rows: number, cols: number): Position[] {
        // Normalizing input to number (0 or 1)
        const getH = (r: number, c: number) => {
            const val = h[r][c];
            return (typeof val === 'boolean' ? (val ? 1 : 0) : val);
        };
        const getV = (r: number, c: number) => {
            const val = v[r][c];
            return (typeof val === 'boolean' ? (val ? 1 : 0) : val);
        };

        let startR = -1, startC = -1;
        outer: for (let r = 0; r < rows; r++) {
            for (let c = 0; c < cols; c++) {
                if ((c < cols - 1 && getH(r, c) === 1) || (r < rows - 1 && getV(r, c) === 1)) {
                    startR = r;
                    startC = c;
                    break outer;
                }
            }
        }
        if (startR === -1) return [];

        const path: Position[] = [];
        let currR = startR;
        let currC = startC;
        const visitedEdges = new Set<string>();

        // Limit loop to prevent infinite loops in case of malformed graph
        const maxSteps = rows * cols * 4;
        let steps = 0;

        while (steps < maxSteps) {
            path.push(new Position(currR, currC));

            let nextR = -1, nextC = -1;
            let edgeKey = "";

            // Check Right
            if (currC < cols - 1 && getH(currR, currC) === 1 && !visitedEdges.has(`h_${currR}_${currC}`)) {
                nextR = currR; nextC = currC + 1; edgeKey = `h_${currR}_${currC}`;
            }
            // Check Left
            else if (currC > 0 && getH(currR, currC - 1) === 1 && !visitedEdges.has(`h_${currR}_${currC - 1}`)) {
                nextR = currR; nextC = currC - 1; edgeKey = `h_${currR}_${currC - 1}`;
            }
            // Check Down
            else if (currR < rows - 1 && getV(currR, currC) === 1 && !visitedEdges.has(`v_${currR}_${currC}`)) {
                nextR = currR + 1; nextC = currC; edgeKey = `v_${currR}_${currC}`;
            }
            // Check Up
            else if (currR > 0 && getV(currR - 1, currC) === 1 && !visitedEdges.has(`v_${currR - 1}_${currC}`)) {
                nextR = currR - 1; nextC = currC; edgeKey = `v_${currR - 1}_${currC}`;
            }

            if (nextR === -1) break;

            visitedEdges.add(edgeKey);
            currR = nextR;
            currC = nextC;
            steps++;

            if (currR === startR && currC === startC) {
                path.push(new Position(currR, currC));
                break;
            }
        }
        return path;
    }
}

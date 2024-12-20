// noinspection DuplicatedCode

export function ApplicationPuzzleBinairoPlus(): void {
    const cellDivs = document.querySelectorAll('div.cell, div.cell-0, div.cell-1');
    const cellsCount = cellDivs.length;
    const columnCount = Math.sqrt(cellsCount);

    const apiEndpoint = 'http://127.0.0.1:5001/binairo-plus/solution';
    const matrix = scrapGrid();
    const comparisonOperators = scrapComparisonOperators();


    function scrapComparisonOperators() {
        const cellSize = 35;
        const extractIndexes = (divs: NodeListOf<Element>, isRow: boolean): [number, number][] => {
            return Array.from(divs).map((div) => {
                const style = div.getAttribute('style') || '';
                const top = parseInt(style.match(/top: (\d+)px/)?.[1] || '0', 10);
                const left = parseInt(style.match(/left: (\d+)px/)?.[1] || '0', 10);
                if (isRow) {
                    return [Math.floor(top / cellSize) - 1, Math.floor(left / cellSize)];
                } else {
                    return [Math.floor(top / cellSize), Math.floor(left / cellSize) - 1];
                }
            });
        };

        const equal_on_columns = extractIndexes(document.querySelectorAll('div.eqh'), true);
        const non_equal_on_columns = extractIndexes(document.querySelectorAll('div.neh'), true);
        const equal_on_rows = extractIndexes(document.querySelectorAll('div.eqv'), false);
        const non_equal_on_rows = extractIndexes(document.querySelectorAll('div.nev'), false);

        return {
            equal_on_columns,
            non_equal_on_columns,
            equal_on_rows,
            non_equal_on_rows,
        };
    }

    function scrapGrid(): number[][] {
        const cells = Array.from(cellDivs);
        const values = cells.map((cell) => {
            const classList = cell.className;
            if (classList.includes('cell-0')) {
                return 1;
            } else if (classList.includes('cell-1')) {
                return 0;
            } else {
                return -1;
            }
        });

        const columnsNumber = cells.filter(cell =>
            cell.getAttribute('style')?.includes('top: 1px')
        ).length;

        const rowsNumber = cells.filter(cell =>
            cell.getAttribute('style')?.includes('left: 1px')
        ).length;

        if (columnsNumber * rowsNumber !== cellsCount) {
            throw new Error('Binairo Plus grid parsing error');
        }

        let matrix: number[][] = [];
        for (let r = 0; r < rowsNumber; r++) {
            const row: number[] = [];
            for (let c = 0; c < columnsNumber; c++) {
                row.push(values[r * columnsNumber + c]);
            }
            matrix.push(row);
        }

        return matrix;
    }

    post(matrix, comparisonOperators, apiEndpoint).then((solution: [[]]) => {
        playSolution(solution);
    });

    async function post(matrix: number[][], comparisonOperators: any, apiEndpoint: string): Promise<[[]]> {
        const body = JSON.stringify({matrix, comparison_operators: comparisonOperators});
        console.debug('body:', body);
        try {
            const response = await fetch(apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: body
            });
            return await response.json();
        } catch (error) {
            console.error('error:', error);
            return [[]];
        }
    }

    function playSolution(solution: [[]]): void {
        solution.forEach((row, i) => {
            row.forEach((cell, j) => {
                if (cell) {
                    const cellDiv = cellDivs[i * columnCount + j];
                    const coordinates = getCoordinates(cellDiv as HTMLElement);
                    const middleX = coordinates.left + coordinates.width / 2.0;
                    const middleY = coordinates.top + coordinates.height / 2.0;
                    createSquare(middleX, middleY);
                }
            });
        });
    }

    function getCoordinates(element: HTMLElement): { top: number, left: number, width: number, height: number } {
        const style = window.getComputedStyle(element);
        return {
            top: parseFloat(style.top),
            left: parseFloat(style.left),
            width: parseFloat(style.width),
            height: parseFloat(style.height)
        };
    }

    function createSquare(middleX: number, middleY: number) {
        createSegment(`23px`, '1px', `${middleX - 11}px`, `${middleY - 11}px`);
        createSegment('23px', '1px', `${middleX - 11}px`, `${middleY + 11}px`);
        createSegment('1px', '23px', `${middleX - 11}px`, `${middleY - 11}px`);
        createSegment('1px', '23px', `${middleX + 11}px`, `${middleY - 11}px`);
    }

    function createSegment(width: string, height: string, left: string, top: string) {
        const segment = document.createElement('div');
        segment.style.position = 'absolute';
        segment.style.width = width;
        segment.style.height = height;
        segment.style.backgroundColor = 'green';
        segment.style.left = left;
        segment.style.top = top;
        const boardBack = document.querySelector('.board-back');
        if (boardBack) {
            boardBack.appendChild(segment);
        } else {
            console.error('Element with class "board-back" not found.');
        }
        return segment;
    }

}
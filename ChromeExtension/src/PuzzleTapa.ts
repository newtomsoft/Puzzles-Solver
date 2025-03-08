export function ApplicationPuzzleTapa(): void {
    const cellDivs = document.querySelectorAll('div.cell, div.tapa-task-cell');
    const cellsCount = cellDivs.length;
    const rowCount = Math.sqrt(cellsCount);
    const columnCount = rowCount;

    const matrix = scrapGrid();
    const apiEndpoint = 'http://127.0.0.1:5000/solution';
    post(matrix, apiEndpoint).then((solution: [[]]) => {
        console.log('solution:', solution);
        playSolution(solution);
    });


    function scrapGrid(): (boolean | number[])[][] {
        const matrix: (boolean | number[])[][] = Array.from({length: rowCount}, () => Array(columnCount).fill(false));
        cellDivs.forEach((cellDiv, i) => {
            const classes = (cellDiv as HTMLElement).className.split(' ');
            if (!classes.includes('tapa-task-cell')) {
                return;
            }
            const spans = cellDiv.querySelectorAll('span');
            const values: number[] = [];
            spans.forEach(span => {
                values.push(parseInt((span as HTMLElement).innerText, 10));
            });
            matrix[Math.floor(i / columnCount)][i % columnCount] = values;
        });
        return matrix;
    }

    async function post(matrix: (boolean | number[])[][], apiEndpoint: string): Promise<[[]]> {
        const body = JSON.stringify({matrix});
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
    }

}
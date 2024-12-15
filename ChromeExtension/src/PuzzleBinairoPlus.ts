export function ApplicationPuzzleBinairoPlus(): void {
    const cellDivs = document.querySelectorAll('div.cell, div.cell-0, div.cell-1');
    const cellsCount = cellDivs.length;
    const rowCount = Math.sqrt(cellsCount);
    const columnCount = rowCount;

    const matrix = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, 1, 0, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [1, -1, -1, -1, -1, 0],
        [1, -1, 1, 0, -1, 1]
    ]
    const apiEndpoint = 'http://127.0.0.1:5001/binairo-plus/solution';
    const comparisonOperators = {
        'equal_on_columns': [[2, 0], [3, 4]],
        'equal_on_rows': [[1, 1], [1, 3]],
        'non_equal_on_columns': [[0, 2], [0, 3], [2, 5], [3, 1]],
        'non_equal_on_rows': []
    };
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
        console.log('playSolution:', solution);
        solution.forEach((row, i) => {
            row.forEach((cell, j) => {
                if (cell) {
                    const cellDiv = cellDivs[i * columnCount + j];
                    const coordinates = getCoordinates(cellDiv as HTMLElement);
                    const middleX = coordinates.left + coordinates.width / 2.0;
                    const middleY = coordinates.top + coordinates.height / 2.0;
                    createSquare(createSegment, middleX, middleY);
                    // if (cellDiv.classList.contains('cell-off')) {
                    //     cellDiv.classList.remove('cell-off');
                    //     cellDiv.classList.add('cell-on');
                    // }
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

    function createSquare(createSegment: (width: string, height: string, left: string, top: string) => void, middleX: number, middleY: number) {
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
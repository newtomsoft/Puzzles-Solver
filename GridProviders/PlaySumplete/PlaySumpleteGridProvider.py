import requests
from bs4 import BeautifulSoup

from GridProviders.GridProvider import GridProvider
from Domain.Board.Grid import Grid


class PlaySumpleteGridProvider(GridProvider):
    @staticmethod
    def get_grid(source: str):
        response = requests.get(source)
        soup = BeautifulSoup(response.text, 'html.parser')
        grid = soup.find('div', {'class': 'grid'})
        numbers = [int(button.find('div').text) for button in grid.find_all('button')]
        size = len(numbers) ** 0.5
        if size != int(size):
            raise ValueError("Board is not square")
        matrix = [numbers[i:i + int(size)] for i in range(0, len(numbers), int(size))]

        sums_divs = PlaySumpleteGridProvider.get_sums(grid)
        sums = [int(div.find('div').text) for div in sums_divs]
        horizontal_sums = sums[:int(len(sums) / 2)]
        vertical_sums = sums[int(len(sums) / 2):]

        for i in range(len(matrix)):
            matrix[i].append(horizontal_sums[i])
        matrix.append(vertical_sums)

        matrix[-1].append(0)

        return Grid(matrix)

    @staticmethod
    def get_sums(grid):
        sums_divs = grid.find_all('div', {'class': 'svelte-3zstav'})
        sums_divs.pop()
        return sums_divs

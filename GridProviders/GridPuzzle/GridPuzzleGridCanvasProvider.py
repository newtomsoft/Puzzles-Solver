import base64
import re

from bs4 import BeautifulSoup

from GridProviders.GridPuzzle.GridPuzzleGridProvider import GridPuzzleGridProvider


class GridPuzzleGridCanvasProvider(GridPuzzleGridProvider):
    @staticmethod
    def _get_canvas_data(html_page: str) -> tuple[list[str], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.Size = (\d+);', html_string).group(1))
        pqq_base64 = re.search(r'gpl\.pqq = "(.*?)";', html_string).group(1)
        pqq_raw = base64.b64decode(pqq_base64[3:])
        pqq_string = pqq_raw.decode('utf-8', errors='ignore')
        pqq_string_list = pqq_string.split('|')
        return pqq_string_list, size

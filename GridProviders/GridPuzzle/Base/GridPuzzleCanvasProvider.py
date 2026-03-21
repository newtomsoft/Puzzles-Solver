import base64
import re

from bs4 import BeautifulSoup

from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider


class GridPuzzleGridCanvasProvider(GridPuzzleProvider):
    @staticmethod
    def _extract_gpl_data(html_page: str, var_name: str = 'pq{1,2}') -> tuple[int, str, str]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size_match = re.search(r'gpl\.([Ss]ize)\s*=\s*(\d+);', html_string)
        if not size_match:
            size_match = re.search(r'size\s*:\s*(\d+)', html_string)
        size = int(size_match.group(2 if size_match.group(0).startswith('gpl') else 1))

        pqq_match = re.search(fr'gpl\.{var_name}\s*=\s*"(.*?)";', html_string)
        pqq = pqq_match.group(1)
        pqq_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(pqq)
        return size, pqq, pqq_string

    @staticmethod
    def _get_canvas_data(html_page: str) -> tuple[list[str], int]:
        size, pqq, pqq_string = GridPuzzleGridCanvasProvider._extract_gpl_data(html_page)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)
        return pqq_string_list, size

    @staticmethod
    def _get_canvas_data_extended(html_page: str) -> tuple[list[str], list[str], list[str], int]:
        size, pqq, pqq_string = GridPuzzleGridCanvasProvider._extract_gpl_data(html_page)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)

        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        ar_match = re.search(r'(gpl\.)?a?r_data\s*=\s*("(.*?)"|gpl\.str2obj\("(.*?)"\));', html_string)
        if not ar_match:
            ar_match = re.search(r'gpl\.a?r_data\s*=\s*"(.*?)";', html_string)
            ar = ar_match.group(1) if ar_match else ""
        else:
            ar = ar_match.group(3) if ar_match.group(3) is not None else ar_match.group(4)
        ar_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(ar)
        ar_string_list = GridPuzzleGridCanvasProvider._split_to_list(ar_string, size)

        ab_match = re.search(r'(gpl\.)?a?b_data\s*=\s*("(.*?)"|gpl\.str2obj\("(.*?)"\));', html_string)
        if not ab_match:
            ab_match = re.search(r'gpl\.a?b_data\s*=\s*"(.*?)";', html_string)
            ab = ab_match.group(1) if ab_match else ""
        else:
            ab = ab_match.group(3) if ab_match.group(3) is not None else ab_match.group(4)
        ab_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(ab)
        ab_string_list = GridPuzzleGridCanvasProvider._split_to_list(ab_string, size)
        
        return pqq_string_list, ar_string_list, ab_string_list, size

    @staticmethod
    def _get_canvas_data_extended2(html_page: str) -> tuple[list[str], list[list[int]], int]:
        size, pqq, pqq_string = GridPuzzleGridCanvasProvider._extract_gpl_data(html_page)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        gpl_numbers = re.search(r'gpl\.numbers\s*=\s*"(.*?)";', html_string).group(1)
        numbers_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(gpl_numbers)
        up_down_left_right = GridPuzzleGridCanvasProvider.convert_pattern(numbers_string)

        return pqq_string_list, up_down_left_right, size

    @staticmethod
    def _get_canvas_data_with_pipe(html_page: str) -> tuple[list[str], int]:
        size, pqq, pqq_string = GridPuzzleGridCanvasProvider._extract_gpl_data(html_page)
        pqq_string_list = [pqq_string[i:i + 1] for i in range(len(pqq_string))]
        return pqq_string_list, size

    @staticmethod
    def _decode_if_custom_base64(string: str) -> str:
        if len(string) < 4 or not GridPuzzleGridCanvasProvider._is_valid_base64(string[3:]):
            return string

        decoded = base64.b64decode(string[3:])
        return decoded.decode('utf-8', errors='ignore')

    @staticmethod
    def _is_valid_base64(string: str) -> bool:
        return len(string) % 4 == 0 and bool(re.match('^[A-Za-z0-9+/]*={0,2}$', string))

    @staticmethod
    def _split_to_list(string: str, size: int) -> list[str]:
        split_pipe = string.split('|')
        if len(split_pipe) == size or len(split_pipe) == size * size:
            return split_pipe
        return [string[i:i + 1] for i in range(len(string))]

    @staticmethod
    def convert_pattern(pattern):
        lignes = pattern.split('$')

        grid = []
        for ligne in lignes:
            cellules_brutes = ligne.split('|')[:-1]

            ligne_convertie = []
            for cell in cellules_brutes:
                if cell == '':
                    ligne_convertie.append(None)
                else:
                    ligne_convertie.append(int(cell))

            grid.append(ligne_convertie)

        return grid


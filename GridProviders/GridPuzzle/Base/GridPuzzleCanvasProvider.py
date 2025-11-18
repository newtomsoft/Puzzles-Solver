import base64
import re

from bs4 import BeautifulSoup

from GridProviders.GridPuzzle.Base.GridPuzzleProvider import GridPuzzleProvider


class GridPuzzleGridCanvasProvider(GridPuzzleProvider):
    @staticmethod
    def _get_canvas_data(html_page: str) -> tuple[list[str], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.([Ss]ize) = (\d+);', html_string).group(2))
        pqq = re.search(r'gpl\.pq{1,2} = "(.*?)";', html_string).group(1)
        pqq_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(pqq)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)
        return pqq_string_list, size

    @staticmethod
    def _get_canvas_data_extended(html_page: str) -> tuple[list[str], list[str], list[str], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.([Ss]ize) = (\d+);', html_string).group(2))
        pqq = re.search(r'gpl\.pq{1,2} = "(.*?)";', html_string).group(1)
        pqq_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(pqq)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)
        ar = re.search(r'ar_data = "(.*?)";', html_string).group(1)
        ar_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(ar)
        ar_string_list = GridPuzzleGridCanvasProvider._split_to_list(ar_string, size)
        ab = re.search(r'ab_data = "(.*?)";', html_string).group(1)
        ab_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(ab)
        ab_string_list = GridPuzzleGridCanvasProvider._split_to_list(ab_string, size)
        return pqq_string_list, ar_string_list, ab_string_list, size

    @staticmethod
    def _get_canvas_data_extended2(html_page: str) -> tuple[list[str], list[list[int]], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.([Ss]ize) = (\d+);', html_string).group(2))
        pqq = re.search(r'gpl\.pq{1,2} = "(.*?)";', html_string).group(1)
        pqq_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(pqq)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list(pqq_string, size)
        gpl_numbers = re.search(r'gpl\.numbers = "(.*?)";', html_string).group(1)
        numbers_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(gpl_numbers)
        numbers_string_list = GridPuzzleGridCanvasProvider._split_to_list(numbers_string, size)
        up_down_left_right = GridPuzzleGridCanvasProvider._split_to_list2(numbers_string_list)

        return pqq_string_list, up_down_left_right, size

    @staticmethod
    def _get_canvas_data_with_pipe(html_page: str) -> tuple[list[str], int]:
        html_string = BeautifulSoup(html_page, 'html.parser').prettify()
        size = int(re.search(r'gpl\.([Ss]ize) = (\d+);', html_string).group(2))
        pqq = re.search(r'gpl\.pq{1,2} = "(.*?)";', html_string).group(1)
        pqq_string = GridPuzzleGridCanvasProvider._decode_if_custom_base64(pqq)
        pqq_string_list = GridPuzzleGridCanvasProvider._split_to_list_with_pipe(pqq_string)
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
    def _split_to_list2(input_list: list[str]) -> list[int]:
        result = []
        current_sublist = []

        for item in input_list:
            if item == '$':
                if current_sublist:
                    result.append(current_sublist)
                    current_sublist = []
            elif item != '|':
                current_sublist.append(int(item))

        if current_sublist:
            result.append(current_sublist)

        return result

    @staticmethod
    def _split_to_list_with_pipe(string: str) -> list[str]:
        return [string[i:i + 1] for i in range(len(string))]

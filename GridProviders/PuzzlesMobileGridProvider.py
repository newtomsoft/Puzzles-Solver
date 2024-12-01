class PuzzlesMobileGridProvider:
    @staticmethod
    def get_puzzle_info_text(soup):
        puzzle_info = soup.find('div', class_='puzzleInfo')
        puzzle_info_text = puzzle_info.text
        return puzzle_info_text

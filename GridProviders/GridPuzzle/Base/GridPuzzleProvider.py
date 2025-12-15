from bs4.element import AttributeValueList

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class GridPuzzleProvider:
    @staticmethod
    def get_html(browser, url, board_selector: str | None = None):
        page = browser.pages[0]
        page.set_viewport_size({"width": 685, "height": 900})
        page.goto(url)
        html_page = page.content()
        if not board_selector:
            return html_page
        div_to_view = page.query_selector(board_selector)
        div_to_view.scroll_into_view_if_needed()
        return html_page

    @staticmethod
    def make_opened_grid(row_count, column_count, matrix_cells) -> Grid:
        borders_dict = {'br': Direction.right(), 'bl': Direction.left(), 'bt': Direction.up(), 'bb': Direction.down()}
        all_borders = set(Direction.orthogonal_directions())
        opened_grid = Grid([[set() for _ in range(column_count)] for _ in range(row_count)])
        for i, cell in enumerate(matrix_cells):
            position = Position(*divmod(i, column_count))
            classes = cell.get('class', AttributeValueList([]))
            closed_borders = (
                    {borders_dict[cls] for cls in classes if cls in borders_dict}
                    | ({Direction.up()} if position in opened_grid.edge_up_positions() else set())
                    | ({Direction.down()} if position in opened_grid.edge_down_positions() else set())
                    | ({Direction.left()} if position in opened_grid.edge_left_positions() else set())
                    | ({Direction.right()} if position in opened_grid.edge_right_positions() else set())
            )
            opened_grid[position] = all_borders - closed_borders

        return opened_grid

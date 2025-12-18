from bs4.element import AttributeValueList
from playwright.async_api import Page

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class GridPuzzleProvider:
    @staticmethod
    async def get_html(browser, url, board_selector: str | None = None):
        page = browser.pages[0]
        await page.set_viewport_size({"width": 685, "height": 900})
        await page.goto(url)

        if "Just a moment..." in await page.title():
            await GridPuzzleProvider._handle_cloudflare_challenge(page)

        html_page = await page.content()
        if not board_selector:
            return html_page
        div_to_view = await page.query_selector(board_selector)
        await div_to_view.scroll_into_view_if_needed()
        return html_page

    @staticmethod
    async def _handle_cloudflare_challenge(page: Page):
        try:
            iframe = await page.wait_for_selector("iframe[src*='challenges.cloudflare.com']", timeout=10000)
            if iframe:
                frame = await iframe.content_frame()
                checkbox = await frame.wait_for_selector("input[type='checkbox']", timeout=10000)
                if checkbox:
                    await checkbox.click()
                    await page.wait_for_load_state("networkidle")
        except Exception:
            pass

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

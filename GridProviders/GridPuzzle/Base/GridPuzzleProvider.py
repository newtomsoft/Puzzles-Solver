import asyncio

from bs4.element import AttributeValueList

from Domain.Board.Direction import Direction
from Domain.Board.Grid import Grid
from Domain.Board.Position import Position


class GridPuzzleProvider:
    @staticmethod
    async def get_html(browser, url, board_selector: str | None = None):
        if len(browser.pages) == 0:
            page = await browser.new_page()
        else:
            page = browser.pages[0]
        try:
            await page.set_viewport_size({"width": 685, "height": 900})
        except Exception:
            pass
        await page.goto(url, wait_until="domcontentloaded", timeout=15000)
        for attempt in range(5):
            try:
                page_title = await page.title()
                break
            except Exception:
                if attempt == 4:
                    raise
                await asyncio.sleep(0.5)
        if "just a moment" in page_title.lower() or "un instant" in page_title.lower():
            print("\n" + "=" * 60, flush=True)
            print("CLOUDFLARE CHALLENGE DETECTED!", flush=True)
            print("Please solve the challenge in the browser window.", flush=True)
            print("Waiting for page to load automatically...", flush=True)
            print("=" * 60 + "\n", flush=True)
            for attempt in range(60):
                await asyncio.sleep(2)
                for attempt in range(5):
                    try:
                        page_title = await page.title()
                        break
                    except Exception:
                        if attempt == 4:
                            raise
                        await asyncio.sleep(0.5)
                if "just a moment" not in page_title.lower() and "un instant" not in page_title.lower():
                    print("Challenge solved! Continuing...", flush=True)
                    break
            else:
                raise TimeoutError("Cloudflare challenge was not solved within 120 seconds")

        try:
            await page.wait_for_selector(".page-body", timeout=5000)
        except Exception:
            pass

        for attempt in range(5):
            try:
                html_page = await asyncio.wait_for(page.content(), timeout=10)
                break
            except Exception:
                if attempt == 4:
                    raise
                await asyncio.sleep(0.5)
        if not board_selector:
            return html_page
        div_to_view = await page.query_selector(board_selector)
        if div_to_view:
            await div_to_view.scroll_into_view_if_needed()
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

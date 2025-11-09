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


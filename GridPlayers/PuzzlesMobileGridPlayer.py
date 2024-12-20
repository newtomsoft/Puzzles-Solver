from playwright.sync_api import Page


class PuzzlesMobileGridPlayer:
    @classmethod
    def submit_score(cls, page: Page):
        page.wait_for_selector('.succ')
        score_submit_button = page.locator("#btnHallSubmit")
        if score_submit_button.count() > 0:
            score_submit_button.first.click()

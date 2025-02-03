from abc import ABC


class PlaywrightGridPlayer(ABC):
    def __init__(self, playwright):
        self.playwright = playwright

    def play(self, grid):
        self.playwright.play(grid)

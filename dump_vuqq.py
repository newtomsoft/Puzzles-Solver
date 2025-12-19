from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://vuqq.com/fr/hitori/?size=5")
        page.wait_for_load_state('domcontentloaded')
        # Wait a bit for JS to render the grid
        page.wait_for_timeout(2000)

        print("Title:", page.title())

        # Dump the grid container
        # Looking for something that looks like a grid
        # Vuqq usually has a game-board or similar
        content = page.content()
        print(content)

        browser.close()

if __name__ == "__main__":
    run()

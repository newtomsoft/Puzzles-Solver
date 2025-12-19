from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://vuqq.com/fr/hitori/?size=5")
        page.wait_for_load_state('domcontentloaded')
        page.wait_for_timeout(2000)

        # Get the first cell
        cell = page.locator(".grid__cell").first

        print("--- Sequence 2: Right Click from Empty ---")
        # Ensure empty
        # Right click
        cell.click(button="right")
        page.wait_for_timeout(500)
        print(f"Right click from Empty: {cell.get_attribute('class')}")

        # Right click again
        cell.click(button="right")
        page.wait_for_timeout(500)
        print(f"Right click again: {cell.get_attribute('class')}")

        print("--- Sequence 3: Cycle Check ---")
        # Reset to empty if needed (assuming right click resets or toggles)
        # Let's just reload to be sure
        page.reload()
        page.wait_for_timeout(2000)
        cell = page.locator(".grid__cell").first

        print("Click 1 (Left):")
        cell.click()
        page.wait_for_timeout(200)
        print(f"State: {cell.get_attribute('class')}")

        print("Click 2 (Left):")
        cell.click()
        page.wait_for_timeout(200)
        print(f"State: {cell.get_attribute('class')}")

        print("Click 3 (Left):")
        cell.click()
        page.wait_for_timeout(200)
        print(f"State: {cell.get_attribute('class')}")

        browser.close()

if __name__ == "__main__":
    run()

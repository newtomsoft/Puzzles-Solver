import asyncio
from GridProviders.GridPuzzle.GridPuzzleAkariGridProvider import GridPuzzleAkariGridProvider


async def main():
    provider = GridPuzzleAkariGridProvider()
    url = "https://gridpuzzle.com/lightup/1nnnnd"
    print(f"Testing GridPuzzleAkariGridProvider with URL: {url}")
    print(f"Headless mode: {provider.headless}")
    try:
        grid_data, browser_context, playwright = await provider.get_grid(url)
        print("Success! Grid data:")
        print(grid_data)
        await browser_context.close()
        await playwright.stop()
    except Exception as e:
        print(f"Error: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())

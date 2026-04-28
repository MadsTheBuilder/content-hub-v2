import asyncio
from playwright.async_api import async_playwright


async def debug():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=500)
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})
        await page.set_content(
            "<h1 style='color:gold;background:#0F172A;padding:40px'>Playwright working</h1>"
        )
        print("Browser open — check your taskbar")
        await asyncio.sleep(10)
        await browser.close()
        print("Done")


asyncio.run(debug())

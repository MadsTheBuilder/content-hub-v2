---
status: Active
date_exported: "2026-04-09 12:24"
original_path: "backend/content/renderer_slides.py"
category: "Content Hub Source Code"
---

# renderer_slides.py

**Description:** Core content generation pipeline logic, routing, and script orchestration.

---

```py
from playwright.async_api import async_playwright
from backend.storage.client import upload_file

SLIDE_HTML_TEMPLATE = """
<!DOCTYPE html>
<html><head><style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&family=Inter:wght@400;500&display=swap');
    
    body {{
        margin: 0;
        width: 1080px;
        height: 1080px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        background: {bg_gradient};
        font-family: 'Inter', sans-serif;
        color: {text_color};
        padding: 100px;
        box-sizing: border-box;
        overflow: hidden;
        position: relative;
    }}

    .background-accent {{
        position: absolute;
        width: 600px;
        height: 600px;
        background: {accent_color};
        filter: blur(150px);
        opacity: 0.15;
        border-radius: 50%;
        top: -100px;
        right: -100px;
        z-index: 0;
    }}

    .content {{
        position: relative;
        z-index: 10;
        width: 100%;
        text-align: left;
    }}

    h1 {{
        font-family: 'Outfit', sans-serif;
        font-size: 84px;
        font-weight: 800;
        margin-bottom: 40px;
        line-height: 1.1;
        letter-spacing: -0.02em;
        color: #FFFFFF;
    }}

    .accent-bar {{
        width: 80px;
        height: 8px;
        background: {accent_color};
        margin-bottom: 40px;
        border-radius: 4px;
    }}

    p {{
        font-size: 44px;
        line-height: 1.4;
        font-weight: 400;
        color: #E2E8F0;
        max-width: 880px;
    }}

    .footer {{
        position: absolute;
        bottom: 80px;
        left: 100px;
        right: 100px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 10;
    }}

    .watermark {{
        font-family: 'Outfit', sans-serif;
        font-size: 24px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: {accent_color};
        opacity: 0.8;
    }}

    .slide-number {{
        font-family: 'Outfit', sans-serif;
        font-size: 28px;
        font-weight: 600;
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 24px;
        border-radius: 100px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        color: #FFFFFF;
    }}
</style></head>
<body>
    <div class="background-accent"></div>
    <div class="content">
        <div class="accent-bar"></div>
        <h1>{headline}</h1>
        <p>{body}</p>
    </div>
    <div class="footer">
        <div class="watermark">{watermark}</div>
        <div class="slide-number">{slide_number} / {total_slides}</div>
    </div>
</body></html>
"""


async def render_slides(storyboard: dict, user_id: str, workflow_id: str, watermark: str = "") -> list[str]:
    frames = storyboard.get("frames", [])
    total = len(frames)
    urls = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1080, "height": 1080})

        for frame in frames:
            bg_gradient = frame.get("bg_gradient", "linear-gradient(135deg, #0F172A 0%, #1E293B 100%)")
            accent_color = frame.get("accent_color", "#C9A96E")
            
            html = SLIDE_HTML_TEMPLATE.format(
                bg_gradient=bg_gradient,
                accent_color=accent_color,
                text_color="#FFFFFF",
                headline=frame.get("headline", ""),
                body=frame.get("body", ""),
                slide_number=frame.get("slide_number", 1),
                total_slides=total,
                watermark=watermark or "CONTENT HUB",
            )
            await page.set_content(html)
            screenshot = await page.screenshot(type="png")
            url = await upload_file(user_id, workflow_id, screenshot, f"slide_{frame.get('slide_number', 1)}.png")
            urls.append(url)

        await browser.close()
    return urls

```

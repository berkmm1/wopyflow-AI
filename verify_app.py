import asyncio
from playwright.async_api import async_playwright
import os
import subprocess
import time

async def run_verification():
    # Start server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"])
    time.sleep(2) # Give server time to start

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            # 1. Check Branding & Tagline
            await page.goto("http://localhost:8000")
            print("Page title:", await page.title())

            hero_text = await page.inner_text("h2")
            print("Hero title:", hero_text)

            tagline = await page.inner_text("section p")
            print("Tagline:", tagline)

            # 2. Verify Analyzer UI
            url_input = await page.query_selector("#lpUrl")
            analyze_btn = await page.query_selector("button:has-text('Analyze Now')")
            print(f"Analyzer UI: Input found? {url_input is not None}, Button found? {analyze_btn is not None}")

            # 3. Simulate Analysis (mocking results)
            # Since we can't easily mock the fetch in this simple setup without more complex playwright usage,
            # we'll just check if the loading animation is triggered
            await page.fill("#lpUrl", "example.com")
            await page.click("button:has-text('Analyze Now')")

            loading = await page.is_visible("#analyzerLoading")
            print(f"Analyzer loading visible? {loading}")

            # 4. Verify PDF Generator UI
            pdf_input_container = await page.query_selector("div[onclick*='pdfInput']")
            print(f"PDF upload container found? {pdf_input_container is not None}")

            # 5. Check Footer
            footer_text = await page.inner_text("footer")
            print(f"Footer has copyright? {'2025' in footer_text}")

            await page.screenshot(path="verification_screenshot.png", full_page=True)
            print("Screenshot saved to verification_screenshot.png")

            await browser.close()
    finally:
        server_process.terminate()

if __name__ == "__main__":
    asyncio.run(run_verification())

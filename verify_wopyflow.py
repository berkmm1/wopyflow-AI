import asyncio
import os
from playwright.async_api import async_playwright
import subprocess
import time

async def verify_app():
    # Start the server
    server_process = subprocess.Popen(["python3", "-m", "http.server", "8000"])
    time.sleep(2)  # Wait for server to start

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto("http://localhost:8000")

            # Verify Title
            title = await page.title()
            print(f"Page Title: {title}")
            assert "Wopyflow AI" in title

            # Mock fetch for Tool 1 to avoid network issues
            await page.route("https://api.allorigins.win/get?*", lambda route: route.fulfill(
                status=200,
                body='{"contents": "<html><body><h1>Example Page</h1><p>Join us today! Buy now. Trust reviews.</p></body></html>"}'
            ))

            # Test Tool 1: Landing Page Analyzer
            print("Testing Landing Page Analyzer...")
            await page.fill("#lpUrl", "https://example.com")
            await page.click("button:has-text('Analyze Page')")

            # Wait for results
            await page.wait_for_selector("#analyzerResults", state="visible", timeout=15000)
            print("Analyzer results visible.")

            score_text = await page.inner_text("#scoreText")
            print(f"Conversion Score: {score_text}")
            assert int(score_text) > 0

            # Test Tool 2: PDF to Social Media Post Generator
            print("Testing PDF Generator...")
            pdf_path = os.path.abspath("test.pdf")
            await page.set_input_files("#pdfInput", pdf_path)

            # Wait for results
            await page.wait_for_selector("#pdfResults", state="visible", timeout=15000)
            print("PDF Generator results visible.")

            twitter_text = await page.inner_text("#twitterText")
            print(f"Twitter Thread Preview: {twitter_text[:50]}...")
            assert "1/5" in twitter_text
            assert "5/5" in twitter_text

            # Test Lead Gen
            print("Testing Lead Gen Form...")
            await page.fill("#leadGenForm input[type='email']", "test@example.com")
            await page.click("#leadGenForm button[type='submit']")
            await page.wait_for_selector("#leadGenSuccess", state="visible")
            print("Lead Gen success message visible.")

            # Take a screenshot
            await page.screenshot(path="verification_screenshot.png", full_page=True)
            print("Screenshot saved to verification_screenshot.png")

            await browser.close()
    finally:
        server_process.terminate()

if __name__ == "__main__":
    asyncio.run(verify_app())

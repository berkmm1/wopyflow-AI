import asyncio
from playwright.async_api import async_playwright
import http.server
import socketserver
import threading
import socket
import os

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def run_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

async def verify():
    port = get_free_port()
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(record_video_dir="verification/videos/")
        page = await context.new_page()

        # Mock allorigins.win
        await page.route("https://api.allorigins.win/get?url=*", lambda route: route.fulfill(
            status=200,
            body='{"contents": "<html><body><h1>Example Page</h1><p>This is a great landing page for developers. Pricing starts at $10. Buy now!</p></body></html>"}'
        ))

        await page.goto(f"http://localhost:{port}/index.html")
        await page.wait_for_selector("h1:has-text('Wopyflow AI')")
        await page.screenshot(path="verification/screenshots/hero_section.png")

        # 1. Test Analyzer
        await page.fill("#lpUrl", "https://example.com")
        await page.click("button:has-text('Analyze')")
        await page.wait_for_selector("#analyzerResults", state="visible", timeout=10000)
        await page.screenshot(path="verification/screenshots/analyzer_results_full.png", full_page=True)

        # Verify JSON toggle
        await page.click("button:has-text('View Technical JSON')")
        await page.wait_for_selector("#jsonBlock:not(.hidden)")
        await page.screenshot(path="verification/screenshots/analyzer_json_view.png")

        # 2. Test PDF Generator
        # Using the existing test.pdf
        await page.set_input_files("#pdfInput", "test.pdf")
        await page.wait_for_selector("#pdfResults", state="visible", timeout=15000)
        await page.screenshot(path="verification/screenshots/pdf_results_full.png", full_page=True)

        # Verify Twitter thread cards
        tweets = await page.query_selector_all("#twitterThreadContainer > div")
        print(f"Number of tweets generated: {len(tweets)}")

        # 3. Test Lead Gen
        await page.fill("#leadGenForm input[type='email']", "user@wopyflow.ai")
        await page.click("#leadGenForm button")
        await page.wait_for_selector("#leadGenSuccess", state="visible")
        await page.screenshot(path="verification/screenshots/lead_gen_success.png")

        await context.close()
        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())

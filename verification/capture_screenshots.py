import asyncio
from playwright.async_api import async_playwright
import os
import http.server
import socketserver
import threading

def run_server(port):
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        httpd.serve_forever()

async def capture():
    port = 8000
    server_thread = threading.Thread(target=run_server, args=(port,), daemon=True)
    server_thread.start()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"http://localhost:{port}/index.html")
        await page.set_viewport_size({"width": 1280, "height": 1600})
        await page.screenshot(path="verification/screenshots/initial_load.png", full_page=True)

        # Test Analyzer
        await page.fill("#lpUrl", "https://example.com")
        await page.click("button:has-text('Analyze')")
        await page.wait_for_selector("#analyzerResults", state="visible", timeout=10000)
        await page.screenshot(path="verification/screenshots/analyzer_results.png", full_page=True)

        # Test Lead Gen
        await page.fill("#leadGenForm input[type='email']", "test@example.com")
        await page.click("#leadGenForm button")
        await page.wait_for_selector("#leadGenSuccess", state="visible")
        await page.screenshot(path="verification/screenshots/lead_gen_success.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(capture())

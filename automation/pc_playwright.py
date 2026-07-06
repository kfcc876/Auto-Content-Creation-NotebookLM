import os
import sys
import json
import asyncio
from pathlib import Path
import argparse

# Selector-based Automation for Playwright (PC / Server Headless)
try:
    from playwright.async_api import async_playwright
except ImportError:
    print("❌ Playwright is not installed.")
    print("Please install it: pip install playwright && playwright install firefox")
    sys.exit(1)

def load_config():
    config_path = Path("config.json")
    if not config_path.exists():
        config_path = Path("config.json.example")
    with open(config_path, "r") as f:
        return json.load(f)

async def run_playwright(notebook_id, storage_state, headless=True):
    notebook_url = f"https://notebooklm.google.com/notebook/{notebook_id}"
    
    async with async_playwright() as p:
        print("🌐 Launching Browser (Firefox)...")
        browser = await p.firefox.launch(headless=headless)
        
        # Load storage state (which contains cookies)
        if os.path.exists(storage_state):
            print(f"🔑 Loading login state from: {storage_state}")
            context = await browser.new_context(storage_state=storage_state)
        else:
            print(f"⚠️ Storage state file not found: {storage_state}")
            print("Running in interactive mode. You will need to log in manually.")
            context = await browser.new_context()
            
        page = await context.new_page()
        
        # Navigate directly to the notebook
        print(f"🚀 Navigating to: {notebook_url}")
        await page.goto(notebook_url, wait_until="networkidle")
        await page.wait_for_timeout(5000)
        
        # Detect Login state
        if "signin" in page.url or "accounts.google.com" in page.url:
            print("🔐 Login Required! Google sign-in detected.")
            if headless:
                print("❌ Browser is running headlessly. Please log in on a non-headless browser first,")
                print("or run this script with --no-headless to perform VNC/GUI interactive login.")
                await browser.close()
                sys.exit(1)
            else:
                print("⏳ Interactive Login mode. Waiting for you to complete sign-in...")
                # Wait for navigation back to notebooklm
                while "notebooklm.google.com" not in page.url:
                    await page.wait_for_timeout(2000)
                print("🎉 Login completed successfully!")
                # Save storage state for next time
                os.makedirs(os.path.dirname(storage_state), exist_ok=True)
                await context.storage_state(path=storage_state)
                print(f"💾 Saved updated login state to: {storage_state}")
                
        print("📓 Notebook loaded successfully.")
        
        # Click Studio Button
        print("🎬 Clicking 'Studio' Panel...")
        studio_btn = page.locator('button:has-text("Studio"), [aria-label="Studio"]')
        await studio_btn.wait_for(state="visible", timeout=15000)
        await studio_btn.click()
        await page.wait_for_timeout(5000)
        
        # Click Video Overview (Direct Selector)
        print("📺 Opening 'Video Overview'...")
        video_overview_card = page.locator('h3:has-text("Video Overview"), [role="button"]:has-text("Video Overview")')
        # Fallback locator if custom cards are used
        if await video_overview_card.count() == 0:
            video_overview_card = page.locator('div:has-text("Video Overview")').last
            
        await video_overview_card.wait_for(state="visible", timeout=10000)
        await video_overview_card.click()
        await page.wait_for_timeout(5000)
        
        # Select Short Format Tab
        print("📱 Selecting 'Short' video format...")
        short_tab = page.locator('button:has-text("Short"), [role="tab"]:has-text("Short")')
        await short_tab.wait_for(state="visible", timeout=10000)
        await short_tab.click()
        await page.wait_for_timeout(3000)
        
        # Click Generate
        print("🟢 Clicking 'Generate' button...")
        generate_btn = page.locator('button:has-text("Generate"), button:has-text("Create")')
        await generate_btn.wait_for(state="visible", timeout=10000)
        await generate_btn.click()
        await page.wait_for_timeout(5000)
        
        print("✅ Short Video Generation Triggered!")
        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Selector-based NotebookLM Shorts Automation for PC/Servers")
    parser.add_argument("--notebook-id", help="Notebook ID to use")
    parser.add_argument("--no-headless", action="store_true", help="Run browser in headful mode for login/VNC")
    args = parser.parse_args()
    
    config = load_config()
    n_id = args.notebook_id or config.get("notebook_id")
    s_state = config.get("storage_state_path", "config/storage_state.json")
    
    if not n_id or n_id == "YOUR_NOTEBOOK_ID_HERE":
        print("❌ Please specify a notebook ID via --notebook-id or configure it in config.json")
        sys.exit(1)
        
    asyncio.run(run_playwright(n_id, s_state, headless=not args.no_headless))

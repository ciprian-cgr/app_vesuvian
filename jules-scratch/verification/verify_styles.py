import re
from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Go to the app
    page.goto("http://localhost:5173/")

    # Log in
    page.get_by_placeholder("Email").fill("test@example.com")
    page.get_by_placeholder("Password").fill("password")
    page.get_by_role("button", name="Sign in").click()

    # Verify Dashboard and take screenshot
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/dashboard.png")

    # Navigate to Settings
    page.get_by_role("button", name="Settings").click()

    # Verify Settings page and take screenshot
    expect(page.get_by_role("heading", name="Settings")).to_be_visible()
    page.screenshot(path="jules-scratch/verification/settings.png")

    # Clean up
    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
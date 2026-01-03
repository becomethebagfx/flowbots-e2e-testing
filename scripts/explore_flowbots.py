#!/usr/bin/env python3
"""Explore FLOWBOTS web app and take screenshots - runs on Windows Vultr"""

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# FLOWBOTS credentials
EMAIL = "brandon@flowbotsai.com"
PASSWORD = "FlowBots2026"
APP_URL = "https://app.flowbotsai.com"
SCREENSHOT_DIR = r"C:\flowbots_lab\screenshots"

def setup_driver():
    """Setup Edge browser with options"""
    options = Options()
    # Don't run headless so we can see GUI
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")

    service = Service(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    return driver

def take_screenshot(driver, name):
    """Take and save screenshot"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    filepath = os.path.join(SCREENSHOT_DIR, f"{name}_{int(time.time())}.png")
    driver.save_screenshot(filepath)
    print(f"Screenshot saved: {filepath}")
    return filepath

def explore_flowbots():
    """Explore FLOWBOTS web app"""
    driver = setup_driver()

    try:
        # 1. Navigate to app
        print("Navigating to FLOWBOTS app...")
        driver.get(APP_URL)
        time.sleep(3)
        take_screenshot(driver, "01_landing")

        # 2. Look for login form or dashboard
        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)

        # Try to find login form
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email']"))
            )
            print("Found login form - logging in...")
            email_field.send_keys(EMAIL)

            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys(PASSWORD)

            take_screenshot(driver, "02_login_filled")

            # Find and click login button
            login_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit'], button:contains('Login'), button:contains('Sign')")
            login_btn.click()
            time.sleep(5)

            take_screenshot(driver, "03_after_login")

        except Exception as e:
            print(f"Login form not found or already logged in: {e}")
            take_screenshot(driver, "02_no_login_form")

        # 3. Explore the dashboard/convert page
        print("Current URL after login:", driver.current_url)

        # Look for navigation elements
        try:
            nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .nav a, [role='navigation'] a")
            print(f"Found {len(nav_links)} navigation links:")
            for link in nav_links[:10]:
                print(f"  - {link.text}: {link.get_attribute('href')}")
        except:
            print("Could not find navigation links")

        # Look for convert/upload elements
        try:
            upload_area = driver.find_element(By.CSS_SELECTOR, "[type='file'], .upload, .dropzone, [class*='drop'], [class*='upload']")
            print("Found upload area!")
            take_screenshot(driver, "04_upload_area")
        except:
            print("No upload area found directly")

        # Look for platform selection
        try:
            selects = driver.find_elements(By.CSS_SELECTOR, "select, [role='listbox'], .dropdown")
            print(f"Found {len(selects)} dropdown/select elements")
            for sel in selects[:5]:
                print(f"  - {sel.get_attribute('class')}")
        except:
            print("No platform selects found")

        # Final screenshot of current state
        take_screenshot(driver, "05_final_state")

        # Get page source for analysis
        with open(os.path.join(SCREENSHOT_DIR, "page_source.html"), "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("Page source saved")

        return {
            "status": "success",
            "url": driver.current_url,
            "title": driver.title
        }

    except Exception as e:
        print(f"Error: {e}")
        take_screenshot(driver, "error")
        return {"status": "error", "error": str(e)}

    finally:
        driver.quit()

if __name__ == "__main__":
    result = explore_flowbots()
    print("\nResult:", result)

#!/usr/bin/env python3
"""Explore FLOWBOTS web app in headless mode - runs on Windows Vultr via SSH"""

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
    """Setup Edge browser with headless options for SSH"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

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
    """Explore FLOWBOTS web app in headless mode"""
    print("Setting up Edge headless driver...")
    driver = setup_driver()

    try:
        # 1. Navigate to app
        print("Navigating to FLOWBOTS app...")
        driver.get(APP_URL)
        time.sleep(3)
        take_screenshot(driver, "01_landing")

        # 2. Look for login form or dashboard
        print(f"Page title: {driver.title}")
        print(f"Current URL: {driver.current_url}")

        # Try to find login form
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email'], input[name='email'], input[id*='email']"))
            )
            print("Found login form - logging in...")
            email_field.clear()
            email_field.send_keys(EMAIL)

            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.clear()
            password_field.send_keys(PASSWORD)

            take_screenshot(driver, "02_login_filled")

            # Find and click login button
            login_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            login_btn.click()
            time.sleep(5)

            take_screenshot(driver, "03_after_login")
            print(f"After login URL: {driver.current_url}")

        except Exception as e:
            print(f"Login form handling: {e}")
            take_screenshot(driver, "02_no_login_form")

        # 3. Explore the dashboard/convert page
        print(f"Current URL: {driver.current_url}")

        # Look for navigation elements
        try:
            nav_links = driver.find_elements(By.CSS_SELECTOR, "nav a, .nav a, [role='navigation'] a, a[href*='convert'], a[href*='dashboard']")
            print(f"Found {len(nav_links)} navigation links:")
            for link in nav_links[:10]:
                href = link.get_attribute('href') or 'no-href'
                text = link.text or link.get_attribute('aria-label') or 'no-text'
                print(f"  - {text}: {href}")
        except Exception as e:
            print(f"Navigation scan: {e}")

        # Look for convert/upload elements
        try:
            upload_elements = driver.find_elements(By.CSS_SELECTOR, "[type='file'], .upload, .dropzone, [class*='drop'], [class*='upload'], [class*='file']")
            print(f"Found {len(upload_elements)} upload-related elements")
            for el in upload_elements[:5]:
                print(f"  - Tag: {el.tag_name}, Class: {el.get_attribute('class')}")
        except Exception as e:
            print(f"Upload scan: {e}")

        # Look for platform selection
        try:
            selects = driver.find_elements(By.CSS_SELECTOR, "select, [role='listbox'], [role='combobox'], .dropdown, [class*='select']")
            print(f"Found {len(selects)} dropdown/select elements")
            for sel in selects[:5]:
                print(f"  - Tag: {sel.tag_name}, Class: {sel.get_attribute('class')}")
        except Exception as e:
            print(f"Dropdown scan: {e}")

        # Final screenshot
        take_screenshot(driver, "05_final_state")

        # Save page source
        source_path = os.path.join(SCREENSHOT_DIR, "page_source.html")
        with open(source_path, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(f"Page source saved to {source_path}")

        return {
            "status": "success",
            "url": driver.current_url,
            "title": driver.title
        }

    except Exception as e:
        print(f"Error: {e}")
        try:
            take_screenshot(driver, "error")
        except:
            pass
        return {"status": "error", "error": str(e)}

    finally:
        driver.quit()

if __name__ == "__main__":
    result = explore_flowbots()
    print(f"\nResult: {result}")

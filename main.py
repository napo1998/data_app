from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, WebDriverException
import os
import time
import random
from datetime import datetime

# Streamlit app URL from environment variable (or default)
STREAMLIT_URL = os.environ.get("STREAMLIT_APP_URL", "https://fitnessapp-4bk3rhl9g5r5ipgpmckvnc.streamlit.app/")

def setup_driver():
    """Configure and return a Chrome WebDriver instance"""
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Add user agent to appear more human-like
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), 
        options=options
    )
    return driver

def simulate_user_interaction(driver, wait):
    """Simulate realistic user interaction with the page"""
    try:
        # Scroll down the page slowly
        print("Simulating page scroll...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(random.uniform(1, 3))
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(1, 2))
        
        # Scroll back up
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.uniform(0.5, 1.5))
        
        # Try to find and interact with common Streamlit elements
        try:
            # Look for buttons, inputs, or other interactive elements
            elements = driver.find_elements(By.TAG_NAME, "button")
            if elements:
                print(f"Found {len(elements)} interactive elements")
        except:
            pass
            
        print("User interaction simulation complete ✅")
        
    except Exception as e:
        print(f"Note: Could not complete all interactions: {e}")

def wake_up_app(driver, wait):
    """Check if app is sleeping and wake it up if needed"""
    try:
        # Look for the wake-up button
        button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes, get this app back up')]"))
        )
        print("Wake-up button found. Clicking...")
        button.click()
        
        # After clicking, check if it disappears
        try:
            wait.until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "//button[contains(text(),'Yes, get this app back up')]")
                )
            )
            print("Button clicked and disappeared ✅ (app is waking up)")
            # Wait a bit longer for the app to fully load
            time.sleep(5)
            return True
        except TimeoutException:
            print("Button was clicked but did NOT disappear ❌")
            return False
            
    except TimeoutException:
        # No button at all → app is assumed to be awake
        print("No wake-up button found. App is already awake ✅")
        return True

def visit_app():
    """Main function to visit the app and simulate traffic"""
    driver = None
    try:
        print(f"\n{'='*60}")
        print(f"Starting visit at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Target URL: {STREAMLIT_URL}")
        print(f"{'='*60}\n")
        
        driver = setup_driver()
        
        # Visit the page
        print(f"Opening {STREAMLIT_URL}...")
        driver.get(STREAMLIT_URL)
        
        # Create wait object with longer timeout
        wait = WebDriverWait(driver, 20)
        
        # Wait for initial page load
        time.sleep(3)
        
        # Check if app needs to be woken up
        if wake_up_app(driver, wait):
            # Simulate realistic user behavior
            time.sleep(random.uniform(2, 4))
            simulate_user_interaction(driver, wait)
            
            # Stay on page for a bit longer
            stay_duration = random.uniform(10, 20)
            print(f"Staying on page for {stay_duration:.1f} seconds...")
            time.sleep(stay_duration)
            
            print("✅ Visit completed successfully")
            return True
        else:
            print("❌ Failed to wake up app")
            return False
            
    except WebDriverException as e:
        print(f"❌ WebDriver error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if driver:
            driver.quit()
            print("Browser closed")

def main():
    """Run a single visit"""
    success = visit_app()
    exit(0 if success else 1)

if __name__ == "__main__":
    main()

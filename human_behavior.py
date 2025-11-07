"""
Human Behavior Simulator - Makes bot act like real human
"""

import random
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import *

class HumanBehavior:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
    
    def random_sleep(self, min_time, max_time):
        """Sleep for random time"""
        sleep_time = random.uniform(min_time, max_time)
        time.sleep(sleep_time)
        return sleep_time
    
    def simulate_reading(self, page_text=""):
        """Simulate reading page content"""
        if not SIMULATE_READING:
            return
        
        # Count words on page
        word_count = len(page_text.split()) if page_text else 500
        
        # Calculate reading time (based on WPM)
        reading_time = (word_count / READING_SPEED_WPM) * 60
        
        # Add randomness
        reading_time = reading_time * random.uniform(0.7, 1.3)
        
        # Clamp to min/max
        reading_time = max(MIN_PAGE_TIME, min(reading_time, MAX_PAGE_TIME))
        
        print(f"   📖 Simulating reading ({word_count} words, {reading_time:.1f}s)...")
        time.sleep(reading_time)
    
    def smooth_scroll(self):
        """Scroll page smoothly like human"""
        if not ENABLE_SCROLLING:
            return
        
        print(f"   📜 Scrolling through page...")
        
        # Get page height
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        
        num_scrolls = random.randint(MIN_SCROLLS, MAX_SCROLLS)
        
        for i in range(num_scrolls):
            # Random scroll distance
            scroll_amount = random.randint(100, 500)
            
            # Scroll smoothly
            self.driver.execute_script(f"window.scrollBy({{top: {scroll_amount}, behavior: 'smooth'}});")
            
            # Random pause (simulating reading)
            pause = random.uniform(SCROLL_PAUSE_MIN, SCROLL_PAUSE_MAX)
            time.sleep(pause)
            
            # Sometimes scroll up a bit (human behavior)
            if random.random() < 0.2:
                scroll_back = random.randint(50, 150)
                self.driver.execute_script(f"window.scrollBy({{top: -{scroll_back}, behavior: 'smooth'}});")
                time.sleep(random.uniform(0.3, 1.0))
    
    def random_mouse_movement(self):
        """Move mouse randomly on page"""
        if not ENABLE_MOUSE_MOVEMENT:
            return
        
        try:
            for _ in range(MOUSE_MOVEMENTS_PER_PAGE):
                # Random coordinates
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                
                # Move mouse
                self.actions.move_by_offset(x, y).perform()
                
                # Small pause
                time.sleep(random.uniform(0.1, 0.5))
                
                # Reset position
                self.actions.move_by_offset(-x, -y).perform()
                
        except Exception as e:
            pass  # Mouse movement not critical
    
    def random_click(self):
        """Click random element on page"""
        if not ENABLE_RANDOM_CLICKS:
            return
        
        if random.random() > CLICK_PROBABILITY:
            return
        
        try:
            # Find clickable elements
            clickable_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                'a, button, [onclick], input[type="submit"]')
            
            if clickable_elements:
                # Filter visible elements
                visible_elements = [el for el in clickable_elements if el.is_displayed()]
                
                if visible_elements:
                    element = random.choice(visible_elements)
                    
                    # Scroll to element
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                    time.sleep(0.5)
                    
                    print(f"   🖱️  Clicking element: {element.tag_name}")
                    
                    # Click
                    element.click()
                    
                    # Wait for page to load
                    time.sleep(random.uniform(1, 3))
                    
        except Exception as e:
            print(f"   ⚠️  Click failed: {str(e)[:50]}")
    
    def simulate_form_interaction(self):
        """Simulate interacting with forms (if present)"""
        try:
            # Find input fields
            inputs = self.driver.find_elements(By.CSS_SELECTOR, 'input[type="text"], input[type="email"], textarea')
            
            if inputs:
                print(f"   ⌨️  Found {len(inputs)} input fields")
                
                for input_field in inputs[:2]:  # Interact with max 2 fields
                    if input_field.is_displayed():
                        # Click field
                        input_field.click()
                        time.sleep(random.uniform(0.5, 1.5))
                        
                        # Type slowly (human-like)
                        fake_text = "test" + str(random.randint(100, 999))
                        for char in fake_text:
                            input_field.send_keys(char)
                            time.sleep(random.uniform(0.1, 0.3))
                        
                        time.sleep(random.uniform(0.5, 1.5))
                        
        except Exception as e:
            pass  # Form interaction not critical
    
    def human_page_interaction(self):
        """Complete human-like page interaction"""
        print(f"   👤 Simulating human behavior...")
        
        # 1. Initial page load wait
        self.random_sleep(1, 3)
        
        # 2. Mouse movement
        self.random_mouse_movement()
        
        # 3. Scroll through page
        self.smooth_scroll()
        
        # 4. Read content
        try:
            page_text = self.driver.find_element(By.TAG_NAME, 'body').text
            self.simulate_reading(page_text)
        except:
            self.random_sleep(MIN_PAGE_TIME, MAX_PAGE_TIME)
        
        # 5. Random click (maybe)
        self.random_click()
        
        # 6. More scrolling
        if random.random() < 0.5:
            self.smooth_scroll()
        
        # 7. Form interaction (if exists)
        if random.random() < 0.3:
            self.simulate_form_interaction()
        
        print(f"   ✅ Human behavior simulation complete")

"""
Browser Manager - Handles browser setup and configuration
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import random
from config import *

class BrowserManager:
    def __init__(self, proxy=None, user_agent=None):
        self.proxy = proxy
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.driver = None
    
    def setup_chrome_options(self):
        """Configure Chrome options for realistic browsing"""
        chrome_options = Options()
        
        # Headless mode (runs in background)
        if HEADLESS_MODE:
            chrome_options.add_argument('--headless')
        
        # User agent
        chrome_options.add_argument(f'user-agent={self.user_agent}')
        
        # Window size
        window_size = random.choice(RANDOM_WINDOW_SIZES)
        chrome_options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
        
        # Proxy configuration
        if self.proxy:
            proxy_str = self.proxy.get('proxy_string')
            chrome_options.add_argument(f'--proxy-server=http://{proxy_str}')
        
        # Anti-detection options
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Additional realistic options
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument('--disable-popup-blocking')
        
        # Language and timezone
        chrome_options.add_argument('--lang=en-US')
        
        # Random preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_settings.popups": 0,
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        return chrome_options
    
    def create_driver(self):
        """Create and configure browser driver"""
        try:
            chrome_options = self.setup_chrome_options()
            
            # Create driver (Termux uses system Chrome)
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Set timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            
            # Execute CDP commands (anti-detection)
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.user_agent
            })
            
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            return self.driver
            
        except Exception as e:
            print(f"❌ Error creating browser: {str(e)}")
            return None
    
    def close_driver(self):
        """Close browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass

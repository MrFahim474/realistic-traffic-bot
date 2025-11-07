"""
Configuration File - Advanced Realistic Traffic Bot
"""

# ========================================
# WEBSITE CONFIGURATION
# ========================================

# YOUR WEBSITE URL - CHANGE THIS!
TARGET_WEBSITE = "https://example.com"

# Pages to visit on your website (will randomly select)
TARGET_PAGES = [
    "/",
    "/about",
    "/contact",
    "/blog",
    "/services",
]

# ========================================
# TRAFFIC SETTINGS
# ========================================

# How many visitors to simulate
TOTAL_VISITS = 50

# Delay between each visitor (seconds)
MIN_VISITOR_DELAY = 10
MAX_VISITOR_DELAY = 30

# ========================================
# HUMAN BEHAVIOR SETTINGS
# ========================================

# Time spent on each page (seconds)
MIN_PAGE_TIME = 5
MAX_PAGE_TIME = 45

# Scrolling behavior
ENABLE_SCROLLING = True
MIN_SCROLLS = 3
MAX_SCROLLS = 10
SCROLL_PAUSE_MIN = 0.5
SCROLL_PAUSE_MAX = 3.0

# Mouse movement
ENABLE_MOUSE_MOVEMENT = True
MOUSE_MOVEMENTS_PER_PAGE = 5

# Clicking behavior
ENABLE_RANDOM_CLICKS = True
CLICK_PROBABILITY = 0.3  # 30% chance to click something

# Reading simulation
SIMULATE_READING = True
READING_SPEED_WPM = 200  # Words per minute

# ========================================
# PROXY SETTINGS
# ========================================

USE_PROXIES = True

# Free proxy sources (automatically fetched)
FREE_PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
]

# Proxy timeout (seconds)
PROXY_TIMEOUT = 15

# Maximum proxies to test
MAX_PROXIES_TO_TEST = 50

# ========================================
# BROWSER SETTINGS
# ========================================

# Run browser in background (headless mode)
HEADLESS_MODE = True

# Browser window size
WINDOW_WIDTH = 1366
WINDOW_HEIGHT = 768

# Random window sizes (simulates different devices)
RANDOM_WINDOW_SIZES = [
    (1920, 1080),  # Desktop
    (1366, 768),   # Laptop
    (1440, 900),   # Desktop
    (1536, 864),   # Laptop
    (360, 640),    # Mobile
    (375, 667),    # iPhone
    (414, 896),    # iPhone Plus
    (768, 1024),   # iPad
]

# User agents (different browsers)
USER_AGENTS = [
    # Chrome on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Firefox on Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    # Chrome on Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    # Safari on Mac
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    # Chrome on Android
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    # Chrome on iPhone
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/120.0.0.0 Mobile/15E148 Safari/604.1",
]

# ========================================
# LOGGING SETTINGS
# ========================================

ENABLE_LOGGING = True
LOG_FILE = "traffic_bot.log"
VERBOSE = True

# Save detailed report
SAVE_REPORT = True
REPORT_FILE = "traffic_report.txt"

# ========================================
# SAFETY SETTINGS
# ========================================

# Respect robots.txt
RESPECT_ROBOTS_TXT = True

# Maximum requests per hour (rate limiting)
MAX_REQUESTS_PER_HOUR = 100

# Enable safe mode (extra delays and checks)
SAFE_MODE = True

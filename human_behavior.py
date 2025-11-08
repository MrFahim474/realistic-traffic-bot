"""
Human Behavior Simulator - Simulates realistic browsing patterns
Works without browser automation
"""

import random
import time
from config import *

class HumanBehavior:
    def __init__(self):
        self.session_duration = 0
        
    def calculate_realistic_timings(self):
        """Calculate how long a human would spend"""
        
        # Random page view time
        page_time = random.uniform(MIN_PAGE_TIME, MAX_PAGE_TIME)
        
        # Simulate different browsing patterns
        pattern = random.choice(['quick', 'normal', 'detailed'])
        
        if pattern == 'quick':
            # Quick visitor: 5-15 seconds
            page_time = random.uniform(5, 15)
            scrolls = random.randint(2, 4)
        elif pattern == 'normal':
            # Normal visitor: 15-45 seconds
            page_time = random.uniform(15, 45)
            scrolls = random.randint(4, 8)
        else:
            # Detailed visitor: 45-120 seconds
            page_time = random.uniform(45, 120)
            scrolls = random.randint(8, 15)
        
        return {
            'page_time': page_time,
            'scrolls': scrolls,
            'pattern': pattern
        }
    
    def simulate_page_visit(self):
        """Simulate realistic page visit behavior"""
        
        timings = self.calculate_realistic_timings()
        
        print(f"   👤 Visitor Pattern: {timings['pattern'].upper()}")
        print(f"   ⏱️  Planned duration: {timings['page_time']:.1f}s")
        print(f"   📜 Simulated scrolls: {timings['scrolls']}")
        
        # Initial page load delay
        initial_delay = random.uniform(0.5, 2.0)
        print(f"   ⏳ Page loading... ({initial_delay:.1f}s)")
        time.sleep(initial_delay)
        
        # Simulate scrolling with pauses
        total_scroll_time = 0
        scroll_duration = timings['page_time'] * 0.6  # 60% time scrolling
        
        for i in range(timings['scrolls']):
            scroll_pause = random.uniform(
                scroll_duration / timings['scrolls'] * 0.5,
                scroll_duration / timings['scrolls'] * 1.5
            )
            
            if VERBOSE:
                print(f"   📖 Reading section {i+1}/{timings['scrolls']}... ({scroll_pause:.1f}s)")
            
            time.sleep(scroll_pause)
            total_scroll_time += scroll_pause
        
        # Remaining time (final reading)
        remaining_time = timings['page_time'] - initial_delay - total_scroll_time
        
        if remaining_time > 0:
            print(f"   🤔 Final reading... ({remaining_time:.1f}s)")
            time.sleep(remaining_time)
        
        self.session_duration = initial_delay + total_scroll_time + remaining_time
        
        print(f"   ✅ Visit completed: {self.session_duration:.1f}s total")
        
        return self.session_duration

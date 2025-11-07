"""
Proxy Manager - Fetches and validates free proxies
"""

import requests
import random
import time
from config import *

class ProxyManager:
    def __init__(self):
        self.proxy_list = []
        self.working_proxies = []
        self.failed_proxies = set()
        self.current_proxy_index = 0
        
    def fetch_free_proxies(self):
        """Fetch proxies from free sources"""
        print("\n🔍 Fetching free proxies from GitHub sources...")
        
        all_proxies = []
        
        for source_url in FREE_PROXY_SOURCES:
            try:
                print(f"📥 Downloading from: {source_url[:50]}...")
                response = requests.get(source_url, timeout=10)
                
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    all_proxies.extend(proxies)
                    print(f"   ✅ Got {len(proxies)} proxies")
                else:
                    print(f"   ❌ Failed (Status: {response.status_code})")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:50]}")
        
        # Clean and deduplicate
        self.proxy_list = list(set([p.strip() for p in all_proxies if ':' in p]))
        print(f"\n📊 Total unique proxies collected: {len(self.proxy_list)}")
        
        return len(self.proxy_list)
    
    def test_proxy(self, proxy_str):
        """Test if a proxy works"""
        proxy_dict = {
            'http': f'http://{proxy_str}',
            'https': f'http://{proxy_str}'
        }
        
        test_urls = [
            'http://httpbin.org/ip',
            'http://ip-api.com/json',
            'http://icanhazip.com'
        ]
        
        for test_url in test_urls:
            try:
                response = requests.get(
                    test_url,
                    proxies=proxy_dict,
                    timeout=PROXY_TIMEOUT
                )
                
                if response.status_code == 200:
                    return True
                    
            except:
                continue
        
        return False
    
    def validate_proxies(self, max_test=None):
        """Validate collected proxies"""
        if not self.proxy_list:
            print("❌ No proxies to validate!")
            return
        
        max_test = max_test or MAX_PROXIES_TO_TEST
        test_count = min(len(self.proxy_list), max_test)
        
        print(f"\n🧪 Testing {test_count} proxies (this may take a few minutes)...")
        print("=" * 60)
        
        tested = 0
        
        for proxy in self.proxy_list[:test_count]:
            tested += 1
            
            # Progress indicator
            progress = (tested / test_count) * 100
            print(f"Testing [{tested}/{test_count}] {progress:.1f}% - {proxy[:20]}...", end='')
            
            if self.test_proxy(proxy):
                self.working_proxies.append(proxy)
                print(" ✅ WORKING")
            else:
                self.failed_proxies.add(proxy)
                print(" ❌ Failed")
        
        print("=" * 60)
        print(f"✅ Working proxies: {len(self.working_proxies)}")
        print(f"❌ Failed proxies: {len(self.failed_proxies)}")
        
        if len(self.working_proxies) == 0:
            print("\n⚠️  WARNING: No working proxies found!")
            print("💡 Suggestion: The bot will run with direct connection (no proxy)")
        
        return len(self.working_proxies)
    
    def get_random_proxy(self):
        """Get a random working proxy"""
        if not self.working_proxies:
            return None
        
        proxy_str = random.choice(self.working_proxies)
        
        return {
            'http': f'http://{proxy_str}',
            'https': f'http://{proxy_str}',
            'proxy_string': proxy_str
        }
    
    def mark_proxy_failed(self, proxy_dict):
        """Mark a proxy as failed and remove it"""
        if not proxy_dict:
            return
        
        proxy_str = proxy_dict.get('proxy_string')
        
        if proxy_str and proxy_str in self.working_proxies:
            self.working_proxies.remove(proxy_str)
            self.failed_proxies.add(proxy_str)
            print(f"❌ Removed failed proxy: {proxy_str[:30]}")
    
    def get_stats(self):
        """Get proxy statistics"""
        return {
            'total_collected': len(self.proxy_list),
            'working': len(self.working_proxies),
            'failed': len(self.failed_proxies)
        }

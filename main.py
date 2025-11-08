#!/usr/bin/env python3
"""
Realistic Traffic Bot - Requests-based version
Works perfectly in Termux without browser drivers
"""

import sys
import time
import random
import requests
from datetime import datetime
from config import *
from proxy_manager import ProxyManager
from human_behavior import HumanBehavior

class RealisticTrafficBot:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.stats = {
            'total_visits': 0,
            'successful': 0,
            'failed': 0,
            'by_proxy': 0,
            'by_direct': 0,
            'total_time': 0,
            'start_time': None,
            'end_time': None,
            'status_codes': {},
        }
        self.log_file = None
        
        if ENABLE_LOGGING:
            self.log_file = open(LOG_FILE, 'a', encoding='utf-8')
    
    def log(self, message, to_file=True):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        
        if VERBOSE:
            print(log_msg)
        
        if to_file and self.log_file:
            self.log_file.write(log_msg + '\n')
            self.log_file.flush()
    
    def setup(self):
        """Initialize the bot"""
        print("\n" + "="*70)
        print("🤖 REALISTIC TRAFFIC BOT - LIGHTWEIGHT VERSION")
        print("="*70)
        print(f"\n🎯 Target Website: {TARGET_WEBSITE}")
        print(f"📊 Planned Visits: {TOTAL_VISITS}")
        print(f"🌐 Use Proxies: {USE_PROXIES}")
        print(f"🧠 Human Behavior: Realistic timing and patterns")
        print("="*70)
        
        # Warning
        print("\n⚠️  IMPORTANT REMINDERS:")
        print("   • Only test YOUR OWN website")
        print("   • Be respectful of server resources")
        print("   • This is for educational/testing purposes only")
        print("="*70)
        
        confirm = input("\n✅ Ready to start? (type 'yes' to continue): ").strip().lower()
        
        if confirm != 'yes':
            print("\n❌ Bot cancelled.")
            sys.exit(0)
        
        # Setup proxies if enabled
        if USE_PROXIES:
            self.log("\n📡 Setting up proxy system...")
            self.proxy_manager.fetch_free_proxies()
            self.proxy_manager.validate_proxies()
            
            proxy_stats = self.proxy_manager.get_stats()
            self.log(f"✅ Proxy setup complete: {proxy_stats['working']} working proxies")
        
        self.log("\n✅ Setup complete! Starting visits...\n")
    
    def generate_realistic_headers(self):
        """Generate realistic browser headers"""
        
        user_agent = random.choice(USER_AGENTS)
        
        # Random accept language
        languages = [
            'en-US,en;q=0.9',
            'en-GB,en;q=0.9',
            'en-US,en;q=0.9,es;q=0.8',
            'en-CA,en;q=0.9,fr;q=0.8',
        ]
        
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': random.choice(languages),
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        
        # Randomly add referer (30% chance)
        if random.random() < 0.3:
            referers = [
                'https://www.google.com/',
                'https://www.bing.com/',
                'https://duckduckgo.com/',
            ]
            headers['Referer'] = random.choice(referers)
        
        return headers
    
    def simulate_visit(self, visit_number):
        """Simulate one complete website visit"""
        self.log(f"\n{'='*70}")
        self.log(f"🚀 VISIT #{visit_number}/{TOTAL_VISITS}")
        self.log(f"{'='*70}")
        
        # Get proxy (if enabled)
        proxy = None
        proxy_dict = None
        
        if USE_PROXIES and self.proxy_manager.working_proxies:
            proxy = self.proxy_manager.get_random_proxy()
            if proxy:
                proxy_dict = {
                    'http': proxy['http'],
                    'https': proxy['https']
                }
                self.log(f"🌐 Using proxy: {proxy['proxy_string'][:30]}...")
                self.stats['by_proxy'] += 1
            else:
                self.log(f"📍 Using direct connection (no working proxies)")
                self.stats['by_direct'] += 1
        else:
            self.log(f"📍 Using direct connection")
            self.stats['by_direct'] += 1
        
        # Select random page
        if TARGET_PAGES and len(TARGET_PAGES) > 0:
            page = random.choice(TARGET_PAGES)
            # Fix double slash issue
            base = TARGET_WEBSITE.rstrip('/')
            page_clean = page if page.startswith('/') else '/' + page
            full_url = base + page_clean
        else:
            full_url = TARGET_WEBSITE
        
        self.log(f"📄 Target page: {full_url}")
        
        # Generate realistic headers
        headers = self.generate_realistic_headers()
        
        try:
            # Human behavior simulation BEFORE request
            human = HumanBehavior()
            
            # Make request
            self.log(f"🌍 Sending request...")
            start_time = time.time()
            
            session = requests.Session()
            
            response = session.get(
                full_url,
                headers=headers,
                proxies=proxy_dict,
                timeout=30,
                allow_redirects=True,
                verify=True
            )
            
            request_time = time.time() - start_time
            
            # Log response
            status_code = response.status_code
            self.stats['status_codes'][status_code] = self.stats['status_codes'].get(status_code, 0) + 1
            
            self.log(f"✅ Response received: Status {status_code} in {request_time:.2f}s")
            self.log(f"📦 Content size: {len(response.content)} bytes")
            
            if status_code == 200:
                # Simulate human reading/interaction time
                behavior_time = human.simulate_page_visit()
                
                # Calculate total time
                total_time = request_time + behavior_time
                self.stats['total_time'] += total_time
                
                self.log(f"⏱️  Total visit duration: {total_time:.2f}s")
                self.log(f"✅ Visit #{visit_number} completed successfully!")
                
                self.stats['successful'] += 1
                
                # Close session
                session.close()
                
                return True
            else:
                self.log(f"⚠️  Non-200 status code: {status_code}")
                self.stats['failed'] += 1
                session.close()
                return False
            
        except requests.exceptions.ProxyError as e:
            self.log(f"❌ Proxy error: {str(e)[:80]}")
            
            # Mark proxy as failed
            if proxy:
                self.proxy_manager.mark_proxy_failed(proxy)
            
            self.stats['failed'] += 1
            return False
            
        except requests.exceptions.Timeout:
            self.log(f"❌ Request timeout after 30s")
            
            if proxy:
                self.proxy_manager.mark_proxy_failed(proxy)
            
            self.stats['failed'] += 1
            return False
            
        except requests.exceptions.RequestException as e:
            error_msg = str(e)[:100]
            self.log(f"❌ Request failed: {error_msg}")
            
            if proxy:
                self.proxy_manager.mark_proxy_failed(proxy)
            
            self.stats['failed'] += 1
            return False
    
    def run(self):
        """Run the complete bot"""
        self.stats['start_time'] = datetime.now()
        
        for visit_num in range(1, TOTAL_VISITS + 1):
            self.stats['total_visits'] += 1
            
            # Simulate visit
            success = self.simulate_visit(visit_num)
            
            # Delay before next visit
            if visit_num < TOTAL_VISITS:
                delay = random.uniform(MIN_VISITOR_DELAY, MAX_VISITOR_DELAY)
                self.log(f"\n⏸️  Waiting {delay:.1f}s before next visit...")
                time.sleep(delay)
        
        self.stats['end_time'] = datetime.now()
        self.show_final_report()
    
    def show_final_report(self):
        """Show final statistics"""
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        
        # Avoid division by zero
        avg_visit_time = 0
        if self.stats['successful'] > 0:
            avg_visit_time = self.stats['total_time'] / self.stats['successful']
        
        success_rate = 0
        if self.stats['total_visits'] > 0:
            success_rate = (self.stats['successful'] / self.stats['total_visits']) * 100
        
        report = f"""

{'='*70}
📊 FINAL REPORT
{'='*70}

⏱️  Total Duration: {duration/60:.1f} minutes ({duration:.0f} seconds)

📈 VISIT STATISTICS:
   • Total Visits Attempted: {self.stats['total_visits']}
   • Successful: {self.stats['successful']} ✅
   • Failed: {self.stats['failed']} ❌
   • Success Rate: {success_rate:.1f}%

🌐 CONNECTION STATISTICS:
   • Via Proxy: {self.stats['by_proxy']}
   • Direct Connection: {self.stats['by_direct']}

📡 HTTP STATUS CODES:
"""
        
        for status, count in sorted(self.stats['status_codes'].items()):
            report += f"   • {status}: {count} times\n"
        
        report += f"""
⏱️  TIME STATISTICS:
   • Total Time on Site: {self.stats['total_time']/60:.1f} minutes
   • Average Visit Duration: {avg_visit_time:.1f}s
   
💾 Detailed logs saved to: {LOG_FILE}

{'='*70}
✅ BOT EXECUTION COMPLETE!
{'='*70}
"""
        
        print(report)
        
        if self.log_file:
            self.log_file.write(report)
            self.log_file.close()
        
        # Save report to separate file
        if SAVE_REPORT:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n📄 Report also saved to: {REPORT_FILE}\n")

def main():
    """Main entry point"""
    try:
        bot = RealisticTrafficBot()
        bot.setup()
        bot.run()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Bot stopped by user (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

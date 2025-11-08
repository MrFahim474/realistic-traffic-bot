"""
Browser Manager - Firefox (robust, webdriver-manager) version

Notes:
- Uses webdriver-manager to automatically download geckodriver.
- Will try to auto-detect Firefox binary. If not found, set env var FIREFOX_BINARY to the binary path.
- On Termux (Android) it's often difficult to run a full Firefox. See instructions after this file.
"""

import os
import random
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from config import *

def find_firefox_binary():
    """
    Try to find firefox binary on PATH or via common locations.
    You can override by setting environment variable FIREFOX_BINARY.
    """
    # 1) explicit environment override
    env_path = os.environ.get("FIREFOX_BINARY")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2) check PATH
    path_bin = shutil.which("firefox") or shutil.which("firefox-esr") or shutil.which("mozilla-firefox")
    if path_bin:
        return path_bin

    # 3) common Linux locations (not exhaustive)
    common_paths = [
        "/usr/bin/firefox",
        "/usr/local/bin/firefox",
        "/opt/firefox/firefox",
        "/data/data/com.termux/files/usr/bin/firefox"  # possible Termux custom location
    ]
    for p in common_paths:
        if os.path.isfile(p):
            return p

    return None


class BrowserManager:
    def __init__(self, proxy=None, user_agent=None):
        """
        proxy: dict returned from your ProxyManager.get_random_proxy() (contains 'proxy_string')
        user_agent: optional string to force UA, otherwise random from config
        """
        self.proxy = proxy
        self.user_agent = user_agent or random.choice(USER_AGENTS)
        self.driver = None

    def setup_firefox_options(self):
        opts = Options()

        # Headless
        if HEADLESS_MODE:
            # use headless if possible
            opts.add_argument("--headless=new")  # newer headless mode where supported
        # set user agent
        if self.user_agent:
            opts.set_preference("general.useragent.override", self.user_agent)

        # Anti-detection / realism preferences
        opts.set_preference("dom.webdriver.enabled", False)
        opts.set_preference("useAutomationExtension", False)
        opts.set_preference("media.peerconnection.enabled", False)
        opts.set_preference("intl.accept_languages", "en-US, en")
        opts.set_preference("permissions.default.image", 1)

        # Proxy preferences (if provided)
        if self.proxy:
            proxy_str = self.proxy.get("proxy_string") or ""
            parts = proxy_str.split(":")
            if len(parts) >= 2:
                host = parts[0]
                try:
                    port = int(parts[1])
                except Exception:
                    port = None
                if port:
                    opts.set_preference("network.proxy.type", 1)
                    opts.set_preference("network.proxy.http", host)
                    opts.set_preference("network.proxy.http_port", port)
                    opts.set_preference("network.proxy.ssl", host)
                    opts.set_preference("network.proxy.ssl_port", port)
                    # If socks proxy is used you may need to set network.proxy.socks and .socks_port
            else:
                # if the proxy string isn't host:port, ignore and continue (ProxyManager should provide host:port)
                pass

        # Window size will be set after driver creation
        return opts

    def create_driver(self):
        """
        Create Firefox webdriver using webdriver-manager to provide geckodriver.
        Returns: selenium.webdriver or None on failure.
        """
        # 1) find firefox binary
        firefox_bin = find_firefox_binary()
        if not firefox_bin:
            print("❌ Firefox binary not found.")
            print("   • If you're on Android/Termux: installing native Firefox is often not available via pkg.")
            print("   • Option A (recommended): run this project on a PC/VM where Firefox is available.")
            print("   • Option B: supply FIREFOX_BINARY environment variable pointing to a compatible firefox binary.")
            print("   • Option C (advanced): use a remote Selenium server or cloud provider.")
            return None

        # 2) prepare options and service
        options = self.setup_firefox_options()
        options.binary_location = firefox_bin

        try:
            # webdriver-manager will download a compatible geckodriver binary and return its path
            gecko_path = GeckoDriverManager().install()
            service = Service(gecko_path)

            # instantiate driver
            self.driver = webdriver.Firefox(service=service, options=options)

            # set window size randomly to simulate devices
            try:
                window_size = random.choice(RANDOM_WINDOW_SIZES)
                self.driver.set_window_size(window_size[0], window_size[1])
            except Exception:
                pass

            # small sanity timeouts
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)

            return self.driver

        except Exception as e:
            # friendly error + tips
            err = str(e)
            print(f"❌ Error creating Firefox driver: {err}")
            print("   Troubleshooting hints:")
            print("   • Make sure geckodriver is compatible with the installed Firefox version.")
            print("   • If running on Android/Termux, geckodriver and Firefox binaries may be incompatible.")
            print("   • Consider running this code on a Linux/Windows PC or a cheap VPS where Firefox + geckodriver are supported.")
            print("   • You can set FIREFOX_BINARY env var to point to an installed firefox binary.")
            return None

    def close_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
            self.driver = None

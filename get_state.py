"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                            File: get_state.py
                            Date: 2026/02/16
                        Version: 0.1-2026.02.16

===============================================================================

                     Copyright (C) 2026 SpudWorks Labs.

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU Affero General Public License as published
        by the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Affero General Public License for more details.

        You should have received a copy of the GNU Affero General Public License
        along with this program. If not, see <https://www.gnu.org/licenses/>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""


# ~ Import Standard Modules. ~ #
import time

# ~ Import Third-Party Modules. ~ #
from playwright.sync_api import sync_playwright


def get_web_state(url, output_path="state_capture.png"):
    """
        ~ Obtain the state of the web url. ~

        Attributes:
            - url             (String) : The URL of the Web App to check.
            - output_path     (String) : Filename to save the screenshot state.

        Returns:
            - Dict                     : The filename of the screenshot,
                                         the device scale factor, and the
                                         viewport size.
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (X11; Linux x86_64)\
                        SpudScout/1.0 (Bot;\
                        +https://github.com/SpudWorks-Labs/SpudScout)",
            viewport={'width': 1280, 'height': 720}
        )
        page    = context.new_page()

        print(f"[*] Navigating to '{url}' now...")
        
        page.goto(url, wait_until="domcontentloaded")

        time.sleep(2)

        dsf     = page.evaluate("window.devicePixelRatio")
        viewport_size = page.viewport_size

        page.screenshot(path=output_path, full_page=False)

        print(f"[+] State Captured!")
        print(f"    - Viewport: {viewport_size['width']}x{viewport_size['height']}")
        print(f"    - Device Scale Factor: {dsf}")
        print(f"    - Screenshot Saved: {output_path}")

        browser.close()

        return {
            "screenshot": output_path,
            "dsf": dsf,
            "viewport": viewport_size
        }


if __name__ == "__main__":
    state = get_web_state("https://news.ycombinator.com")

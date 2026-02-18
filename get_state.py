"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                            File: get_state.py
                            Date: 2026/02/16
                        Version: 0.5.1-2026.02.17

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
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

# ~ Import Third-Party Modules. ~ #
from playwright.sync_api import sync_playwright


class StateManager:
    """
    ~ Manages the Playwright lifecycle and capture the
      visual state of the web. ~
    """

    def __init__(self, headless=False):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.headless = headless

        moz_agent = "Mozilla/5.0 (X11; Linux x86_64)"
        scout_repo = "https://github.com/SpudWorks-Labs/SpudScout"
        scout_agent = f"SpudScout/0.3.1 (Bot; +{scout_repo})"
        self.user_agent = f"{moz_agent} {scout_agent}"

    def start(self):
        """
        ~ Launch the browser session. ~
        """

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            user_agent=self.user_agent,
            viewport={'width': 1280, 'height': 720}
        )
        self.page = self.context.new_page()

        logging.info("Browser session started!")

    def can_scout_visit(self, url):
        """
        ~ Ethical robots.txt validation. ~ #
        """

        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
        robo_parser = RobotFileParser()

        try:
            robo_parser.set_url(base_url)
            robo_parser.read()

            return robo_parser.can_fetch("SpudScout", url)

        except Exception as e:
            logging.warning(f"Could not parse robots.txt at {base_url}: {e}")

            return False

    def capture_view(self, url, output_path="state_capture.png"):
        """
        ~ Navigates and captures the current pixels. ~
        """

        if not self.page:
            self.start()

        if not self.can_scout_visit(url):
            logging.error(f"Access denied by robots.txt for {url}")

            return None

        logging.info(f"Navigating to {url}")

        self.page.goto(url, wait_until="networkidle")

        self._human_scroll()

        dsf = self.page.evaluate("window.devicePixelRatio")
        self.page.screenshot(path=output_path)

        return {
            "screenshot": output_path,
            "dsf": dsf,
            "viewport": self.page.viewport_size,
            "page_handle": self.page
        }

    def _human_scroll(self):
        """
        ~ Private method to trigger lazy-loading. ~
        """

        for _ in range(3):
            self.page.mouse.wheel(0, 500)
            time.sleep(0.5)

        self.page.evaluate("window.scrollTo(0, 0)")
        time.sleep(0.5)

    def shutdown(self):
        """
        ~ Cleanly closes all playwright resources. ~
        """

        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()

        logging.info("Browser session was terminated.")


"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                             File: scout.py
                            Date: 2026/02/17
                        Version: 0.3-2026.02.17

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

# ~ Import System Modules. ~ #
import sys

# ~ Import Custom Modules. ~ #
import get_state
from processor import VisionProcessor
from classifier import ElementClassifier


class Scout:
    def __init__(self):
        self.processor = VisionProcessor()
        self.classifier = ElementClassifier()

    def scrape(self, url):
        state = get_state.get_web_state(url)

        candidates = self.processor.process_state(state["screenshot"])
        cleaned = self.processor.clean_candidates(candidates)
        chip_paths = self.processor.extract_chips(state["screenshot"], cleaned)

        results = self.classifier.classify_candidates(cleaned)

        for result in results:
            print(f"    Element: {result.get('text', 'Unknown')}")


def display_usage():
    """
    ~ Display the correct usage syntax for the scouter. ~
    """

    print(f"Usage: python {sys.argv[0]} <url>")


if __name__ == "__main__":
    scout = Scout()
    args = sys.argv[1:]

    if not args:
        display_usage()

    url = args[0]

    scout.scrape(url)

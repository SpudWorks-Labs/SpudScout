"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                             File: scout.py
                            Date: 2026/02/17
                        Version: 0.3.1-2026.02.18

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
import logging
import json

# ~ Import Local Modules. ~ #
from get_state import StateManager
from processor import VisionProcessor
from classifier import ElementClassifier


logging.basicConfig(level=logging.INFO, format='[*] %(message)s')


class Scout:
    """
    ~ The main class for SpudScout. ~

    Functions:
        __init__                       : Initialize the SpudScout.
        observe                        : Ethically observe a site.
        export_state                   : Export the webpage state as JSON.
    """

    def __init__(self):
        """
        ~ Initialize the SpudScout and its attributes. ~

        Attributes:
            - processor
                     (VisionProcessor) : The module to process an image.
            - classifier               
                   (ElementClassifier) : The module to classify each element.
            - current_state     (List) : A list of current elements.
        """

        self.state_manager = StateManager()
        self.processor = VisionProcessor()
        self.classifier = ElementClassifier()
        self.current_state = []

    def observe(self, url):
        """
        ~ Ethically observe the data from the web url. ~

        Arguments:
            - url             (String) : The url to the webpage.
        """

        logging.info(f"Initiating observation on: {url}")

        state = self.state_manager.capture_view(url)

        if not state:
            logging.error("Failed to capture data, check url or the robots.txt")
            return []

        self.processor.dsf = state.get("dsf", 1.0)

        raw_candidates = self.processor.process_state(state["screenshot"])
        cleaned = self.processor.clean_candidates(raw_candidates)

        self.processor.extract_chips(state["screenshot"], cleaned)
        self.current_state = self.classifier.classify_candidates(cleaned)

        self.processor.draw_debug_overlay(state["screenshot"], self.current_state)

        logging.info(f"Observation complete. Found {len(self.current_state)} interactive elements.")

        return self.current_state


    def export_state(self, filename="web_state.json"):
        """
        ~ Export the web apps visual state into a JSON file. ~
        """

        if not self.current_state:
            logging.warning("No state available to export.")
            return

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.current_state, f, indent=4)

        logging.info(f"State successfully exported to '{filename}'!")


def display_usage():
    """
    ~ Display the correct usage syntax for the scouter. ~
    """

    print(f"Usage: python {sys.argv[0]} <url>")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        display_usage()
        sys.exit(1)

    target_url = sys.argv[1]

    scout = Scout()
    results = scout.observe(target_url)

    if results:
        scout.export_state()

        for result in results:
            print(f"    - [{result['point']}] : {result.get('text', 'Unknown')}")
            
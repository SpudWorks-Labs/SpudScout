"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                           File: classifier.py
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

# ~ Import Standard Modules. ~ #
import os
import json

# ~ Import Third-PArty Modules. # ~
import cv2
import pytesseract
import numpy as np


class ElementClassifier:
    """
    ~ The Element Classifier for SpudScout. ~

    Functions:
        - __init__                     : Initialize the classifier.
        - extract_text_from_chip       : Extract text from each chip.
        - classify_candidates          : Classify each candidate.
    """

    def __init__(self):
        """
        ~ Initialize the Element Classifier. ~

        Attributes:
            - tesseract_config 
                           (RegString) : The tesseract config string.
        """

        self.tesseract_config = r'--oem 3 --psm 7'

    def extract_text_from_chip(self, chip_path):
        """
        ~ Reads text from a single image chip using OCR.
          includes preprocessing to handle images with
          white-text-on-dark-backgrounds. ~

        Arguments:
            - chip_path       (String) : The path to the chip.
        """

        # ~ Check if the path exists. ~ #
        if not os.path.exists(chip_path):
            return ""

        img = cv2.imread(chip_path)

        # ~ Check if the image has been loaded, ~ #
        if img is None:
            return ""

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        text = pytesseract.image_to_string(binary, config=self.tesseract_config).strip()

        if not text or len(text) < 2:
            inverted = cv2.bitwise_not(binary)
            text_inverted = pytesseract.image_to_string(inverted, config=self.tesseract_config).strip()

            if len(text_inverted) > len(text):
                text = text_inverted

        return text

    def classify_candidates(self, candidates, chip_dir="chips"):
        """
        ~ Iterates through the candidates and attaches OCR text to them. ~

        Arguments:
            - candidates (List) : A list of all candidates.
            - chip_dir (String) : The directory containing the chips.
        """

        classified_elements = []

        print(f"[*] Analyzing {len(candidates)} UI elements")

        for i, candidate in enumerate(candidates):
            chip_path = f"{chip_dir}/chip_{i}.png"
            raw_text = self.extract_text_from_chip(chip_path)
            clean_text = raw_text.replace("\n", " ").strip()

            if len(clean_text) >= 2:
                candidate["text"] = clean_text
                classified_elements.append(candidate)

                print(f"    -> [Chip {i}] Found: '{clean_text}'")

            else:
                pass

        return classified_elements


if __name__ == "__main__":
    classifier = ElementClassifier()

    dummy_candidates = [{"id": i for i in range(5)}]
    results = classifier.classify_candidates(dummy_candidates)

    print("[+] Classification complete. Sample results:")

    for result in results:
        print(f"    Element: {result.get('text', 'Unknown')}")

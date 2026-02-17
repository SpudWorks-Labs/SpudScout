"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                           File: processor.py
                            Date: 2026/02/17
                        Version: 0.2-2026.02.17

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

# ~ Import Standard Libraries. ~ #
import os

# ~ Import Third-Party Modules. ~ #
import cv2
import numpy as np


class VisionProcessor:
    """
    ~ This class allows SpudScout to process images with vision. ~

    Functions:
        __init__ : 
        process_state :
        draw_debug_overlay :
        extract_chips :
    """

    def __init__(self, dsf=1.0):
        self.dsf = dsf
        self.min_area = 400
        self.max_area = 150000

    def process_state(self, image_path):
        """
        ~ Analyzes the screenshot and returns a list of clickable centers. ~

        Attributes:
            - image_path      (String) : The path to the image.

        Returns:
            - List                     : A list of all possible candidates.
        """

        raw_img = cv2.imread(image_path)

        # ~ Check if the image can be read. ~ #
        if raw_img is None:
            raise ValueError("Could not read the image at '{image_path}'!")

        # ~ Convert to grayscale, apply Canny and locate contours within. ~ #
        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        smoothed = cv2.bilateralFilter(gray, 9, 75, 75)
        edges = cv2.Canny(smoothed, 50, 150)
        kernel = np.ones((3, 3,), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates = []

        # ~ Check all contours for proper ones. ~ #
        for contour in contours:
            area = cv2.contourArea(contour)

            # ~ Check if the area is within tha area range. ~ #
            if self.min_area < area < self.max_area:
                M = cv2.moments(contour)

                if M["m00"] != 0:
                    cx_px = int(M["m10"] / M["m00"])
                    cy_px = int(M["m01"] / M["m00"])

                    cx_pt = cx_px / self.dsf
                    cy_pt = cy_px / self.dsf

                    candidates.append({
                        "point": (cx_pt, cy_pt),
                        "area": area,
                        "bbox": cv2.boundingRect(contour)
                    })

        return candidates

    def draw_debug_overlay(self, image_path, candidates, output_path="debug_vision.png"):
        """
        ~ Draws bounding boxes and clicking points on a copy of the screenshot
          to verify what the VisionProcessor is detecting. ~

        Attributes:
            - image_path      (String) : The path to the image.
            - candidates        (List) : A list of all of the candidates.
            - output_path     (String) : A filename to save the debug image.
        """

        overlay_img = cv2.imread(image_path)

        # ~ Locate each candidate and mark it with a box and a dot. ~ #
        for candidate in candidates:
            x, y, w, h = candidate["bbox"]

            cx_px = int(candidate["point"][0] * self.dsf)
            cy_px = int(candidate["point"][1] * self.dsf)

            cv2.rectangle(overlay_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(overlay_img, (cx_px, cy_px), 5, (0, 0, 255), -1)
            cv2.putText(overlay_img, f"Area: {int(candidate["area"])}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            cv2.imwrite(output_path, overlay_img)

            print(f"[+] Debugging overlay saved to: {output_path}")

    def extract_chips(self, image_path, candidates, output_dir="chips"):
        """
        ~ Crops each detected candidate from the original image and saves it. 
          This allows Tesseract of an LLM to read the contents inside
          the 'buttons'. ~

        Attributes:
            - image_path      (String) : The path to the image.
            - candidates        (List) : A list of candidates.
            - output_dir      (String) : The name of the output directory.

        Returns:
            - List                     : A list of the paths of each chip.
        """

        # ~ Create the chip directory. ~ #
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        img = cv2.imread(image_path)
        chip_paths = []

        # ~ Save each chip from the candidate. ~ #
        for i, candidate in enumerate(candidates):
            x, y, w, h = candidate["bbox"]
            chip = img[y:y + h, x:x + w]
            chip_name = f"{output_dir}/chip_{i}.png"
            cv2.imwrite(chip_name, chip)
            chip_paths.append(chip_name)

        print(f"[+] Extracted {len(chip_paths)} chips to {output_dir}/")

        return chip_paths


if __name__ == "__main__":
    vp = VisionProcessor()
    candidates = vp.process_state("state_capture.png")
    vp.draw_debug_overlay("state_capture.png", candidates)
    vp.extract_chips("state_capture.png", candidates)

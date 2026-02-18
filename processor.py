"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                            Company: SpudWorks
                         Program Name: SpudScout
       Description: An Agentic Web Scraper that uses Computer Vision.
                           File: processor.py
                            Date: 2026/02/17
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

# ~ Import Standard Libraries. ~ #
import os
import logging

# ~ Import Third-Party Modules. ~ #
import cv2
import numpy as np


class VisionProcessor:
    """
    ~ This class allows SpudScout to process images with vision. ~

    Functions:
        __init__                       : Initialize the vision processor;
        process_state                  : Process the web apps state.
        draw_debug_overlay             : Create the debug image with overlays.
        extract_chips                  : Extract chips from processed images.
    """

    def __init__(self, dsf=1.0):
        """
        ~ Initialize the Vision Processor Module. ~

        Arguments:
            - dsf              (Float) : The Device Scale Factor.

        Attributes:
            dsf                (Float) : The Device Scale Factor.
            min_area             (Int) : The minimum size for the area 
                                         of the clickables.
            max_area             (Int) : The maximum size for the area
                                         of the clickables.
        """

        self.dsf = dsf
        self.min_area = 800
        self.max_area = 200000

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
            logging.error(f"VisionProcessor could not read image: {image_path}")

            return []

        # ~ Convert to grayscale, apply Canny and locate contours within. ~ #
        gray = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
        smoothed = cv2.bilateralFilter(gray, 9, 75, 75)
        edges = cv2.Canny(smoothed, 50, 150)

        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)

        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        candidates = []

        # ~ Check all contours for proper ones. ~ #
        for contour in contours:
            area = cv2.contourArea(contour)

            # ~ Check if the area is within tha area range. ~ #
            if self.min_area < area < self.max_area:
                
                # ~ Calculate the middle click point. ~ #
                M = cv2.moments(contour)

                if M["m00"] != 0:
                    cx = (int(M["m10"] / M["m00"])) / self.dsf
                    cy = (int(M["m01"] / M["m00"])) / self.dsf

                    candidates.append({
                        "point": (cx, cy),
                        "area": area,
                        "bbox": cv2.boundingRect(contour)
                    })

        return self.clean_candidates(candidates)

    def clean_candidates(self, candidates):
        """
        ~ Removes overlapping boxes or redundant noise.
          If one box is entirely inside another, we usually
          only want the parent or the specific child. For now,
          we'll just filter by a stricter area. ~

        Returns:
            - List                     : A list of refined candidates.
        """

        if not candidates:
            return []

        candidates = sorted(candidates, key=lambda x: x['area'], reverse=True)
        refined = []

        for i, candidate in enumerate(candidates):
            x, y, w, h = candidate["bbox"]
            aspect_ratio = w / float(h)

            if aspect_ratio < 0.05 or aspect_ratio > 20:
                continue

            is_redundant = False

            for ref in refined:
                rx, ry, rw, rh = ref["bbox"]

                if (x >= rx and y >= ry and (x+w) <= (rx+rw) and (y+h) <= (ry+rh)):
                    is_redundant = True
                    break

            if not is_redundant:
                refined.append(candidate)
        
        return refined

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
        if img is None: return []

        chip_paths = []

        # ~ Save each chip from the candidate. ~ #
        for i, candidate in enumerate(candidates):
            x, y, w, h = candidate["bbox"]
            pad = 2
            chip = img[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad]
            path = f"{output_dir}/chip_{i}.png"

            cv2.imwrite(path, chip)
            chip_paths.append(path)

        logging.info(f"Extracted {len(chip_paths)} chips.")

        return chip_paths


    def draw_debug_overlay(self, image_path, candidates, output="debug_vision.png"):
        """
        ~ Draws bounding boxes and clicking points on a copy of the screenshot
          to verify what the VisionProcessor is detecting. ~

        Attributes:
            - image_path      (String) : The path to the image.
            - candidates        (List) : A list of all of the candidates.
            - output          (String) : A filename to save the debug image.
        """

        img = cv2.imread(image_path)
        if img is None: return

        # ~ Locate each candidate and mark it with a box and a dot. ~ #
        for candidate in candidates:
            x, y, w, h = candidate["bbox"]

            px = int(candidate["point"][0] * self.dsf)
            py = int(candidate["point"][1] * self.dsf)

            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(img, (px, py), 5, (0, 0, 255), -1)

        cv2.imwrite(output, img)


if __name__ == "__main__":
    vp = VisionProcessor()
    candidates = vp.clean_candidates(vp.process_state("state_capture.png"))
    vp.draw_debug_overlay("state_capture.png", candidates)
    vp.extract_chips("state_capture.png", candidates)

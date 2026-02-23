 # SpudScout Architecture: The "Vision-First" Web Scanner.


## Summary

SpudScout uses a hybrid approach: **CV for speed, VLM for intelligence.**
We treat the website as a physical canvas, using a normalized 0-1000 coordinate system
to bridge the gap between pixel-perfect CV and context-aware AI.


### Phase 1: Element Discovery

* **Action:** Playwright launches a headless browser and navigates to the target.
* **Metadata:** We extract the **DSF (Device Scale Factor)** and view-port dimensions.
* **Output:** A raw "Physical Pixel" screenshot.
* **Action:** OpenCV runs Canny Edge detection and contour mapping.
* **Goal:** Find high contrast elements (buttons, inputs, etc.) quickly.
* **Logic:** Store these in `all_candidates` using **Physical Pixels**.
* **Preperation (The Bridge):**
- **Normalization:** Map Physical Pixels to Normalized [0, 1000] coordinates.
- **Prompting:** Inject CV-found coordinates into the VLM prompt to reduce redundant computation.
* **VLM Task:** Find what the CV Stage has missed.
* **Integration:** The VLM returns missing elements (e.g., text links, ghost buttons, etc.) in 0-1000 format.
* **De-Duplicate:** Apply **NMS (Non-Maximum Supression)** logic to merge CV and VLM candidates into a unified interactive map.
* **Final Output:** A unified list of interactive elements.
* **Debug:** A `debug_vision.png` overlay for developer verification.


### Phase 2: Data Extraction

This phase extracts all of the data on the page so that is can be used for datasets and such.
**To be planned later.**


### Phase 3: Automation

Final step of the Scouter that allows it to interact with the site.
**Also to be planned later.** 
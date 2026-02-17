# SpudScout

An **Agentic Visual Web Scraper** capable of complex automation without the
"Selector Hell" of modern, obfuscated web apps. By leveraging **Canny Edge 
Detection** and **Quantized LLMs**, SpudScout navigates the web like a human:
by looking at the interface, not just the source code.

---


## Why SpudScout?

Traditional scrapers break when the DOM structure changes. SpudScout maintains
resilience by prioritizing **visual landmarks** over brittle CSS selectors.

* **Theme-Agnostic:** Grayscale + Canny processing ensures UI landmarks are
                      identified regardless of Dark/Light mode transitions.
* **Privacy-First:** 100% local execution. No screenshots or data ever leave
                     your machine for third-party API processing.
* **Resource Lean:** Architected for **CPU-only** environments using GGUF
                     quantization for local inference.

---


## Tech Stack & Constraints

We intentionally limit our scope to master the fundamentals of
Computer Vision (CV) and Browser Automation.

* **Logic:** Python 3.11+
* **Automation:** Playwright (Synchronous) — *Chosen for predictable state management.*
* **Vision:** OpenCV (Grayscale + Canny) & NumPy.
* **OCR:** Tesseract. (Fallback for text-region validation)
* **Brain:** Ollama. (GGUF Models) — *CPU-optimized local inference.*


## Installation (Arch/EndevourOS)

*1. System Dependencies*
```bash
sudo pacman -S tesseract tesseract-data-eng opencv hdf5
```

*2. Environment Setup.*
```bash
python -m venv venv
source venv/bin/activate
pip install playwright opencv-python numpy pytesseract
playwright install chromium
```


## Core Values

*1. Coordinate Math & Scaling.*
We do not trust raw coordinate values, so SpudScout calculates the *Device Scale Factor (DSF)* 
to map screenshot pixels to viewport points.

    **Constraint:** Always verify (Viewport × DSF) == ScreenshotWidth

*2. Humanity-First Scraping.*
Since we are guests on the web, SpudScout enforces the following rules:
* *Jittered Latency:* No "inhuman" clicking speeds.
* *Robots.txt Respect:* Automatic parsing and adherence.
* *Custom User-Agents:* Transparent identification.

---


## Roadmap

Here is the following phase-map for the project:
* *Phase 1:* CV-based button detection. (Canny Edge) <COMPLETE>
* *Phase 2:* GGUF-integrated intent parsing. (Ollama)
* *Phase 3:* Autonomous "Spud-Loops" for multi-page navigation.

---


## Contributing

This is a "Professional Grade" lab. We value *Deep Work* over "**Quick Fixes**" in
our codebase. If ou are submitting a PR, expect a deep review. We do not want "It works";
we want to know why this is a better use of the resources for the task it completes.


## Important Notes & Acknowledgements

This project is created by Human developers with the help of AI-Assistance.


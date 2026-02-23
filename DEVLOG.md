**Note:** All time is in ***UTC***

*2026/02/16*
* 17:01
    - The project has been created and the base documentation
      files and structure have been created.

* 15:18
    - The README file has been created and the Local LMs have been
      installed and tested for functionality.

* 21:20
    - Created the `get_state.py` file to obtain the state of
      the webpage via the URL.

* 21:50
    - Added a `robots.txt` checker and a scroll function to avoid "lazy-loading"
      to get the most out of the data.

* 04:52
    - Created the `processor.py` file for the Visual Processing module.

* 06:53
    - The `processor.py` module now processes possible candidates for buttons
      in the image provided.

* 20:03
	- Created the skeleton of the `classifier.py` module.
	- Updated the comments and documentation.

* 20:58
	- Finished the base of the `cassifier.py` module and now it can function.
	- Now creating a `scout.py` file to orchestrate the pipelines.

* 21:34
	- It works as intended and can now read the text on the screen.

*2026/02/18*
* 17:04
	- Staring an AI code audit and found the following on `scout.py`:
		* Keep browser open for agentic actions.
		* Rename `scrape` to `observe` for proper naming convention.
		* Need error handling on `get_web_state()` to avoid crashes.
		* Lacks memory, a `current_state` variable could help.
		* `logging` is better than `print` in these circumstances.

* 17:44
	- Refactored `scout.py` and now moving on to `get_state.py`.
	- `get_state.py` needs the following changes:
		* The browser needs a seperate class to persist.
		* Add a network idle to ensure all is loaded.
		* Returning the `page` as well as the screenshot is better.

* 18:18
	- Refactored the `get_state.py` module now moving onto `processing.py`.
	- The following needs to be done for `processing.py`:
		* Keep the overlapping box that makes the most sense.
		* Safety check to avoid the `ValueError` that would crash the program.
		* Read image once pass it around for efficiency.

* 18:50
	- Refactored the `processing.py` module and now moving on to the `classifier.py`
	  after a short break.

* 19:56
	- The `classifier.py` module needs the following refactors:
		* Regex cleaning to strip common OCR hallucinations.
		* Log instead of printing.
		* `--psm 6` might be bettter than `--psm 7` for the config.

* 20:17
	- Refactored the `classifier.py` module.

* 21:56
	- About to step away soon, need to finish the artifacts that appear.

*2026/02/19*
* 21:44
	- Picking away at finding each element with many filters.

*2026/02/23*
* 21:11
	- Created the `ARCHITECTURE.md` file so I can stop playing with values and 
	  try a more calculated aproach... Which I should have done to begin with.


### TO-DO

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

### TO-DO
[!] Refactor code.
[!] Clean the code.
[!] AI code audit.

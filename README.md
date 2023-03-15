# Google Maps Scraper

This is personal project and not completed, tweaked the code based of [this](https://github.com/MightyKyloRen/GoogleMapsScrapping) for my own usage. 

Changelogs:
- Extended the scrape list to allow more scrapes
- Optimised the initial codes by removing some duplicated codes (try/except and for-loop) and also include code reusability
- Added more informational print statements to allow me to debug and understand number of scrape queries i'm receiving.


### Todo:
- Require to open an excel file and loop into the company names and search for related companies.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip -r requirements.txt
```

## Usage

You are required to amend the SEARCH_TERM, LOCATION and maybe the FINAL_URL if you're not intending to use it to search for terms Singapore in main.py. Not using in SG, the geo coordinates in the FINAL_URL will need to change.  

```python
python3 main.py
```

## Credits
MightyKyloRen/GoogleMapsScrapping

# Google Maps Scraper

This is not completed personal project, tweaked the code based of [this](https://github.com/MightyKyloRen/GoogleMapsScrapping) for my own usage. Added some useful print statements and also extend the scrapes to allow longer lists instead of a fixed number.  

### Todo:
- Require to open an excel file and loop into the company names and search for related companies.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip: -r requirements.txt
```

## Usage

You are required to amend the SEARCH_TERM, LOCATION and maybe the FINAL_URL if you're not intending to use it to search for terms Singapore in main.py. Not using in SG, the geo coordinates in the FINAL_URL will need to change.  

```python
python3 main.py
```

## Credits
MightyKyloRen/GoogleMapsScrapping

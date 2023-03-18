# Google Maps Scraper

This is a personal project, working scraper for Google Maps with Email Finder. I kinda have similar problem as [this](https://medium.com/xeneta/boosting-sales-with-machine-learning-fbcf2e618be3) medium where you have a bunch of company names but sifting out this bunch of company names takes time. But of course, this company pays for another API service to provide description of the companies they scraped but I'm a poor student so I'm trying to keep it at 0 cost. My ultimate goal is try lead gen for local B2B and see if what Youtubers mentioned like Cold emails, Lead magnets, Facebook scrapes, Google scrapes would be effective for local businesses.  

Changelogs:
- Extended the download list to allow more scrapes
- Optimised the initial codes by removing some duplicated codes (try/except and for-loop) and also include code reusability
- Added threading so it helps the performance of the scraper, hoping to do parallelism too.
- Added proxies so that my IP won't get banned for scraping Google..
- Moved most of the selenium settings out to a settings file just to declutter my main file.
- Added more informational print statements to allow me to debug and understand number of scrape queries i'm receiving.

### Notes

18 March 2023
- I'm keeping main.py because it somehow can scrape more but still considerably lesser than what i thought, i still thinking of ways to overcome the 122 limit of searches. 
- After I've added the threading, i managed to fetch <120 queries but it didn't go scrape through all the queries (less than 60 queries scraped).
- Suggest to use main.py if you're looking at this repo and I won't be constantly updating this as I've jampacked with projects and exams.

### Todo:
- Require to open an excel file and loop into the company names and search for related companies.
- Test out these emails to send out cold emails and maybe lead magnets. 
- Will try to scrape website facebook/instagram/google analytics tool once i've stablised this tool. (removing util because it kinda not what is intended to do)

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

## Disclaimers
This code is to download data in bulk but just a personal project. The author is not responsible for any illegitimate use.
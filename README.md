# Data Entry Automation

This is a Python script I made that scrapes rental listing data (address, price, and link) from a Zillow clone site and automatically fills in and submits the responses from a Google Form to an external Google Sheet. 

## What it does

1. Scrapes a property listings page using `requests` to grab the HTML structure and `BeautifulSoup` to organize data pertaining to the:
   - Property addresses
   - Prices
   - Listing links
2. Cleans up the scraped text. 
3. Uses Selenium to open a Google Form and automatically type in the address, price, and link for every listing it scraped.
4. Submits the form, waits for the "response recorded" confirmation, then clicks "Submit another response" and repeats until every listing has been entered.

## Upcoming improvements.

- Add error handling in case a listing is missing a price or address
- Make the XPath selectors less fragile (they're tied to the form's exact layout right now)

## How to run it

1. Install the dependencies: `requests`, `beautifulsoup4`, `selenium`
2. Make sure you have Chrome and the matching ChromeDriver installed
3. Update `FORM_URL` and `ZILLOW_LINK` if you're pointing it at a different form/page.
4. Run the script.

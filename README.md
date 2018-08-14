

This is a project called async_phone_scraper created by Clayton Blythe on 2018/08/13

Email: claytondblythe@gmail.com

### Asynchronous Phone Number Scraper w/ Python

Uses asyncio, aiohttp, beautifulsoup, and regular expressions to search for 7 or 10 digit phone numbers on a website, with the goal of creating a set of phone numbers scraped from the internet with some given seed url. I set an default limit on phone number set size to be 1000 phone numbers for early stopping.

From my tests, it can scrape about 7000 websites for phone numbers in about 30 seconds. Right now, each unique url is visited at most once, but some domains could get a lot of requests, so checking robots.txt would be a nice thing to do. 
```
seed_url = "https://www.yelp.com/biz/muraccis-japanese-curry-and-grill-san-francisco"
async_scraper = AsyncPhoneScraper(seed_url=seed_url)
async_scraper.scrape_numbers()
print(f"Number of Phone Numbers scraped: {len(async_scraper.seen_numbers)}")
print(f"Number of Websites scraped: {len(async_scraper.visited_urls)}")
```
*Please use responsibly*

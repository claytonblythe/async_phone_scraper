

This is a project called async_phone_scraper created by Clayton Blythe on 2018/08/13

Email: claytondblythe@gmail.com

### Asynchronous Phone Number Scraper w/ Python

Uses asyncio, aiohttp, to maintain a set of phone numbers scraped from the internet with some seed url 
From my tests, it can scrape about 7000 websites for phone numbers in about 30 seconds. Right now, each unique url is visited at most once, but some domains could get a lot of requests, so checking robots.txt would be a nice thing to do. 

*Please use responsibly*

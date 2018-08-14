import aiohttp
import asyncio
from bs4 import BeautifulSoup
from queue import deque
import re
from urllib import parse


class AsyncPhoneScraper:
    def __init__(self, seed_url, max_phone_size=1000, batch_size=800):
        self.seed_url = seed_url
        self.url_q = deque([self.seed_url])
        self.seen_numbers = set()
        self.visited_urls = set()
        self.max_phone_size = max_phone_size
        self.batch_size = batch_size

    def clean_string(self, string):
        bad_chars = ["\n", "(", ")", "-", " ", '*', '.']
        for char in bad_chars:
            string = string.replace(char, "")
        return string

    def add_phone_numbers(self, soup):
        # Parse soup from page with regular expressions to get that page's set of unique phone numbers
        phone_num_pattern = re.compile(
            """(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})""")
        # Iterator is more memory efficient
        phone_num_iterator = re.finditer(phone_num_pattern, soup.text)
        for match in phone_num_iterator:
            clean_number = self.clean_string(match.group(1))
            self.seen_numbers.add(clean_number)

    def add_urls(self, base_url, soup):
        # Follow the relative paths by joining base url with relative url
        for a_tag in soup.find_all('a', href=True):
            link = parse.urljoin(base_url, a_tag.get('href'))
            if link not in self.visited_urls:
                self.url_q.append(link)
                self.visited_urls.add(link)

    async def fetch(self, session, url):
        timeout = aiohttp.ClientTimeout(total=5)
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    response.raise_for_status()
                return await response.text()
        except Exception as e:
            return ''

    async def fetch_all(self, urls, loop):
        async with aiohttp.ClientSession(loop=loop) as session:
            results = await asyncio.gather(*[loop.create_task(self.fetch(session, url))
                                             for url in urls])
        return results

    def scrape_numbers(self):
        while self.url_q and len(self.seen_numbers) < self.max_phone_size:
            loop = asyncio.get_event_loop()
            urls = [self.url_q.popleft() for _ in range(min(self.batch_size, len(self.url_q)))]
            htmls = loop.run_until_complete(self.fetch_all(urls, loop))
            for base_url, text in zip(urls, htmls):
                soup = BeautifulSoup(text, "html.parser")
                self.add_phone_numbers(soup)
                self.add_urls(base_url, soup)


if __name__ == "__main__":
    seed_url = "https://www.yelp.com/biz/muraccis-japanese-curry-and-grill-san-francisco"
    async_scraper = AsyncPhoneScraper(seed_url=seed_url)
    async_scraper.scrape_numbers()
    print(f"Number of Phone Numbers scraped: {len(async_scraper.seen_numbers)}")
    print(f"Number of Websites scraped: {len(async_scraper.visited_urls)}")

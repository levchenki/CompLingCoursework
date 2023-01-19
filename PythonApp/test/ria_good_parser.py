import asyncio
from datetime import datetime, timedelta
import re
from typing import Coroutine, List

import aiohttp
from bs4 import BeautifulSoup
from redis import Redis

redis = Redis(host='localhost', port=6379, db=0)


def fix_news_item_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


MAX_QUERIES = 1
CUR_QUERIES = 0
counter = 0

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'
user_agent2 = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
headers = {
    'User-Agent': user_agent
}


async def fetch_str(url: str) -> str:
    global CUR_QUERIES, counter
    mem = redis.get(url)
    if mem is not None:
        return mem
    while CUR_QUERIES >= MAX_QUERIES:
        await asyncio.sleep(0.2)
    CUR_QUERIES += 1
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as resp:
                    assert resp.status == 200, f'status: {resp.status}'
                    CUR_QUERIES -= 1
                    counter += 1
                    text_ = await resp.text()
                    if len(text_) > 200:
                        redis.set(url, text_)
                    print(f'[FETCH] {counter}')
                    return text_
        except Exception as e:
            print(f'[ERROR!] {e}')
            await asyncio.sleep(0.2)


async def process_1_news_by_url(url: str):
    bs = BeautifulSoup(await fetch_str(url), 'lxml')
    articles = bs.select('.article__body .article__block[data-type=text]')
    content = ' '.join([fix_news_item_text(el.text) for el in articles])
    news.add(content)
    cur_count = len(news)
    if cur_count % 100 == 0:
        print(f'processed news: {cur_count}')


async def process_page_with_20_news(page: int, date: datetime):
    # global date, page
    count = 20
    offset = page * count
    date_from = (date - timedelta(days=30)).strftime('%Y-%m-%d')
    date_to = date.strftime('%Y-%m-%d')
    url = f'https://ria.ru/services/search/getmore/?query=0&offset={offset}&list_sids[]=khoroshie-novosti&project[]=khoroshie-novosti&interval=period&date_from={date_from}&date_to={date_to}'
    # res = requests.get(bad_news_url)
    bs = BeautifulSoup(await fetch_str(url), 'lxml')
    anchors = bs.select('div.list-item a:nth-child(1)')
    links = [el['href'] for el in anchors]
    print(f'[PAGE]\t{page}\t{date_from}-{date_to}\t{len(links)}')
    await asyncio.gather(*[process_1_news_by_url(link) for link in links])


news: set[str] = set()


async def main():
    coroutines_list: List[Coroutine] = []
    start_date = datetime.now()
    for date in [start_date - timedelta(days=days) for days in range(0, 720, 30)]:
        coroutines_list.extend([process_page_with_20_news(page, date) for page in range(150)])
    await asyncio.gather(*coroutines_list)
    with open('good_news_ria.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(news))


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

import asyncio
import os
import re
from typing import List, TypeVar

import aiohttp

access_token = os.environ["token"]
T = TypeVar('T')


def fix_news_item_text(el: dict) -> str:
    return re.sub(r'\s+', ' ', el.get('text')).strip()


async def get_news(offset=0):
    count = 100
    offset = offset * count + 1
    bad_news_url = f'https://api.vk.com/method/wall.get?owner_id={target_group_id}&access_token={access_token}&v=5.131&count={count}&offset={offset}'
    # res = requests.get(bad_news_url)
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(bad_news_url) as res:
                    json_ = await res.json()
                    items = json_.get('response').get('items')
                    return [text for text in list(map(fix_news_item_text, items)) if 'https' not in text and len(text) > 50]
        except Exception as e:
            print(f'ERROR: {e}')
            await asyncio.sleep(1)
            pass


news: List[str] = []


async def main():
    # need_count = 10000
    for offset in range(60):
        news.extend(await get_news(offset))
        print(offset, sep='\t')
    with open('good_news3.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(news))


bad_news_group_id = -147781255
good_news_group_1_id = -122934507
good_news_group_2_id = -179156732
good_news_group_3_id = -179156732

target_group_id = good_news_group_3_id

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

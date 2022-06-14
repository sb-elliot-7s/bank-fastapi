import datetime

import aiohttp
from bs4 import BeautifulSoup


class CurrencyParserService:
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) "
                      "AppleWebKit/534.30 ("
                      "KHTML, like Gecko) Version/4.0 Safari/534.30"
    }
    URL = 'https://ru.investing.com/currencies/streaming-forex-rates-majors'

    async def _fetch(self, url: str):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url=url, headers=self.HEADERS) as response:
                return await response.text()

    async def parse_currency(self):
        text = await self._fetch(url=self.URL)
        soup = BeautifulSoup(text, 'html.parser')
        base = soup.find('table', class_='genTbl')
        currencies = base.find('tbody').find_all('tr')
        documents = []
        for currency in currencies:
            pair = currency.get('id').replace('pair_', '')
            dt = currency.find('td', class_=f'pid-{pair}-time')
            document = {
                'title': currency.find('td', class_='bold left noWrap elp plusIconTd').text,
                'bid': currency.find('td', class_=f'pid-{pair}-bid').text.strip(),
                'ask': currency.find('td', class_=f'pid-{pair}-ask').text.strip(),
                'change_in_value': currency.find('td', class_=f'pid-{pair}-pc').text.strip(),
                'change_in_procent': currency.find('td', class_=f'pid-{pair}-pcp').text.strip(),
                'dt': dt.text.strip(),
                'unix_ts': dt.get('data-value').strip()
            }
            documents.append(document)
        return {'created': datetime.datetime.now(), 'values': documents}

    async def exchange_money(self):
        await self._fetch(url='')

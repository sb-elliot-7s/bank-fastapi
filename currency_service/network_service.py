import datetime
import json

import aiohttp
from bs4 import BeautifulSoup
from configs import get_configs
from .schemas import ExchangeCurrencySchema


class NetworkService:
    @staticmethod
    async def fetch(url: str, headers: dict = None, params: dict = None):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.get(url=url, headers=headers, params=params) as response:
                return await response.text()


class CurrencyParserService(NetworkService):
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) "
                      "AppleWebKit/534.30 ("
                      "KHTML, like Gecko) Version/4.0 Safari/534.30"
    }
    URL = 'https://ru.investing.com/currencies/streaming-forex-rates-majors'

    async def parse_currency(self):
        text = await self.fetch(url=self.URL, headers=self.HEADERS)
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


class CurrencyExchangeService(NetworkService):
    EXCHANGE_URL = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&'

    async def exchange_rate(self, from_currency: str, to_currency: str):
        result = await self.fetch(url=self.EXCHANGE_URL, params={
            'from_currency': from_currency,
            'to_currency': to_currency,
            'apikey': get_configs().api_key
        })
        object = json.loads(result).get('Realtime Currency Exchange Rate')
        return ExchangeCurrencySchema.from_raw_object(object=object)

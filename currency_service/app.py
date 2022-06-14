import faust

from .network_service import CurrencyParserService
from .repositories import CurrencyRepositories
from .deps import currency_collection

app = faust.App('currency_parser', broker='kafka://localhost:9092')

currency_topic = app.topic('currency')


@app.task
async def start_work():
    print('start work')


@app.timer(interval=600)  # 10min
async def execute():
    parser = CurrencyParserService()
    documents = await parser.parse_currency()
    if documents:
        await CurrencyRepositories(currency_collection=currency_collection) \
            .save_currencies_to_db(documents=documents)

import faust
from .push_services import EmailPushService
from .constants import email_service_data

app = faust.App('push_service', broker='kafka://localhost:9092')


class Push(faust.Record):
    email: str
    code: str


push_service_topic = app.topic('push_service_topic', value_type=Push)


@app.agent(push_service_topic)
async def process(stream):
    async for message in stream:
        yield await EmailPushService(**email_service_data) \
            .send(to_client=message.email, message=message.code)

import aiosmtplib
from email.message import EmailMessage

from .interfaces.push_service import PushService


class EmailPushService(PushService):

    def __init__(self, host: str, port: int, username: str, password: str):
        self._username = username
        self.aiosmtplib_object = aiosmtplib.SMTP(hostname=host,
                                                 port=port,
                                                 username=username,
                                                 password=password,
                                                 use_tls=True)

    async def send(self, to_client: str, message: str) -> None:
        await self.aiosmtplib_object.connect()
        email_message = EmailMessage()
        email_message["From"] = self._username
        email_message["To"] = to_client
        email_message["Subject"] = 'Verification code'
        email_message.set_content(f'code {message}')

        await self.aiosmtplib_object.send_message(message=email_message, sender=self._username)
        await self.aiosmtplib_object.quit()


# from twilio.rest import Client


class SMSPushService(PushService):

    # account_sid = "ACbb0eff5f0e9dc9a0e44b2ab0b9a219ca"
    # auth_token = "your_auth_token"

    def __init__(self):
        # self._client = Client(account_sid, auth_token)
        pass

    async def send(self, to_client, message: str) -> None:
        # message = self._client.messages.create(
        #     to=to_client,
        #     from_="+15017250604",
        #     body=message)
        pass

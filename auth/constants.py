from enum import Enum

from configs import get_configs


class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'


email_service_data = {
    'host': get_configs().yandex_hostname,
    'port': get_configs().yandex_port,
    'username': get_configs().yandex_mail,
    'password': get_configs().yandex_password
}

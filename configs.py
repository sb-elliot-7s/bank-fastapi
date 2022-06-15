from pydantic import BaseSettings


class Configs(BaseSettings):
    secret_key: str
    exp_time: int
    temporary_token_exp_time: int
    algorithm: str

    api_key: str

    yandex_mail: str
    yandex_password: str
    yandex_hostname: str
    yandex_port: int

    key_for_pyotp: str
    tfa_interval: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_configs() -> Configs:
    return Configs()

from pydantic import BaseSettings


class Configs(BaseSettings):
    secret_key: str
    exp_time: int
    algorithm: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


def get_configs() -> Configs:
    return Configs()

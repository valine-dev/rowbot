from pydantic import BaseSettings


class Config(BaseSettings):

    # Local proxy
    use_proxy: bool = True
    proxy_http_url: str = 'http://127.0.0.1:8080/'
    proxy_https_url: str = 'http://127.0.0.1:8081/'

    # Twitter API
    twitter_api_token: str = ''

    retweet_control_objects: list = []
    retweet_muted_objects: list = []


    class Config:
        extra = "ignore"

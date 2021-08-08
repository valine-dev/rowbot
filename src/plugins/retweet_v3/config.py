from pydantic import BaseSettings


class Config(BaseSettings):

    # Local proxy
    use_proxy: bool = True
    proxy_http_url: str = 'http://127.0.0.1:8080/'
    proxy_https_url: str = 'http://127.0.0.1:8081/'

    retweet_control: list = []
    retweet_default: str = ''
    retweet_muted: list = []
    retweet_feeds: list = []

    retweet_platforms: list = ['twitter_api']

    class Config:
        extra = "ignore"

from pydantic import BaseSettings


class Config(BaseSettings):

    # Local proxy
    use_proxy: bool = True
    proxy_http_url: str = 'http://127.0.0.1:8080/'
    proxy_https_url: str = 'http://127.0.0.1:8081/'

    # Twitter API
    twitter_api_token: str = ''

    retweet_control_users: list = []
    retweet_default_tag: str = ''
    retweet_muted_users: list = []
    
    self_identity: str = ''

    class Config:
        extra = "ignore"

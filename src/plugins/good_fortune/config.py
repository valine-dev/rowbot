from pydantic import BaseSettings


class Config(BaseSettings):
    # 本地代理（仅HTTP）
    use_proxy: bool = True
    proxy_http_url: str = 'http://127.0.0.1:8080/'
    proxy_https_url: str = 'http://127.0.0.1:8081/'

    # 是否加入 HITOKOTO 生成的签语
    use_hitokoto: bool = True

    # 特殊签的概率
    special: int = 5

    class Config:
        extra = "ignore"

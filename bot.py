import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot

nonebot.init(apscheduler_autostart=True)
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
nonebot.load_plugins("src/plugins")

if __name__ == "__main__":
    nonebot.run()
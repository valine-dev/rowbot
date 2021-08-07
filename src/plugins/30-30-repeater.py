'''复读机插件，每侦测到两句以上的复读就跟随'''
import nonebot
from nonebot import on_message
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from pydantic import BaseSettings
from nonebot.typing import T_State

repeater = on_message(priority=2)


class Config(BaseSettings):
    # 使用复读的群
    repeater_control: list = []

    class Config:
        extra = 'ignore'


# 从全局配置读取配置
global_config = nonebot.get_driver().config
repeater_control = Config(**global_config.dict()).repeater_control

# 建立cache
__cache__: dict = {}
for group in repeater_control:
    # 初始化
    __cache__[group] = []


@repeater.handle()
async def repeater_handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    group = str(event.group_id)
    if group in repeater_control:
        __cache__[group].append(event.message)
        print(__cache__)
        if len(__cache__[group]) == 3:
            __cache__[group].pop(0)
        if len(__cache__[group]) == 2:
            if __cache__[group][0] == __cache__[group][1]:
                await repeater.finish(event.message)

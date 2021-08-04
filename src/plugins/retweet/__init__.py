import nonebot
import httpx
from nonebot import on_command
from nonebot.adapters import Bot, Event
from nonebot.permission import Permission
from nonebot.rule import to_me
from nonebot.typing import T_State

from .config import Config

# Read config from global
global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())

retweet = on_command("天气", rule=to_me(), priority=5)
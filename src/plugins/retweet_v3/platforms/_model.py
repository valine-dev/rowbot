from nonebot.adapters.cqhttp import MessageSegment
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Media:
    '''媒体模型
    Attrs:
    mtype (str): 媒体类型，目前支持 "image" 和 "video"
    url (str): 可直接访问到资源的链接
    '''

    mtype: str
    url: str

    def get_segment(self, type_: str = None):
        '''获取该Media对应的消息片段
            其中 type_ 是 image 类型独有的，详情查阅cqhttp文档
        '''
        seg = {
                "file": self.url,
                "cache": True,
                "proxy": True,
                "timeout": None
            }
        if self.mtype == 'image':
            seg['type'] = type_
        return MessageSegment(self.mtype, seg)


@dataclass
class Work:
    '''表示一篇推文/帖子的类
    Attrs:
    uid (str): work在对应平台的唯一识别码
    author (str): 作者的显示名
    author_index (str): 作者在该平台能被找到的名字
    date (str): work的发布日期
    text (str): 正文内容
    media (list[str]): 附带的一切媒体（图像、视频等等）的Media对象
    url (str): 可访问的源链接
    '''

    uid: str
    author: str
    author_index: str
    date: datetime
    text: str
    url: str
    media: list[Media] = field(default_factory=list)

    def add_media(self, m: Media):
        self.media += m

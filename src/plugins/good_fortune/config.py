from pydantic import BaseSettings


class Config(BaseSettings):

    # 本地代理（仅HTTP）
    use_proxy: bool = True
    proxy_http_url: str = 'http://127.0.0.1:8080/'
    proxy_https_url: str = 'http://127.0.0.1:8081/'

    # 所有可能出现的签语 这里的{e}会被请求的事件替换，{kotoba}会被签语替代, {uid}会被目标用户ID取代
    results: list = [
        ''' {e}的运势：【大吉】

 是大吉哦！完完全全的好运气呢！
 似乎什么事情随便做一下就会获得完全胜利！
 一发入魂、天降大馅饼
 可恶，运气好到令人羡慕……

 {kotoba}''',
        ''' {e}的运势：【中吉】

 非常令人安心的运势呢
 即便不是绝佳好运气也是次佳好运气（？
 说不定十连抽就能获得金色传说，或者在路上捡到十块钱什么的——
 总之就是好运气啦！

 {kotoba}''',
        ''' {e}的运势：【末吉】

 唔？是末吉……
 嘛，就算是末吉也不要灰心丧气啦——！
 你看，这里边不还有个“吉”字吗w

 {kotoba}''',
        ''' {e}的运势：【凶】

 游戏结束了呢w
 是厄运中的厄运，厄神的厄运
 ——但不要难过啦！据说把签绑在御签挂上就可以转运啦哦
 已经帮你绑好了哦！
 所以不用担心啦！

 {kotoba}''',
    ]

    # 特殊运势
    special_results: list = [
        '''{e}的运势:dj㔊jj(*T&_MISSING_g79㔋9_FORTUNE_7f*&(jk
U*HE的签CO㔅
nu㔀ll_FOR㔅T㔇㔈UNE

...

{uid}_ACHIEVEMENT_GET -> HIDDEN_FORTUNE_CORRUPTED
        ''',
        ''' {e}的运势：Niko
 拥有救世主一般的好运，
 如果这样子到了异世界拯救世界，
 最后一定可以功成名就回家的吧？

 真的可以吗？

 【成就获得：隐藏运势-Niko】'''
    ]
    # 是否加入 HITOKOTO 生成的签语
    use_hitokoto: bool = True

    # 特殊签的概率
    special: int = 5

    class Config:
        extra = "ignore"

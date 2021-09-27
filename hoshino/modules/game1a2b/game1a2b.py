import re

from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('1a2b')

start_1a2b = re.compile(r'^1[Aa]2[Bb]$')
guess_1a2b = re.compile(r'^[0-9]{4}')
is_1a2b_start = False
answer = 1234

@sv.on_rex(r'^1[Aa]2[Bb]$|^[0-9]{4}')
async def hello(bot, ev):
    start = start_1a2b.match(ev.message.extract_plain_text())
    guess = guess_1a2b.match(ev.message.extract_plain_text())
    global is_1a2b_start
    if start:
        if is_1a2b_start:
            await bot.send(ev, '1A2B已经开始，请等待游戏结束')
        else:
            
            is_1a2b_start = True
            await bot.send(ev, '1A2B游戏开始啦！发送你要猜的四位数字，开始游戏吧~')
    elif guess:
        if guess == answer:
            await bot.send(ev, '恭喜_____中了正确答案：1234！')
            is_1a2b_start = False
        else:
            await bot.send(ev, '_A_B')

    # if is_1a2b_start:
    #     await bot.send(ev,'echo: 1a2b test')

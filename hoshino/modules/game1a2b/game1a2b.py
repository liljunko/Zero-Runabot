import re
import random

from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('1a2b')

start_1a2b = re.compile(r'^1[Aa]2[Bb]$')
guess_1a2b = re.compile(r'^[0-9]{4}')
is_1a2b_start = False
answer = '5862'

# TODO: answer generator
def ans_gener():
    answer = random.sample(range, 4)
    return answer

# TODO: game judge
def hint(answer, guess):
    correct = sum([answer[i] == guess[i] for i in range(4)])
    misplaced = sum([i in answer for i in guess]) - correct
    if correct == 4:
        return True
    else:
        return correct, misplaced


@sv.on_rex(r'^1[Aa]2[Bb]$|^[0-9][0-9][0-9][0-9]$')
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
        if not is_1a2b_start:
            return
        # TODO: 重复判断
        # if 重复
            # return
        # TODO: game judge
        if guess == answer:
            await bot.send(ev, '恭喜_____中了正确答案：5862！')
            is_1a2b_start = False
        else:
            await bot.send(ev, '_A_B')

    # if is_1a2b_start:
    #     await bot.send(ev,'echo: 1a2b test')

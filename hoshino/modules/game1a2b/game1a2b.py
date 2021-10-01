import re
import random

from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('1a2b')

start_1a2b = re.compile(r'^1[Aa]2[Bb]$')
guess_1a2b = re.compile(r'^[0-9]{4}$')
is_1a2b_start = False
answer = ""
guess_count = 0   # 计数器

def ans_gener():
    ans = ""
    tmp = random.sample(range(10), 4)
    for a in tmp:
        ans += str(a)
    return ans

def have_repeat(guess):
    hash_set = dict()
    # guess_list = list(guess)
    for ch in guess:
        if ch in hash_set:
            return True
        else:
            hash_set[ch] = None
    return False

def judge(answer, guess):
    # answer_list = list(answer)
    # guess_list = list(guess)
    correct = sum([answer[i] == guess[i] for i in range(4)])
    misplaced = sum([i in answer for i in guess]) - correct
    return correct, misplaced


@sv.on_rex(r'^1[Aa]2[Bb]$|^[0-9]{4}$')
async def hello(bot, ev):
    start = start_1a2b.match(ev.message.extract_plain_text())
    guess = guess_1a2b.match(ev.message.extract_plain_text())
    global is_1a2b_start, answer, guess_count
    if start:
        if is_1a2b_start:
            await bot.send(ev, '1A2B已经开始，请等待游戏结束')
            return
        else:
            answer = ans_gener()
            guess_count = 0
            is_1a2b_start = True
            await bot.send(ev, '[CQ:face,id=74]1A2B游戏开始啦！发送你要猜的四位数字，开始游戏吧~')
            return
    elif guess:
        # await bot.send(ev, answer)
        if not is_1a2b_start:
            return
        player_guess = guess.group(0)
        if have_repeat(player_guess):
            return
        correct, misplaced = judge(answer, player_guess)
        if correct == 4:
            is_1a2b_start = False
            hint = '[CQ:face,id=144]恭喜[CQ:at,qq=' + str(ev.user_id) + ']猜中了正确答案：' + answer + '[CQ:face,id=144]'
            await bot.send(ev, hint)
            return
        else:
            guess_count += 1
            hint ='(' + str(guess_count) + ') Guess: '+ player_guess +' —— ' \
                + str(correct) + 'A' + str(misplaced) + 'B'
            await bot.send(ev, hint)
            return
    else:
        return
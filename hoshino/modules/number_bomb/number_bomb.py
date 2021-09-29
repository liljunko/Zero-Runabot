from math import trunc
import re
import random

from pytz import country_names

from hoshino import Service
from hoshino.typing import CQEvent
from hoshino.util import silence

sv = Service('number_bomb')

MAX_PLAYER = 6

# TODO: 全局变量
_is_bomb_start = False
player_list = list()
_current_player = 0
_bomb = 0
_min = 1
_max = 100

# TODO: 游戏初始化
def bomb_init():
    global _is_bomb_start, _current_player
    global _bomb, _min, _max
    ###生成玩家列表###
    is_bomb_start = True
    random.shuffle(player_list)
    _current_player = 0
    ###生成炸弹###
    _bomb = random.randrange(2, 100)
    _min = 1
    _max = 100

    init_hint = '【心跳~禁言数字炸弹】游戏开始\n'\
              + '======================\n'\
              + 'Bomb已生成~【1】—>【100】\n'\
              + '======================\n'\
              + '首先由[CQ:at,qq=' + str(player_list[0]) + ']猜数'

    return init_hint
    
    # order = '[CQ:at,qq=' + str(player_list(0)) + ']'
    # for i in range(1, MAX_PLAYER):
    #     order += '->[CQ:at,qq=' + str(player_list(i)) + ']'
    # return order

# TODO: 游戏重置

# TODO: 答案生成

# TODO: 数字判断
def bomb_bingo(guess):
    if _bomb == int(guess):
        return True
    else:
        return False


# TODO: game logic
@sv.on_fullmatch('.bomb join')
async def bomb_join(bot, ev):
    if _is_bomb_start == True:
        await bot.send(ev, 'bomb已经开始，请等待游戏结束~')
        return
    else:
        if ev.user_id in player_list:
            await bot.send(ev, '请不要重复报名')
            return
        if len(player_list) == MAX_PLAYER:
            await bot.send(ev, '报名失败，玩家已满')
            return
        else:
            # global player_list
            player_list.append(ev.user_id)
            hint = 'Bomb报名成功！\n'\
                 + '============\n'\
                 + ' Player: ['+ str(len(player_list)) + ' / ' + str(MAX_PLAYER) +']'
            await bot.send(ev, hint)
            
@sv.on_fullmatch('.bomb start')
async def bomb_start(bot, ev):
    if _is_bomb_start == True:
        await bot.send(ev, 'Bomb已经开始，请等待游戏结束~')
        return
    if ev.user_id not in player_list:
        await bot.send(ev, '你没有报名，请不要迫害玩家~')
        return
    # if len(player_list) < 2:
    #     await bot.send(ev, 'Bomb开始失败，玩家不足')
    else:
        hint = bomb_init()
        await bot.send(ev, hint)
        await bot.send(ev, str(_bomb))

@sv.on_rex(r'^b[\d]{1,2}$')
async def bomb_guess(bot, ev):
    await bot.send(ev, 'matched guess')
    if _is_bomb_start == False:
        return
    if (ev.user_id not in player_list) or (ev.user.id != player_list[_current_player]):
        await bot.send(ev, '你未参加游戏，或尚未轮到你的回合')
        return
    guess = str(ev.message.extract_plain_text()).lstrip('b')
    if bomb_bingo(guess):
        await bot.send(ev, 'Bingo')
    else:
        await bot.send(ev, 'Update')
        return
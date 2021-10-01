# import re
import random

from hoshino import Service, util
from hoshino.typing import CQEvent

sv = Service('number_bomb')

MAX_PLAYER = 6
MAX_SILENCE_MINUTES = 3

# TODO: 全局变量
_is_bomb_start = False
player_list = list()
_current_player = 0
_min = 1
_max = 100
_bomb = -1
_turn = -1

# TODO: 游戏初始化
def bomb_init():
    global _is_bomb_start, _turn, _current_player
    global _bomb, _min, _max
    _is_bomb_start = True
    ###生成玩家列表###
    random.shuffle(player_list)
    _current_player = 0
    ###生成炸弹###
    _turn = 1
    _bomb = random.randrange(2, 100)
    _min = 1
    _max = 100

    init_hint = '【心跳~禁言数字炸弹】游戏开始\n'\
              + '====================\n'\
              + 'Bomb已生成~【1】—>【100】\n'\
              + '====================\n'\
              + '首先由[CQ:at,qq=' + str(player_list[0]) + ']猜数'

    return init_hint
    # 玩家列表
    # order = '[CQ:at,qq=' + str(player_list(0)) + ']'
    # for i in range(1, MAX_PLAYER):
    #     order += '->[CQ:at,qq=' + str(player_list(i)) + ']'
    # return order

# TODO: 游戏重置
def game_reset():
    global _is_bomb_start, _turn, _current_player
    global _bomb, _min, _max
    _is_bomb_start = False
    ###重置玩家列表###
    player_list.clear()
    _current_player = 0
    ###重置Bomb###
    _turn = -1
    _bomb = -1
    _min = 1
    _max = 100
    


# TODO: 提示更新
def hint_update(guess):
    global _min, _max, _turn, _current_player
    _current_player += 1
    if _current_player == len(player_list):
        _current_player = 0
        _turn += 1
    #小于Bomb
    if guess > _min and guess < _bomb:
        _min = guess
        hint = 'Turn'+ str(_turn) +': \t\tM I S S\n'\
             + '==============\n'\
             + 'Hint: 【'+ str(_min) +'】—>【'+ str(_max) +'】\n'\
             + '==============\n'\
             + '轮到[CQ:at,qq=' + str(player_list[_current_player]) + ']猜数'
        return hint
    #大于Bomb
    if guess > _bomb and guess < _max:
        _max = guess
        hint = 'Turn'+ str(_turn) +': \t\tM I S S\n'\
             + '==============\n'\
             + 'Hint: 【'+ str(_min) +'】—>【'+ str(_max) +'】\n'\
             + '==============\n'\
             + '轮到[CQ:at,qq=' + str(player_list[_current_player]) + ']猜数'
        return hint


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
            hint = ' Bomb报名成功！\n'\
                 + '==========\n'\
                 + '  Player: ['+ str(len(player_list)) + ' / ' + str(MAX_PLAYER) +']'
            await bot.send(ev, hint)

@sv.on_fullmatch('.bomb quit')
async def bomb_quit(bot, ev):
    if ev.user_id in player_list:
        player_list.remove(ev.user_id)
        hint = ' Bomb退出成功！\n'\
             + '==========\n'\
             + ' Player: ['+ str(len(player_list)) + ' / ' + str(MAX_PLAYER) +']'
        await bot.send(ev, hint)
        return
    else:
        await bot.send(ev, '取消报名失败，你没有报名')
        return
            
@sv.on_fullmatch('.bomb start')
async def bomb_start(bot, ev):
    if _is_bomb_start == True:
        await bot.send(ev, 'Bomb已经开始，请等待游戏结束~')
        return
    if ev.user_id not in player_list:
        await bot.send(ev, '你没有报名，请不要迫害玩家~')
        return
    if len(player_list) < 2:
        await bot.send(ev, 'Bomb开始失败，玩家不足')
    else:
        hint = bomb_init()
        await bot.send(ev, hint)
        # await bot.send(ev, str(_bomb))

@sv.on_prefix('b')
async def bomb_guess(bot, ev):
    # await bot.send(ev, 'matched guess')
    if _is_bomb_start == False:
        await bot.send(ev, 'Bomb尚未开始')
        return
    if (ev.user_id not in player_list) or (ev.user_id != player_list[_current_player]):
        await bot.send(ev, '你未参加游戏，或尚未轮到你的回合')
        return
    guess = int(ev.message.extract_plain_text().strip())
    # await bot.send(ev, str(guess))
    if guess <= _min or guess >= _max:
        await bot.send(ev, '数字超出范围，请重新输入~')
    elif guess == _bomb:
        min = 1
        if _turn == 1:
            min = MAX_SILENCE_MINUTES
        bomb_hint = 'Boom————\t游戏结束\n'\
                  + '=================\n'\
                  + 'Bomb—>【'+ str(_bomb) +'】<—Bomb\n'\
                  + '=================\n'\
                  + '[CQ:at,qq='+ str(player_list[_current_player]) +']被禁言'+ str(min) +'分钟'
        game_reset()
        await bot.send(ev, bomb_hint)
        await util.silence(ev, min*60, skip_su=False)
    else:
        hint = hint_update(guess)
        await bot.send(ev, hint)

@sv.on_fullmatch('.bomb reset')
async def bomb_reset(bot, ev):
    game_reset()
    await bot.send(ev, 'Bomb重置完成！')
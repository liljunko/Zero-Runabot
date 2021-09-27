import re

from hoshino import Service
from hoshino.typing import CQEvent

sv = Service('1a2b')

start_1a2b = re.compile(r'^1[Aa]2[Bb]$')
guess_1a2b = re.compile(r'^[0-9]{4}')
is_1a2b_start = False

@sv.on_rex(r'^1[Aa]2[Bb]$|^[0-9]{4}')
async def hello(bot, ev):
    start = start_1a2b.match(ev.message)
    guess = guess_1a2b.match(ev.message)
    if start:
        await bot.send(ev,'match 1a2b')
    if guess:
        await bot.send(ev,'match number')

    # if is_1a2b_start:
    #     await bot.send(ev,'echo: 1a2b test')

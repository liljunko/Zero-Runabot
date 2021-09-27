from hoshino import Service

sv = Service('1a2b')

@sv.on_rex(r'^1[Aa]2[Bb]$')
async def hello(bot, ev):
    await bot.send(ev,'echo: 1a2b test')

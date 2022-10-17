import discord
import os
import json
import logging
from discord import Message, message
from discord.ext import commands
from discord.ui import Button, View
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)
cfx = json.load(open(cwd+'\json\cfx.json', encoding='utf-8'))

token = os.environ["DBOTTOKEN"]
intents = discord.Intents.all()
intents.message_content = True
#у изменения активности есть варианты - streaming, playing, listening, watching, competing
# + есть варианты unknown и custom - первый говорит сам за себя, а как работает второй я пока не понял
activity = discord.Activity(name='голоса в своей голове', type=discord.ActivityType.listening)
Bot = commands.Bot(command_prefix=cfx['prefix'], activity=activity, intents=intents, owner_id=cfx['owner'])
logging.basicConfig(level=logging.DEBUG)

# Проверка базового функционала сообщений
# P.S. я так и не понял почему он копирует все переданное после команды сообщение только если в аргументах функции есть *, arg после контекста
# P.S.S - по поводу контекта - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Context
@Bot.command()
async def tm(ctx, *, arg: str):
    await ctx.send(arg, delete_after=3)

@Bot.command()
async def stats(ctx):
    await ctx.send( f'```diff\n'+
                    f'discord version - {discord.__version__}\n'+
                    f'server count - {len(Bot.guilds)}\n'+
                    f'nmember count - {len(set(Bot.get_all_members()))}'+
                    '```')

@Bot.command()
async def OC(ctx):
    if ctx.message.author.id == cfx['owner']:
        await ctx.send('1')
    else:
        await ctx.send(f'{ctx.message.author.id}\n'+
                       f'{cfx["owner"]}\n{type(cfx["owner"])}')

#TODO - базовый функционал эмодзи + callback на нажатия 
@Bot.command()
async def et(ctx):
    await ctx.send("_")
    emoji = '🤔'
    await ctx.message.add_reaction(emoji)

# Проверка базавого функционала ЛС
@Bot.command()
async def dm(ctx):
    user = Bot.get_user(ctx.author.id)
    await user.send(f'no way!\ndm is working!')

# Проверка базового функционала кнопок через UI дискорда
@Bot.command()
async def test(ctx):
        # callback функционал - в данном виде редактирует сообщение делая его "пустым"
        # сделать его полностью пустым сделав " " нельзя, дискорд будет ругатся, но при желании можно удалить все сообщение
        async def button_callback(interaction):
            await interaction.response.edit_message(content="_", view=None)

        button = Button(label="BTN_TST", style=discord.ButtonStyle.danger, custom_id='button1')
        view = View()
        view.add_item(button)

        await ctx.send(view=view)

        button.callback = button_callback

Bot.run(token)
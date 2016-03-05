import subprocess
import shlex
import os
import threading
from settings import config
from terminalapp import runcmd
import psutil
import telegram

bot = telegram.Bot(token=config['bot_access_token'])

def chdir(chat_id, cmd):
    if len(shlex.split(cmd)) == 1:
        os.chdir(os.path.expanduser('~'))
    else:
        os.chdir(shlex.split(cmd)[1])
    bot.sendMessage(chat_id, os.path.abspath('.'))

def kill_all_children(chat_id, cmd):
    proc_pid = int(shlex.split(cmd)[1])
    proc = psutil.Process(proc_pid)
    for child in proc.children(recursive=True):
        cpid = child.pid
        child.kill()
        bot.sendMessage(chat_id, '%s killed' % cpid)
    proc.kill()
    bot.sendMessage(chat_id, '%s killed' % proc_pid)


functions = {
    'cd': chdir,
    'killchi': kill_all_children
}

def run(chat_id, cmd):
    prog = shlex.split(cmd)[0]
    if prog in functions:
        functions[prog](chat_id, cmd)
    else:
        threading.Thread(target=runcmd, args=(chat_id, cmd)).start()

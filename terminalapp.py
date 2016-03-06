import shlex
import subprocess
import traceback
import sys
import telegram
from settings import config

bot = telegram.Bot(token=config['bot_access_token'])

def tail(out):
    a, b, c = b'', b'', b''
    while True:
        a, b, c = b, c, out.read(4096)
        if len(c) == 0:
            break
    return (a + b + c)[-4096: ]

def runcmd(chat_id, cmd):
    try:
        if ord(cmd[0]) == ord('!'):
            args = ['sh', '-c', cmd[1:]]
        else:
            args = shlex.split(cmd)
        proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, bufsize=3)
        bot.sendMessage(chat_id, cmd + ': ' + str(proc.pid))
        _out = str(tail(proc.stdout), 'utf-8')
        if len(_out) > 0:
            bot.sendMessage(chat_id, _out)
    except Exception as e:
        try:
            exc_info = sys.exc_info()
        finally:
            traceback.print_exception(*exc_info)
            del exc_info
        print(e)
        bot.sendMessage(chat_id, 'ERROR: ' + str(e))

import time
from textwrap import dedent
from settings import config
import telegram
import psutil

bot = telegram.Bot(token=config['bot_access_token'])
def highcpuproc():
    last = time.time()
    while True:
        mcpu = (float('-inf'), None)
        for proc in psutil.process_iter():
            k = proc.cpu_percent(interval=None)
            if k > mcpu[0]:
                mcpu = (k, proc)
        now = time.time()
        if mcpu[0] > 95 and last - now > 60:
            last = now
            for admin in config['admins']:
                bot.sendMessage(config['admins'][admin], dedent("""
                    pid: {}; name: {};
                    consuming up more cpu(>95)
                """.format(mcpu[1].pid, mcpu[1].name)))

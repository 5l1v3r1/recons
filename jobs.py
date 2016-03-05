from apscheduler.schedulers.background import BackgroundScheduler
from settings import config
import telegram
import psutil
from textwrap import dedent
bot = telegram.Bot(token=config['bot_access_token'])

sched = BackgroundScheduler()

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def sizeof_fmt(num, suffix='b'):
    for unit in ['', 'k', 'm', 'g', 't', 'p', 'e', 'z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

@sched.scheduled_job('interval', minutes=1)
def resources():
    cpu1, cpu2 = psutil.cpu_percent(interval=1, percpu=True)
    ram = psutil.virtual_memory()
    msg = dedent("""
        **resources job**
        cpu core 1    : {}
        cpu core 2    : {}
        total ram     : {}
        free ram      : {}
        used ram      : {}
    """.format(cpu1, cpu2, sizeof_fmt(ram.total), sizeof_fmt(ram.free), sizeof_fmt(ram.used)))
    for admin in config['admins']:
        if config['admins'][admin]:
            bot.sendMessage(config['admins'][admin], msg)

sched.configure(job_defaults=job_defaults)

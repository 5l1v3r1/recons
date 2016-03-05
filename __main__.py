import atexit
from jobs import sched
from routing import updater
from settings import config
import threading


print('value1')
updater.start_polling()
print('value2')
threading.Thread(target=sched.start).start()

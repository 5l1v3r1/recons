import atexit
from jobs import sched
from routing import updater
from settings import config
import threading
from triggers import highcpuproc

print('value1')
updater.start_polling()
print('value2')
threading.Thread(target=sched.start).start()
threading.Thread(target=highcpuproc).start()

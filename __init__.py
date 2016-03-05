from jobs import sched
import threading

threading.Thread(thread=sched.start).start()

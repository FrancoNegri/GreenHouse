import queue
import threading
from bot import startBot
from monitor import start
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
monitorQueue = queue.Queue()
botQueue = queue.Queue()
threads = []

#bot
logging.info("Main    : maknig bot")
t = threading.Thread(target=startBot,args=(monitorQueue,botQueue))
logging.info("Main    : running bot")
t.deamon = True
t.start()
logging.info("Main    : wait for the thread to finish")
threads.append(t)

#monitor
logging.info("Main    : maknig bot")
m = threading.Thread(target=start,args=(monitorQueue,botQueue))
logging.info("Main    : running bot")
m.deamon = True
m.start()
logging.info("Main    : wait for the thread to finish")
threads.append(t)

# block until all tasks are done
m.join()
t.join()

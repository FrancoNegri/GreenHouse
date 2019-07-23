import queue
import threading
from bot import startBot
from monitor import start
import logging

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
q = queue.Queue()
threads = []

#bot
logging.info("Main    : maknig bot")
t = threading.Thread(target=startBot,args=(q,))
logging.info("Main    : running bot")
t.start()
logging.info("Main    : wait for the thread to finish")
threads.append(t)

#monitor
logging.info("Main    : maknig bot")
t = threading.Thread(target=start,args=(q,))
logging.info("Main    : running bot")
t.start()
logging.info("Main    : wait for the thread to finish")
threads.append(t)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
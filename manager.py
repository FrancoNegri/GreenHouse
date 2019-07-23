import queue
import threading
from bot import startBot
from monitor import start
import logging
import sqlite3
import time

def insert_data(conn, data):
    sql = ''' INSERT INTO managerStats(bot, monitor) VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def launchThread(name, startBot, monitorQueue, botQueue):
    logging.info("Main    : maknig bot")
    t = threading.Thread(target=startBot,args=(monitorQueue,botQueue))
    logging.info("Main    : running bot")
    t.deamon = True
    t.start()
    return t

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
monitorQueue = queue.Queue()
botQueue = queue.Queue()
bot = launchThread("bot", startBot, monitorQueue, botQueue)
monitor = launchThread("monitor", start, monitorQueue, botQueue)

while True:
    botAlive = bot.isAlive()
    monitorAlive = monitor.isAlive()
    data = [botAlive,monitorAlive]
    conn=sqlite3.connect('/home/pi/sensordata.db')
    insert_data(conn, data)
    conn.commit()
    conn.close()
    if not botAlive:
        bot = launchThread("bot", startBot, monitorQueue, botQueue)
    if not monitorAlive:
        monitor = launchThread("monitor", start, monitorQueue, botQueue)
    time.sleep(secs)

# block until all tasks are done
m.join()
t.join()
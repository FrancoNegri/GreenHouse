import time
import serial
import sqlite3
import datetime
import time
import queue

class ManualMode:
    def putState(self,state):
        self._state = state

    def state(self):
        return self._state

def isDay():
    timestamp = datetime.datetime.now().time() # Throw away the date information
    start = datetime.time(8)
    end = datetime.time(20)
    return start <= timestamp <= end

def reciveData(s1):
    data = ""
    if(s1.inWaiting() > 0):
        timestamp = datetime.datetime.now().time()
        date = datetime.datetime.now().date()
        while True:
            inputValue=s1.read(1)
            #print(inputValue.decode(),end='')
            if inputValue.decode() is '\n':
                break
            data = data + inputValue.decode()
    splittedData = data.split("\t")
    print(splittedData)
    return (int(float(splittedData[1])),int(float(splittedData[0])),int(splittedData[2]) > 90, int(splittedData[3]), int(splittedData[4]), int(splittedData[5]), int(splittedData[6]), int(splittedData[7]))

def insert_data(conn, data):
    sql = ''' INSERT INTO dhtreadings(temperature, humidity,light,tapa, switch1, switch2 , switch3, switch4) VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    return cur.lastrowid

def nextInstructions(s1,monitorQueue,botQueue,manualMode):
    command = None
    try:
        command = monitorQueue.get(timeout=30)
    except queue.Empty:
        pass
    if command:
        print("Command: " + command)
        if command == "manualMode":
            manualMode.putState(True)
            botQueue.put_nowait("Sabruskis modo manual")
        elif command == "automaticMode":
            manualMode.putState(False)
            botQueue.put_nowait("Sabruskis modo automatico")
        elif command == "t" or command == "T" or command == "+" or command == "-" or command == "l" or command == "L":
            s1.write(command.encode())
            botQueue.put_nowait("Sabruskis ejecutando: " + command)
        else:
            botQueue.put_nowait("Comando no valido")
    if not manualMode.state():
        day = isDay()
        light = state("switch2")
        if day and light == 0:
            s1.write('t'.encode())
            time.sleep(1)
            s1.write('+'.encode())
        elif not day and light == 1:
            s1.write('-'.encode())
            time.sleep(1)
            s1.write('T'.encode())
        heatLight = state("switch1")
        temperature = state("temperature")
        if not day:
            if temperature < 20 and heatLight == 0:
                s1.write('L'.encode())
            elif temperature >= 24 and heatLight == 1:
                s1.write('l'.encode())
        else:
            if temperature < 26 and heatLight == 0:
                s1.write('L'.encode())
            elif temperature >= 30 and heatLight == 1:
                s1.write('l'.encode())


def state(id):
    con=sqlite3.connect('/home/pi/sensordata.db')
    cur = con.cursor()
    cur.execute('SELECT '+ id +' FROM dhtreadings ORDER BY id DESC LIMIT 1')
    result = cur.fetchall()
    print(result)
    return result[0][0]

def start(monitorQueue, botQueue):
    manualMode = ManualMode()
    manualMode.putState(False)
    port = "/dev/ttyACM0"
    s1 = serial.Serial(port, 9600)
    s1.flushInput()
    path = '/home/pi/data.csv'
    while True:
        nextInstructions(s1,monitorQueue,botQueue,manualMode)
        if(s1.inWaiting() > 0):
            data = reciveData(s1)
            conn=sqlite3.connect('/home/pi/sensordata.db')
            insert_data(conn, data)
            conn.commit()
            conn.close()
        #time.sleep(30)

if __name__ == "__main__":
    start(queue.Queue(),queue.Queue())

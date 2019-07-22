import time
import serial
import sqlite3

port = "/dev/ttyACM0"

s1 = serial.Serial(port, 9600)
s1.flushInput()

import datetime
import time

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
			if inputValue.decode() is '\n':
				break
			data = data + inputValue.decode()
	splittedData = data.split("\t")
	return (int(float(splittedData[1])),int(float(splittedData[0])),int(splittedData[2]) > 50, int(splittedData[3]), int(splittedData[4]), int(splittedData[5]), int(splittedData[6]), int(splittedData[7]))

def insert_data(conn, data):
	sql = ''' INSERT INTO dhtreadings(temperature, humidity,light,tapa, switch1, switch2 , switch3, switch4) VALUES(?,?,?,?,?,?,?,?) '''
	cur = conn.cursor()
	cur.execute(sql, data)
	return cur.lastrowid

path = '/home/pi/data.csv'
log = open(path,'a+')

prevUpdate = isDay()
if prevUpdate:
	s1.write('+'.encode())
else:
	s1.write('-'.encode())

#reciveData(s1)#flush possible missing data from arduino
while True:
	day = isDay()
	print("ok")
	if day and prevUpdate is not day:
		s1.write('+'.encode())
	elif not day and prevUpdate is day:
		s1.write('-'.encode())
	if(s1.inWaiting() > 0):
		data = reciveData(s1)
		print(data)
		conn=sqlite3.connect('/home/pi/sensordata.db')
		#conn.row_factory = dict_factory
		insert_data(conn, data)
		conn.commit()
		conn.close()
		#print(data)
	prevUpdate = day
	log.flush()
	time.sleep(30)

import numpy as np
import matplotlib.pyplot as plt
import time
import sqlite3
import matplotlib.dates as mdates
from matplotlib.ticker import FormatStrFormatter
from matplotlib.dates import DateFormatter
from matplotlib.ticker import FuncFormatter

def getValues(cur, param, quantity, minutes_between):
	cur.execute("SELECT " + param + " FROM dhtreadings WHERE id % " + minutes_between + " == 0 ORDER BY id DESC LIMIT " + quantity)
	return cur.fetchall()

hours = mdates.HourLocator(interval = 1)

def draw():
	conn=sqlite3.connect('/home/pi/sensordata.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
	#fileHandle = sqlite('/home/pi/data.csv',"r" )
	#lineList = fileHandle.readlines()
	#fileHandle.close()
	cur = conn.cursor()
	tempHist = getValues(cur, "temperature", "150", "10")
	humHist = getValues(cur, "humidity", "150", "10")
	timeHist = getValues(cur, 'created_date as "[timestamp]"', "150", "10")
	light = getValues(cur, "switch1", "150", "10")

	tempHist = list(map(lambda x: x[0],tempHist))
	humHist = list(map(lambda x: x[0],humHist))
	timeHist = list(map(lambda x: x[0],timeHist))
	light = list(map(lambda x: x[0],light))

	tempHist.reverse()
	humHist.reverse()
	timeHist.reverse()

	fig, ax = plt.subplots()
	plt.title('Temperatura: Ultimas 24 horas', fontsize=16)
	plt.xlabel('Hora')
	plt.ylabel('Temperatura')
	plt.plot(timeHist, tempHist)
	#plt.ylim(bottom=0)
	plt.yticks(np.arange(10, 42, 2))
	plt.grid()
	years_fmt = mdates.DateFormatter('%Y')
	myFmt = DateFormatter("%Hhs")
	ax.xaxis.set_major_locator(hours)
	ax.xaxis.set_major_formatter(myFmt)
	ax.yaxis.set_major_formatter(FormatStrFormatter('%.0f Cº'))
	plt.xticks(fontsize=8,rotation=90)
	plt.yticks(fontsize=8)
	#ax.yaxis.set_major_locator(plt.MaxNLocator(5))
	#fig.autofmt_xdate()
	plt.savefig("/home/pi/GreenHouse/static/image.png")
	plt.clf()

	fig, ax = plt.subplots()
	plt.title('Humedad: Ultimas 24 horas', fontsize=16)
	plt.xlabel('Hora')
	plt.ylabel('Humedad')
	plt.plot(timeHist, humHist)
	#plt.ylim(top=100, bottom=0)
	plt.yticks(np.arange(0, 110, 10))
	plt.grid()
	myFmt = DateFormatter("%Hhs")
	ax.xaxis.set_major_locator(hours)
	ax.xaxis.set_major_formatter(myFmt)
	ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0%}'.format(y/100)))
	plt.xticks(fontsize=8,rotation=90)
	plt.yticks(fontsize=8)
	#fig.autofmt_xdate()
	plt.savefig("/home/pi/GreenHouse/static/humedad.png")
	plt.clf()


	fig, ax = plt.subplots()
	plt.title('Calefaccion: Ultimas 24 horas', fontsize=16)
	plt.xlabel('Hora')
	plt.ylabel('Luz')
	plt.plot(timeHist, light)
	#plt.ylim(bottom=0)
	plt.yticks(np.arange(0, 3, 1))
	plt.grid()
	years_fmt = mdates.DateFormatter('%Y')
	myFmt = DateFormatter("%Hhs")
	ax.xaxis.set_major_locator(hours)
	ax.xaxis.set_major_formatter(myFmt)
	plt.xticks(fontsize=8,rotation=90)
	plt.yticks(fontsize=8)
	#ax.yaxis.set_major_locator(plt.MaxNLocator(5))
	#fig.autofmt_xdate()
	plt.savefig("/home/pi/GreenHouse/static/luz.png")
	plt.clf()


	print("end")



if __name__ == "__main__":
	while True:
		draw()
		time.sleep(60*30)

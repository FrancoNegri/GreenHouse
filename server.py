#import drawer
from flask import Flask, render_template
from flask_socketio import SocketIO
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
	con=sqlite3.connect('/home/pi/sensordata.db')
	cur = con.cursor()
	cur.execute("SELECT temperature,humidity,created_date FROM dhtreadings ORDER BY id DESC LIMIT 1")
	result = cur.fetchall()
	print(result)
	return render_template('session.html', temperature=result[0][0], humidity=result[0][1], time=result[0][2])

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0',port=80, debug=False)

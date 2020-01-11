#!/usr/bin/env python3
from flask import Flask, request
import json
import letters
import time
import datetime
from dateutil import parser
from multiprocessing import Process, Value
from ctypes import Structure
from conf import ConfHandler

app = Flask('lampice')

terminator = Value('d', 0)
lights = Process(target=letters.doWork, args=(terminator,))
lights.start()

@app.route('/message/', methods=['GET'])
def get_message():
	ch = ConfHandler.getConfHandler()
	message = ch.getConf()['message']
	return message, 200

@app.route('/message/', methods=['PUT', 'POST'])
def put_message():
	global lights
	ch = ConfHandler.getConfHandler()
	c = ch.getConf()
	c['message'] = str(request.data.decode("utf-8"))
	delay = int(c['start_delay'])
	c['start_time'] = datetime.datetime.fromtimestamp(int(request.headers['timestamp'])/1000) + datetime.timedelta(seconds = delay)
	c['start_time'] = c['start_time'].isoformat()
	ch.putConf(c)
	if lights != None:
		terminator.value = 1
		lights.join()
	terminator.value = 0
	lights = Process(target=letters.doWork, args=(terminator,))
	lights.start()
	return 'OK!', 200

@app.route('/config/', methods=['GET'])
def get_conf():
	ch = ConfHandler.getConfHandler()
	c = ch.getConfRaw()
	return c, 200

@app.route('/config/', methods=['PUT', 'POST'])
def put_conf():
	ch = ConfHandler.getConfHandler()
	ch.putConf(json.loads(request.data.decode("utf-8")))
	return 'OK!', 200

@app.route('/reset/', methods=['GET', 'PUT', 'POST'])
def reset():
	ch = ConfHandler.getConfHandler()
	ch.resetConf()
	return 'OK!', 200

if __name__ == '__main__':
 app.run(host="0.0.0.0", port=5000)

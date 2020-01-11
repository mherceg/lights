PROD = True
if PROD:
	import board
	import neopixel 
from multiprocessing import Value
from conf import ConfHandler
from collections import defaultdict
import datetime
from dateutil import parser
import time
import random

layout = '____Z_YXW_NOP_Q_HGFE__'
colours_orig = {
	'A' : 'FFFF99',
	'B' : '0000FF',
	'C' : 'CC0066',
	'D' : '66FFFF',
	'E' : '0080FF',
	'F' : 'FF7417',
	'G' : 'CC0066',
	'H' : '0080FF',
	'I' : '66FFFF',
	'J' : 'CC0066',
	'K' : '0080FF',
	'L' : '66FFFF',
	'M' : 'FF7417',
	'N' : 'CC0066',
	'O' : 'CC0066',
	'P' : '66FFFF',
	'Q' : 'CC0066',
	'R' : '66FFFF',
	'S' : 'FFFF99',
	'T' : 'FF7417',
	'U' : '0080FF',
	'V' : 'CC0066',
	'W' : '0080FF',
	'X' : 'FF7417',
	'Y' : 'CC0066',
	'Z' : 'CC0066'
}

def get_colour(letter, colours):
	def tuplerise(hash):
		return (int(hash[:2], 16), int(hash[2:4], 16), int(hash[4:], 16))
	if letter in colours:
		return tuplerise(colours[letter])
	else:
		if isinstance(colours, dict):
			return tuplerise(random.choice(list(colours.values())))
		return tuplerise(random.choice(colours))

def find_location(letter):
	ind = None
	for i, l in enumerate(layout):
		if l == letter:
			ind = i
	return ind

def set_letter(pixels, letter, colours):
	c = get_colour(letter, colours)
	ind = find_location(letter)
	if PROD:
		if ind is not None:
			pixels[ind] = c
	else:
		print(letter, ind, c)

def clear_letter(pixels, letter, colours):
	ind = find_location(letter)
	if PROD:
		if ind is not None:
			pixels[ind] = (0,0,0)
	else:
		print(' ', ind, ' ')

def do_next_letter(message, start_time, time_on, time_off, colours, pixels, q):
	message = message + '  '
	tm = start_time
	ind = 0
	if q == None:
		while tm < datetime.datetime.now():
			tm += datetime.timedelta(seconds=time_on)
			tm += datetime.timedelta(seconds=time_off)
			ind += 1
			if ind >= len(message):
				ind = 0
		q = ind
	else:
		if q >= len(message):
			q = 0
		ind = q
	set_letter(pixels, message[ind], colours)
	time.sleep(time_on)
	clear_letter(pixels, message[ind], colours)
	time.sleep(time_off)
	return q + 1


def doWork(end):
	conf = ConfHandler.getConfHandler()
	c = conf.getConf()
	brightness = int(c['brightness'])/100
	if (c['colour_scheme'] == 'original'):
		colours = colours_orig
	else:
		colours = c['colours']
	message = c['message'].upper()
	start_time = parser.parse(c['start_time'])
	time_on = c['time_on']
	time_off = c['time_off']
	random_mode = c['random_mode']
	pixels = None
	if PROD:
		pixels = neopixel.NeoPixel(board.D18, len(layout), brightness=brightness)
	time.sleep(1)
	q = None
	while end.value == 0:
		if random_mode:
			valid = []
			for i in layout:
				if i >= 'A' and i <= 'Z':
					valid.append(i)
			l = random.choice(valid)
			set_letter(pixels, l, colours)
			time.sleep(random.randint(1,3))
			clear_letter(pixels, l, colours)
		else:
			q = do_next_letter(message, start_time, time_on, time_off, colours, pixels, q)
	if PROD:
		pixels.deinit()

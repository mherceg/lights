import json
from ctypes import Structure

CONF_FILE = 'conf.json'

class ConfHandler(Structure):

	singleton = None

	def __init__(self):
		self.CONF_FILE = '/home/pi/conf.json'
		self.CONF_BAK = '/home/pi/conf.bak'
		self.HANDLER = self

	def getConf(self):
		content = ''
		with open(self.CONF_FILE, "r") as f:
			content = f.read()
		return json.loads(content)

	def putConf(self, c):
		with open(self.CONF_FILE, "w") as f:
			f.write(json.dumps(c, sort_keys=True, indent=2))

	def getConfRaw(self):
		content = ''
		with open(self.CONF_FILE, "r") as f:
			content = f.read()
		return str(content)

	def resetConf(self):
		content = ''
		with open(self.CONF_BAK, "r") as f:
			content = json.loads(f.read())
		with open(self.CONF_FILE, "w") as f:
			f.write(json.dumps(content, sort_keys=True, indent=2))

	@staticmethod
	def getConfHandler():
		if ConfHandler.singleton == None:
			ConfHandler.singleton = ConfHandler()
		return ConfHandler.singleton


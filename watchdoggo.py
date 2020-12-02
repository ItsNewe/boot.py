from dbinteraction import dbexec
from datadog import initialize, api, statsd
import datetime

class Doggo:
	def __init__(self):
		self.guildc = None
		self.userc = None
		self.autorolec = None
		self.commandsc = None
		self.datadogOpts= {
				"api_key": dbexec("dsaApiKey", log=True),
				"app_key":dbexec("ddAppKey", log=True),
				"statsd_host":"127.0.0.1",
				"statsd_port":8125
			}
		initialize(**self.datadogOpts)

	def gather(self, gc, uc, arc, cc):
		now = datetime.datetime.now()
		self.guildc, self.userc, self.autorolec, self.commandsc= gc, uc, arc, cc

	def update(self):
		print(self.guildc, self.userc, self.autorolec, self.commandsc)
		dbexec("INSERT INTO stats1 VALUES(DATETIME('now','localtime'),?,?,?,?)", (self.guildc, self.userc, self.autorolec, self.commandsc,), db="stats")
	
	def ddNewCommand():
		statsd.increment("konata_commandsTotal.increment")

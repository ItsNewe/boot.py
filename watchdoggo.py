from dbinteraction import *
import datetime

class Doggo:
    def __init__(self):
        self.guildc = None
        self.userc = None
        self.autorolec = None
        self.commandsc = None

    def gather(self, gc, uc, arc, cc):
        now = datetime.datetime.now()
        self.guildc, self.userc, self.autorolec, self.commandsc= gc, uc, arc, cc

    def update(self):
        print(self.guildc, self.userc, self.autorolec, self.commandsc)
        dbexec("INSERT INTO stats1 VALUES(DATETIME('now','localtime'),?,?,?,?)", (self.guildc, self.userc, self.autorolec, self.commandsc,), db="stats")
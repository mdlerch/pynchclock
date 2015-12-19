import sqlite3
import csv
import os.path
import datetime

def checkfiles(pynchdb):
    if not os.path.isfile(pynchdb):
        conn = sqlite3.connect(pynchdb)
        c = conn.cursor()
        c.execute('''CREATE TABLE clock
                 (job text, hours real, joborder int)''')
        c.execute("INSERT INTO clock VALUES ('MyJob', 0, 1)")
        conn.commit()
        c.execute('''CREATE TABLE timesheet
                 (job text, jobdate datetime, hours real)''')
        writedate = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
        c.execute("INSERT INTO timesheet VALUES ('MyJob', ?, 0)", (writedate, ))
        conn.commit()
        conn.close()


def readClockDB(pynchdb):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()

    clock = {'hours': {}}
    clock['order'] = []
    for row in c.execute('SELECT job, hours FROM clock ORDER BY joborder'):
        jobname, hours = row
        clock['hours'][jobname] = float(hours)
        clock['order'].append(jobname)

    conn.close()

    clock['hours']['None'] = 0.0
    clock['current'] = "None"
    clock['order'].append("None")
    return clock


def updateClockDB(pynchdb, clock, jobname):
    if jobname != "None":
        conn = sqlite3.connect(pynchdb)
        c = conn.cursor()
        c.execute("UPDATE clock SET hours = ? WHERE job = ?",
                  (clock['hours'][jobname], jobname))
        conn.commit()
        conn.close()


def addToClockDB(pynchdb, clock, jobname):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    c.execute("INSERT INTO clock VALUES (?, ?, ?)",
              (jobname, clock['hours'][jobname], 0))
    conn.commit()
    conn.close()
    updateClockOrderDB(pynchdb, clock)


def updateClockOrderDB(pynchdb, clock):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    idx = 0
    for jobname in clock['order']:
        idx += 1
        c.execute('UPDATE clock SET joborder = ? WHERE job = ?', (idx, jobname))
        conn.commit()
    conn.close()


def deleteFromClockDB(pynchdb, jobname):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    c.execute('DELETE FROM clock WHERE job = ?', (jobname, ))
    conn.commit()
    conn.close()


def readTimesheetDB(pynchdb):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    timesheet = {}
    for row in c.execute('SELECT DISTINCT job FROM timesheet'):
        jobname, = row
        timesheet[jobname] = {'date' : [], 'hours' : []}
        for row in c.execute('SELECT jobdate, hours FROM timesheet WHERE job = ?', (jobname, )):
            date, hours = row
            timesheet[jobname]['date'].append(date)
            timesheet[jobname]['hours'].append(hours)
    conn.close()
    return timesheet


def updateTimesheetDB(pynchdb, timesheet, jobname, date):
    idx = timesheet[jobname]['date'].index(date)
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    c.execute('UPDATE timesheet SET hours = ? WHERE job = ? AND jobdate = ?',
              (timesheet[jobname]['hours'][idx], jobname, date))
    conn.commit()
    conn.close()



def addToTimesheetDB(pynchdb, timesheet, jobname, date):
    idx = timesheet[jobname]['date'].index(date)
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    c.execute("INSERT INTO timesheet VALUES (?, ?, ?)",
              (jobname, date, timesheet[jobname]['hours'][idx]))
    conn.commit()
    conn.close()

import datetime
from database import *
from printclock import *
from editclock import *

def is_enter(c):
    return c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n")

def updateTimesheet(timesheet, clock, writedate, pynchdb):
    for j, t in clock['hours'].iteritems():
        if j in timesheet.keys():
            if writedate in timesheet[j]['date']:
                timesheet[j]['hours'][timesheet[j]['date'].index(writedate)] = t
                updateTimesheetDB(pynchdb, j, writedate, t)
            else:
                timesheet[j]['hours'].append(t)
                timesheet[j]['date'].append(writedate)
                addToTimesheetDB(pynchdb, j, writedate, t)
        elif j != 'None':
            timesheet[j]['hours'] = t
            timesheet[j]['date'] = writedate
            addToTimesheetDB(pynchdb, j, writedate, t)

def editTimesheet(timesheet, jobname, date, newhours, pynchdb):
    idx = timesheet[jobname]['date'].index(date)
    timesheet[jobname]['hours'][idx] = newhours
    editTimesheetDB(pynchdb, jobname, date, newhours)

def addToTimesheet(timesheet, jobname, date, hours, pynchdb):
    if not jobname in timesheet.keys():
        timesheet[jobname] = {'date': [], 'hours': []}
    timesheet[jobname]['date'].append(date)
    timesheet[jobname]['hours'].append(hours)
    addToTimesheetDB(pynchdb, jobname, date, hours)

def deleteFromTimesheet(timesheet, jobname, date, pynchdb):
    idx = timesheet[jobname]['date'].index(date)
    timesheet[jobname]['date'].pop(idx)
    timesheet[jobname]['hours'].pop(idx)
    deleteFromTimesheetDB(pynchdb, jobname, date)



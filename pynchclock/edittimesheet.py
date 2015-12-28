import datetime
from database import *
from printobjects import *
from editclock import *

def is_enter(c):
    return c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n")

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



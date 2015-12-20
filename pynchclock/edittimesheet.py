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
    timesheet[jobname]['date'].append(date)
    timesheet[jobname]['hours'].append(hours)
    addToTimesheetDB(pynchdb, jobname, date, hours)

def deleteFromTimesheet(timesheet, jobname, date, pynchdb):
    idx = timesheet[jobname]['date'].index(date)
    timesheet[jobname]['date'].pop(idx)
    timesheet[jobname]['hours'].pop(idx)
    deleteFromTimesheetDB(pynchdb, jobname, date)


def chooseEditDate(timesheet, clock, jobname, stdscr, pynchdb):
    active = -1
    while 1:
        maxy, maxx = stdscr.getmaxyx()
        maxdates = printTimesheet(timesheet, clock, jobname, active, stdscr)
        c = stdscr.getch()

        # note: indexing is backwards for timesheet

        # UP means more older means more negative
        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if -active < maxdates:
                active += -1
        # DOWN means more recent means less negative
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if active < 0:
                active += 1
        elif is_enter(c):
            pauseScreen()
            if -active > 0:
                stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
                newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
                stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
                stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
                newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
                newhours = newHOURS * 3600 + newMINS * 60
                idx = maxdates + active
                date = timesheet[jobname]['date'][idx]
                editTimesheet(timesheet, jobname, date, newhours, pynchdb)
            if active == 0:
                stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
                newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
                stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
                stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
                newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
                newhours = newHOURS * 3600 + newMINS * 60
                editClock(clock, jobname, newhours, pynchdb)
            restartScreen()
        elif c == ord('A'):
            pauseScreen()
            stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
            newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
            newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            newhours = newHOURS * 3600 + newMINS * 60
            stdscr.addstr(maxy - 1, 0, "New year (YYYY): ")
            newYEAR = int(stdscr.getstr(maxy - 1, 17, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            stdscr.addstr(maxy - 1, 0, "New month: ")
            newMONTH = int(stdscr.getstr(maxy - 1, 11, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            stdscr.addstr(maxy - 1, 0, "New day: ")
            newDAY = int(stdscr.getstr(maxy - 1, 9, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            newdate = "{0:02}-{1:02}-{2:02}".format(newYEAR, newMONTH, newDAY)
            addToTimesheet(timesheet, jobname, newdate, newhours, pynchdb)
            sortTimesheet(timesheet, jobname)
            restartScreen()

        elif c == ord('D'):
            if active != 0:
                idx = maxdates + active
                date = timesheet[jobname]['date'][idx]
                deleteFromTimesheet(timesheet, jobname, date, pynchdb)
                active += 1


        elif c == ord('Q'):
            break


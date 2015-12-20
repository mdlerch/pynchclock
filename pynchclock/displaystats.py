import math
import curses
import datetime
from windowcheck import *

def displayStats(timesheet, clock, jobname, stdscr):
    stdscr.clear()
    ndates = len(timesheet[jobname]['date'])

    maxy, maxx = stdscr.getmaxyx()

    if checkWindowSize(stdscr, 10, 5):
        return

    if ndates > maxy - 2:
        maxdates = maxy - 2
    else:
        maxdates = ndates

    maxtime = max(timesheet[jobname]['hours'])
    maxtime = max(maxtime, clock['hours'][jobname])
    # alltimes.append(clock['hours'][jobname])

    scale = (maxx - 2.0) / maxtime

    # plot historic hours
    for i in range(-maxdates, 0):
        chars = int(round(timesheet[jobname]['hours'][i] * scale)) - 11
        plotstring = "{0} ".format(timesheet[jobname]['date'][i]) + "=" * chars
        stdscr.addstr(i + maxdates, 0, plotstring)

    # print current hours
    chars = int(round(clock['hours'][jobname] * scale)) - 11
    today = datetime.datetime.now()
    todaydate = today.strftime("%Y-%m-%d")
    plotstring = "{0} ".format(todaydate) + "=" * chars
    stdscr.addstr(maxdates, 0, plotstring)

    c = stdscr.getch()

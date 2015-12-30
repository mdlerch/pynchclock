import math
import curses
import datetime
from windowcheck import *

def displayStats(timesheet, clock, jobname, stdscr):
    stdscr.clear()
    ndates = len(timesheet[jobname]['date'])

    maxy, maxx = stdscr.getmaxyx()

    stdscr.addstr(0, 0, "Stats for: " + jobname)

    if checkWindowSize(stdscr, 10, 5):
        return

    if ndates > maxy - 2:
        maxdates = maxy - 2
    else:
        maxdates = ndates

    maxtime = max(timesheet[jobname]['hours'])
    maxtime = max(maxtime, clock['hours'][jobname])

    # if no jobs longer than 1 minute, set maxtime to 1 minute
    if maxtime < 60:
        maxtime = 60

    # subtract 14 for room for date
    scale = (maxx - 14.0) / maxtime

    # print current hours
    # subtract 11 for date info
    nplot = int(round(clock['hours'][jobname] * scale))
    today = datetime.datetime.now()
    todaydate = today.strftime("%Y-%m-%d")
    plotstring = "({0}) ".format(todaydate) + "=" * nplot
    stdscr.addstr(1, 0, plotstring)

    # plot historic hours
    for i in range(0, maxdates):
        jobhours = timesheet[jobname]['hours'][-(i + 1)]
        jobdate = timesheet[jobname]['date'][-(i + 1)]
        nplot = int(round(jobhours * scale))
        plotstring = " {0}  ".format(jobdate) + "=" * nplot
        stdscr.addstr(i + 2, 0, plotstring)


    c = stdscr.getch()

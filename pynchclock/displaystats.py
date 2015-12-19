import math
import curses
import datetime
from windowcheck import *

def displayStats(timesheet, clock, job, stdscr):
    stdscr.clear()
    ndates = len(timesheet[job]['date'])

    maxy, maxx = stdscr.getmaxyx()

    examplestring = "{0}: {1:02.0f}:{2:02.0f}".format("1999-12-31", 10, 10)

    if checkWindowSize(stdscr, len(examplestring), 5):
        return

    if ndates > maxy - 2:
        maxdates = maxy - 2
    else:
        maxdates = ndates

    # print historic hours
    for i in range(-maxdates, 0):
        t = timesheet[job]['hours'][i]
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        statstring = "{0}: {1:02.0f}:{2:02.0f}".format(timesheet[job]['date'][i],
                                                       math.floor(h), m)
        stdscr.addstr(i + maxdates, 0, statstring)

    # print current hours
    today = datetime.datetime.now()
    todaydate = today.strftime("%Y-%m-%d")
    t = clock['hours'][job]
    h = t / 3600.0
    m = (h - math.floor(h)) * 60
    statstring = "{0}: {1:02.0f}:{2:02.0f}".format(todaydate, math.floor(h), m)
    stdscr.addstr(maxdates, 0, statstring)

    c = stdscr.getch()

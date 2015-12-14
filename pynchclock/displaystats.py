import math
import curses
import datetime

def displayStats(allhours, clock, job, stdscr):
    stdscr.clear()
    ndates = len(allhours['dates'])

    maxy, maxx = stdscr.getmaxyx()

    if ndates > maxy - 2:
        maxdates = maxy - 2
    else:
        maxdates = ndates

    for i in range(-maxdates, 0):
        t = allhours['allhours'][job][i]
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        statstring = "{0}: {1:02.0f}:{2:02.0f}".format(allhours['dates'][i],
                                                       math.floor(h), m)
        stdscr.addstr(i + maxdates, 0, statstring)

    today = datetime.datetime.now()
    todaydate = today.strftime("%Y-%m-%d")
    t = clock['hours'][job]
    h = t / 3600.0
    m = (h - math.floor(h)) * 60
    statstring = "{0}: {1:02.0f}:{2:02.0f}".format(todaydate, math.floor(h), m)
    stdscr.addstr(maxdates, 0, statstring)

    c = stdscr.getch()

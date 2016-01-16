import math
import curses
import datetime
from windowcheck import *

def displayStats(timesheet, clock, jobname, stdscr):

    selected = 0

    first = 1
    last = 1

    ndates = len(timesheet[jobname]['date'])

    maxy, maxx = stdscr.getmaxyx()


    if checkWindowSize(stdscr, 10, 5):
        return

    while 1:

        if ndates > maxy - 2:
            last = (first - 1) + (maxy - 2)
        else:
            first = 1
            last = ndates
        if first != last:
            if first == 1:
                maxtime = max(timesheet[jobname]['hours'][-last:])
            else:
                maxtime = max(timesheet[jobname]['hours'][-last:-(first - 1)])
        else:
            maxtime = timesheet[jobname]['hours'][0]
        maxtime = max(maxtime, clock['hours'][jobname])
        # if no jobs longer than 1 minute, set maxtime to 1 minute
        if maxtime < 60:
            maxtime = 60

        # subtract 14 for room for date
        scale = (maxx - 14.0) / maxtime

        h = math.floor(maxtime / 3600)
        m = math.floor((maxtime - h * 3600) / 60)

        maxtimestr = "{0:02.0f}:{1:02.0f}".format(h, m)
        stdscr.addstr(0, 0, jobname + " max = " + maxtimestr)

        # print current hours
        # subtract 11 for date info
        nplot = int(round(clock['hours'][jobname] * scale))
        nblank = max(maxx - nplot - 14, 0)
        today = datetime.datetime.now()
        todaydate = today.strftime("%Y-%m-%d")
        plotstring = "({0}) ".format(todaydate) + "=" * nplot + " " * nblank
        if selected == 0:
            stdscr.addstr(1, 0, plotstring, curses.A_REVERSE)
        else:
            stdscr.addstr(1, 0, plotstring)


        # plot historic hours
        for i in range(first, last + 1):
            row = i - first + 2
            jobhours = timesheet[jobname]['hours'][-i]
            jobdate = timesheet[jobname]['date'][-i]
            nplot = int(round(jobhours * scale))
            nblank = max(maxx - nplot - 14, 0)
            plotstring = " {0}  ".format(jobdate) + "=" * nplot + " " * nblank
            if i == selected:
                stdscr.addstr(row, 0, plotstring, curses.A_REVERSE)
            else:
                stdscr.addstr(row, 0, plotstring)

        c = stdscr.getch()

        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if selected > 0:
                selected += -1
            # if selected is less than first and first is the beginning
            if selected < first and first > 1:
                first += -1
        # DOWN means more recent means less negative
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if selected < ndates:
                selected += 1
            # if selected is greater than last shift
            if selected > last:
                first += 1

        if c == ord('Q'):
            break

        stdscr.refresh()

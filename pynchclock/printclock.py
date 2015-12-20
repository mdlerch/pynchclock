import math
import curses
import datetime
from windowcheck import *


def pauseScreen():
    curses.echo()
    curses.curs_set(1)


def restartScreen():
    # stdscr.nodelay(1)
    curses.noecho()
    curses.curs_set(0)


def printClock(clock, stdscr, active):
    stdscr.clear()
    job_name_length = []
    for job in clock['order']:
        job_name_length.append(len(job))

    spacing = max(job_name_length)
    shift = 3

    maxy, maxx = stdscr.getmaxyx()

    if checkWindowSize(stdscr, spacing + shift + 8, len(clock['order']) + 1):
        return

    i = 0
    for job in clock['order']:

        t = clock['hours'][job]
        h = t / 3600.0
        m = (h - math.floor(h)) * 60

        if i == 9:
            shift = shift - 1

        jobname = job.ljust(spacing + shift, '.')

        if job != "None":
            jobstring = "{3}. {0}{1:02.0f}:{2:02.0f}".format(jobname, math.floor(h), m, i+1)
        else:
            jobstring = "{1}. {0}".format(job, i+1)

        if clock['order'][i] == active:
            stdscr.addstr(i, 0, jobstring, curses.A_REVERSE)
        elif clock['order'][i] == clock['current']:
            stdscr.addstr(i, 0, jobstring, curses.color_pair(1))
        else:
            stdscr.addstr(i, 0, jobstring)

        i += 1

    stdscr.refresh()

def printTimesheet(timesheet, clock, jobname, active, stdscr):
    stdscr.clear()

    maxdates = 0

    if jobname in timesheet.keys():
        ndates = len(timesheet[jobname]['date'])

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
            t = timesheet[jobname]['hours'][i]
            h = t / 3600.0
            m = (h - math.floor(h)) * 60
            statstring = "{0}: {1:02.0f}:{2:02.0f}".format(timesheet[jobname]['date'][i],
                                                           math.floor(h), m)
            if i == active:
                stdscr.addstr(i + maxdates, 0, statstring, curses.A_REVERSE)
            else:
                stdscr.addstr(i + maxdates, 0, statstring)

    # print current hours
    today = datetime.datetime.now()
    todaydate = today.strftime("%Y-%m-%d")
    t = clock['hours'][jobname]
    h = t / 3600.0
    m = (h - math.floor(h)) * 60
    statstring = "{0}: {1:02.0f}:{2:02.0f}".format(todaydate, math.floor(h), m)
    if active == 0:
        stdscr.addstr(maxdates, 0, statstring, curses.A_REVERSE)
    else:
        stdscr.addstr(maxdates, 0, statstring)

    stdscr.refresh()

    return maxdates


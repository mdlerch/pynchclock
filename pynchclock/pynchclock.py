import time
import os.path
import csv
import math
import curses
import datetime
import os.path
import clioptions
from timesheet import *
from displaystats import displayStats

def is_enter(c):
    return c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n")

def printHours(clock, stdscr, active):
    stdscr.clear()
    job_name_length = []
    for job in clock['order']:
        job_name_length.append(len(job))

    spacing = max(job_name_length)
    shift = 3

    maxy, maxx = stdscr.getmaxyx()

    if maxy < 4 or maxx < 9:
        stdscr.addstr(0, 0, ".")
        stdscr.refresh()
        return

    if maxy < len(clock['order']) + 1 or maxx < (spacing + shift + 8):
        stdscr.addstr(0, 0, "Window")
        stdscr.addstr(1, 0, "too small")
        stdscr.refresh()
        return

    i = 0
    for job in clock['order']:

        t = clock['timesheet'][job]
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


def pauseScreen():
    curses.echo()
    curses.curs_set(1)


def restartScreen():
    # stdscr.nodelay(1)
    curses.noecho()
    curses.curs_set(0)


def addJob(clock, stdscr, active):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "New job: ")
    newjob = stdscr.getstr(maxy - 1, 9, 30)
    clock['timesheet'][newjob] = 0.0
    idx = clock['order'].index(active)
    clock['order'].insert(idx, newjob)


def deleteJob(clock, stdscr, active):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "Are you sure you wish to delete " + active + " [y/n]? ")
    c = stdscr.getch(maxy - 1, 50)
    if c == ord('y'):
        if clock['current'] == active:
            clock['current'] = "None"
        clock['timesheet'].pop(active)
        clock['order'].remove(active)

def checkfiles(jobsfile):
    if not os.path.isfile(jobsfile):
        clock = {'order': ['MyJob', 'None'],
                 'timesheet': {'MyJob': 0, 'None': 0},
                 'current': "None"}
        writeJobs("jobsfile.csv", clock)


def readJobs(jobsfile):
    if not os.path.isfile(jobsfile):
        clock = {'order': ['MyJob', 'None'],
                 'timesheet': {'MyJob': 0, 'None': 0},
                 'current': "None"}
        return clock

    with open(jobsfile) as jobs:
        jobs_reader = csv.reader(jobs)

        clock = {'timesheet': {}}
        clock['order'] = []

        for row in jobs_reader:
            (clock['timesheet'])[row[0]] = float(row[1])
            clock['order'].append(row[0])

        clock['timesheet']['None'] = 0.0
        clock['current'] = "None"
        clock['order'].append("None")

    return clock


def writeJobs(jfile, clock):
    with open(jfile, "wb") as jobs_file:
        jobs_writer = csv.writer(jobs_file)

        for job in clock['order']:
            if job != "None":
                jobtime = clock['timesheet'][job]
                jobs_writer.writerow([job, jobtime])


def updateTimes(clock, start):
    if clock['current'] != "None":
        clock['timesheet'][clock['current']] += time.time() - start
    return time.time()


def resetJobs(clock):
    for j, t in clock['timesheet'].iteritems():
        clock['timesheet'][j] = 0.0


def eventLoop(clock, stdscr, jobsfile, savefile):
    start = None
    active = clock['current']
    message = None
    icon_shift = 1
    allhours = readTimesheet(savefile)

    while 1:
        maxy, maxx = stdscr.getmaxyx()

        printHours(clock, stdscr, active)

        if message:
            stdscr.addstr(maxy - 1, 0, message)
            icon_shift = 2

        if clock['current'] == "None":
            stdscr.addstr(maxy - icon_shift, 0, "||")
        else:
            stdscr.addstr(maxy - icon_shift, 0, "> " + clock['current'])

        message = None
        icon_shift = 1


        i = clock['order'].index(active)
        njobs = len(clock['timesheet'].keys())
        c = stdscr.getch()

        # with nodelay, getch returns curses.ERR
        if c != curses.ERR:

            # Moving up or down
            if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
                if clock['order'].index(active) > 0:
                    i = i - 1
                    active = clock['order'][i]
            elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
                if clock['order'].index(active) < njobs - 1:
                    i = i + 1
                    active = clock['order'][i]

            # Selecting a job
            elif is_enter(c):
                start = updateTimes(clock, start)
                writeJobs(jobsfile, clock)
                clock['current'] = active

            # Pause
            elif c == ord('p'):
                start = updateTimes(clock, start)
                active = "None"
                clock['current'] = active
                writeJobs(jobsfile, clock)

            # Add a new job
            elif c == ord('A'):
                start = updateTimes(clock, start)
                clock['current'] = "None"
                pauseScreen()
                addJob(clock, stdscr, active)
                writeJobs(jobsfile, clock)
                restartScreen()

            # Delete a job
            elif c == ord('D'):
                pauseScreen()
                if active == "None":
                    message = "Cannot delete `None`"
                else:
                    deleteJob(clock, stdscr, active)
                active = "None"
                writeJobs(jobsfile, clock)
                restartScreen()

            # Show job stats
            elif c == ord('V'):
                if active != "None":
                    pauseScreen()
                    start = updateTimes(clock, start)
                    if active in allhours['allhours']:
                        displayStats(allhours, clock, active, stdscr)
                    else:
                        message = "No stats on " + active
                    restartScreen()
                    start = updateTimes(clock, start)
                    writeJobs(jobsfile, clock)

            # Update jobs list
            elif c == ord('U'):
                pauseScreen()
                start = updateTimes(clock, start)
                writeJobs(jobsfile, clock)
                message = "Updated " + jobsfile
                restartScreen()
                clock['current'] = "None"
                active = "None"


            # Save timesheet
            elif c == ord('S'):
                pauseScreen()
                start = updateTimes(clock, start)
                writetime = datetime.datetime.now()
                writetime = writetime - datetime.timedelta(days = 1)
                allhours = writeTimesheet(savefile, clock, writetime, allhours)
                clock['current'] = "None"
                active = "None"
                message = "Timesheet appended to " + savefile
                restartScreen()

            # Reset all jobs to 0.0 hours
            elif c == ord('R'):
                pauseScreen()
                printHours(clock, stdscr, active)
                stdscr.addstr(maxy-1, 0, "Are you sure you wish to reset [y/n]? ")
                c = stdscr.getch(maxy-1, 38)
                if c == ord('y'):
                    resetJobs(clock)
                restartScreen()

            # Quit the program
            elif c == ord('Q'):
                start = updateTimes(clock, start)
                writeJobs(jobsfile, clock)
                curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
                exit()







def main():
    options = clioptions.parseArgs()

    jobsfile = options['jobsfile']
    savefile = options['savefile']

    checkfiles(jobsfile)

    clock = readJobs(jobsfile)

    # initialize curses
    stdscr = curses.initscr()
    stdscr.keypad(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.nodelay(0)

    restartScreen()

    # First job is none
    clock['current'] = "None"

    eventLoop(clock, stdscr, jobsfile, savefile)

import time
import csv
import math
import curses

# change how things are stored:
# one time called clock?
# dictionary
# current: string key of current job or integer index of current job?
# timesheet: dictionary of job names and times

def printHours(clock, stdscr, active):
    i = 0
    for k,t in clock['timesheet'].iteritems():
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        jobstring = "{3}.  {0}: {1:.0f} hours, {2:.0f} minutes".format(k, math.floor(h), m, i+1)
        if i == active:
            stdscr.addstr(i, 0, jobstring, curses.A_REVERSE)
        elif i == clock['cur_job']:
            stdscr.addstr(i, 0, jobstring, curses.color_pair(1))
        else:
            stdscr.addstr(i, 0, jobstring)
        i += 1
    jobstring = "{0}.  None".format(i+1)
    if i == active:
        stdscr.addstr(i, 0, jobstring, curses.A_REVERSE)
    elif i == clock['cur_job']:
        stdscr.addstr(i, 0, jobstring, curses.color_pair(1))
    else:
        stdscr.addstr(i, 0, jobstring)
    stdscr.refresh()

def readJobs(file):
    with open(file) as jobs_file:
        jobs_reader = csv.reader(jobs_file)
        clock = { 'timesheet':{} }
        for row in jobs_reader:
            (clock['timesheet'])[row[0]] = float(row[1])
        njobs = len(clock['timesheet'].keys())
        clock['current'] = njobs
        return clock

def writeJobs(file, clock):
    with open(file, "wb") as jobs_file:
        jobs_writer = csv.writer(jobs_file)
        for key, val in clock['timesheet'].items():
            jobs_writer.writerow([key, val])

def updateTimes(clock, start):
    if clock['cur_job'] != njobs:
        job = clock['timesheet'].keys()[clock['cur_job']]
        clock['timesheet'][job] += time.time() - start


def selectJob(clock, stdscr, jobfile, start):
    active = clock['cur_job']
    while(1):
        printHours(clock, stdscr, active)
        njobs = len(clock['timesheet'].keys())
        c = stdscr.getch()

        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if active > 0:
                active = active - 1
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if active < njobs:
                active = active + 1
        elif c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n"):
            updateTimes(clock, start)
            break
        elif c == ord('p'):
            updateTimes(clock, start)
            active = njobs
            break
        elif c == ord('q'):
            updateTimes(clock, start)
            writeJobs(jobfile, clock)
            curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
            exit()
        elif c == ord('a'):
            maxy, maxx = stdscr.getmaxyx()
            stdscr.addstr(maxy-1, 0, "New job: ")
            curses.echo()
            curses.curs_set(1)
            newjob = stdscr.getstr(maxy-1, 10, 30)
            clock['timesheet'][newjob] = 0.0
            curses.noecho()
            curses.curs_set(0)
            stdscr.clear()
        elif c == ord('d'):
            maxy, maxx = stdscr.getmaxyx()
            stdscr.addstr(maxy-1, 0, "Are you sure you wish to delete[y/n]? ")
            curses.echo()
            curses.curs_set(1)
            c = stdscr.getch(maxy-1, 36)
            if c == ord('y'):
                clock['timesheet'].pop(clock['timesheet'].keys()[active])
            curses.noecho()
            curses.curs_set(0)
            stdscr.clear()

    clock['cur_job'] = active

jobfile = "/home/mike/.config/pynchclock/jobs.csv"
clock = readJobs(jobfile)

# initialize curses
stdscr = curses.initscr(); stdscr.keypad(1); curses.start_color()
stdscr.refresh(); curses.noecho(); curses.curs_set(0)
winy, winx = stdscr.getmaxyx()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

jobs = clock['timesheet'].keys()
njobs = len(jobs)
clock['cur_job'] = njobs

selectJob(clock, stdscr, jobfile, time.time())

while (1):
    start = time.time()

    selectJob(clock, stdscr, jobfile, start)

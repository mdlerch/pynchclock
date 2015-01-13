import time
import csv
import math
import curses

def printHours(hours, stdscr, cur_job, active):
    i = 0
    for k,t in hours.iteritems():
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        jobstring = "{3}.  {0}: {1:.0f} hours, {2:.2f} minutes".format(k, math.floor(h), m, i+1)
        if i == active:
            stdscr.addstr(i, 0, jobstring, curses.A_REVERSE)
        elif i == cur_job:
            stdscr.addstr(i, 0, jobstring, curses.color_pair(1))
        else:
            stdscr.addstr(i, 0, jobstring)
        i += 1
    jobstring = "{0}.  None".format(i+1)
    if i == active:
        stdscr.addstr(i, 0, jobstring, curses.A_REVERSE)
    elif i == cur_job:
        stdscr.addstr(i, 0, jobstring, curses.color_pair(1))
    else:
        stdscr.addstr(i, 0, jobstring)
    stdscr.refresh()

def readJobs(file):
    with open(file) as jobs_file:
        jobs_reader = csv.reader(jobs_file)
        hours = {}
        for row in jobs_reader:
            hours[row[0]] = float(row[1])
        return hours

def writeJobs(file, hours):
    with open(file, "wb") as jobs_file:
        jobs_writer = csv.writer(jobs_file)
        for key, val in hours.items():
            jobs_writer.writerow([key, val])

def selectJob(hours, stdscr, njobs, cur_job, jobfile):
    active = cur_job
    while(1):
        printHours(hours, stdscr, cur_job, active)
        c = stdscr.getch()
        if c == ord('q'):
            writeJobs(jobfile, hours)
            curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
            exit()
        elif c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if active > 0:
                active = active - 1
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if active < njobs:
                active = active + 1
        elif c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n"):
            break
    return active

jobfile = "/home/mike/.config/pynchclock/jobs.csv"
hours = readJobs(jobfile)

# initialize curses
stdscr = curses.initscr(); stdscr.keypad(1); curses.start_color()
stdscr.refresh(); curses.noecho();
winy, winx = stdscr.getmaxyx()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

jobs = hours.keys()
njobs = len(jobs)
cur_job = njobs

cur_job = selectJob(hours, stdscr, njobs, cur_job, jobfile)

while (1):
    start = time.time()

    next_job = selectJob(hours, stdscr, njobs, cur_job, jobfile)
    if cur_job != njobs:
        hours[jobs[cur_job]] += time.time() - start
    cur_job = next_job

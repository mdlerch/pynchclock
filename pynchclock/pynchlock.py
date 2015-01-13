import time
import csv
import math
import curses

def printHours(hours, stdscr, active):
    i = 1
    for k,t in hours.iteritems():
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        jobstring = "{3}.  {0}: {1:.0f} hours, {2:.2f} minutes".format(k, math.floor(h), m, i)
        if i == active:
            stdscr.addstr(i - 1, 0, jobstring, curses.A_REVERSE)
        else:
            stdscr.addstr(i - 1, 0, jobstring)
        i += 1
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

jobfile = "/home/mike/.config/pynchclock/jobs.csv"
hours = readJobs(jobfile)

stdscr = curses.initscr()
curses.start_color()
stdscr.refresh()
curses.noecho()

winy, winx = stdscr.getmaxyx()

printHours(hours, stdscr, 0)

jobs = hours.keys()

stdscr.addstr(winy - 1, 0, "Pick a job (q to quit): ")
cur_job_i = stdscr.getch()
next_job_i = cur_job_i

if cur_job_i == ord('q'):
    exit()

cur_job = jobs[int(chr(cur_job_i)) - 1]

while (cur_job_i != ord('q')):
    start = time.time()
    printHours(hours, stdscr, int(chr(next_job_i)))

    stdscr.addstr(winy - 1, 0, "Pick a job (q to quit): ")
    next_job_i = stdscr.getch()
    hours[cur_job] += time.time() - start

    if next_job_i == ord('q'):
        writeJobs(jobfile, hours)
        exit()

    next_job = jobs[int(chr(next_job_i)) - 1]
    cur_job = next_job

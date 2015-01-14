import time
import csv
import math
import curses

def printHours(clock, stdscr, active):
    i = 0
    for job in clock['order']:
        t = clock['timesheet'][job]
        h = t / 3600.0
        m = (h - math.floor(h)) * 60

        if job != "None":
            jobstring = "{3}. {0}: {1:.0f} hours, {2:.0f} minutes".format(job, math.floor(h), m, i+1)
        else:
            jobstring = "{1}. {0}".format(job, i+1)

        if clock['order'][i] == active:
            stdscr.addstr(i, 0, jobstring, curses.A_REVERSE)
        elif clock['order'][i] == clock['cur_job']:
            stdscr.addstr(i, 0, jobstring, curses.color_pair(1))
        else:
            stdscr.addstr(i, 0, jobstring)
        i += 1
    stdscr.refresh()

def readJobs(file):
    with open(file) as jobs_file:
        jobs_reader = csv.reader(jobs_file)
        clock = { 'timesheet':{} }
        clock['order'] = []
        for row in jobs_reader:
            (clock['timesheet'])[row[0]] = float(row[1])
            clock['order'].append(row[0])
        clock['timesheet']['None'] = 0.0
        clock['cur_job'] = "None"
        clock['order'].append("None")
        return clock

def writeJobs(file, clock):
    with open(file, "wb") as jobs_file:
        jobs_writer = csv.writer(jobs_file)
        for job in clock['order']:
            if job != "None":
                time = clock['timesheet'][job]
                jobs_writer.writerow([job, time])

def updateTimes(clock, start):
    if clock['cur_job'] != "None":
        clock['timesheet'][clock['cur_job']] += time.time() - start


def eventLoop(clock, stdscr, jobfile):
    start = None
    active = clock['cur_job']
    while(1):
        i = clock['order'].index(active)
        printHours(clock, stdscr, active)
        njobs = len(clock['timesheet'].keys())
        c = stdscr.getch()

        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if clock['order'].index(active) > 0:
                i = i - 1
                active = clock['order'][i]
            stdscr.clear()
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if clock['order'].index(active) < njobs - 1:
                i = i + 1
                active = clock['order'][i]
            stdscr.clear()
        elif c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n"):
            updateTimes(clock, start)
            clock['cur_job'] = active
            start = time.time()
            stdscr.clear()
        elif c == ord('p'):
            updateTimes(clock, start)
            active = "None"
            clock['cur_job'] = active
            stdscr.clear()
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
            newjob = stdscr.getstr(maxy-1, 9, 30)
            clock['timesheet'][newjob] = 0.0
            clock['order'].remove("None")
            clock['order'].append(newjob)
            clock['order'].append("None")
            curses.noecho()
            curses.curs_set(0)
            stdscr.clear()
            active = newjob
        elif c == ord('d'):
            maxy, maxx = stdscr.getmaxyx()
            if active == "None":
                stdscr.addstr(maxy-1, 0, "Cannot delete None")

            stdscr.addstr(maxy-1, 0, "Are you sure you wish to delete[y/n]? ")
            curses.echo()
            curses.curs_set(1)
            c = stdscr.getch(maxy-1, 38)
            if c == ord('y'):
                clock['timesheet'].pop(active)
                clock['order'].remove(active)
            curses.noecho()
            curses.curs_set(0)
            stdscr.clear()
            active = clock['order'][i]


def main():
    jobfile = "/home/mike/.config/pynchclock/jobs.csv"
    clock = readJobs(jobfile)

    # initialize curses
    stdscr = curses.initscr(); stdscr.keypad(1); curses.start_color()
    stdscr.refresh(); curses.noecho(); curses.curs_set(0)
    winy, winx = stdscr.getmaxyx()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    clock['cur_job'] = "None"

    eventLoop(clock, stdscr, jobfile)

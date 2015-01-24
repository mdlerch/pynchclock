import time
import csv
import math
import curses
import datetime
import configreader
import clioptions

def is_enter(c):
    return c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n")

def printHours(clock, stdscr, active):
    stdscr.clear()
    job_name_length = []
    for job in clock['order']:
        job_name_length.append(len(job))
    spacing = max(job_name_length)

    i = 0
    for job in clock['order']:

        t = clock['timesheet'][job]
        h = t / 3600.0
        m = (h - math.floor(h)) * 60

        shift = 3
        if i+1 > 9:
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


def newJob(clock, stdscr):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "New job: ")
    newjob = stdscr.getstr(maxy - 1, 9, 30)
    clock['timesheet'][newjob] = 0.0
    clock['order'].remove("None")
    clock['order'].append(newjob)
    clock['order'].append("None")


def deleteJob(clock, stdscr, active):
    maxy, maxx = stdscr.getmaxyx()
    if active == "None":
        stdscr.addstr(maxy - 1, 0, "Cannot delete None")
    stdscr.addstr(maxy - 1, 0, "Are you sure you wish to delete[y/n]? ")
    c = stdscr.getch(maxy - 1, 38)
    if c == ord('y'):
        clock['timesheet'].pop(active)
        clock['order'].remove(active)


def readJobs(file):
    with open(file) as jobs_file:
        jobs_reader = csv.reader(jobs_file)

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


def writeTimesheet(tfile, clock, writetime):
    year = writetime.strftime("%Y")
    month = writetime.strftime("%m")
    day = writetime.strftime("%d")
    with open(tfile, "a") as timesheet_file:
        times_writer = csv.writer(timesheet_file)

        for job in clock['order']:
            if job != "None":
                jobtime = clock['timesheet'][job]
                times_writer.writerow([year, month, day, job, jobtime])


def updateTimes(clock, start):
    if clock['current'] != "None":
        clock['timesheet'][clock['current']] += time.time() - start


def resetJobs(clock):
    for j, t in clock['timesheet'].iteritems():
        clock['timesheet'][j] = 0.0


def eventLoop(clock, stdscr, jobsfile, savefile):
    start = None
    active = clock['current']
    message = None
    icon_shift = 1

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
                updateTimes(clock, start)
                clock['current'] = active
                start = time.time()
            elif c == ord('p'):
                updateTimes(clock, start)
                active = "None"
                clock['current'] = active

            # Add a new job
            elif c == ord('a'):
                updateTimes(clock, start)
                clock['current'] = "None"
                pauseScreen()
                printHours(clock, stdscr, active)
                newJob(clock, stdscr)
                restartScreen()

            # Delete a job
            elif c == ord('d'):
                pauseScreen()
                printHours(clock, stdscr, active)
                deleteJob(clock, stdscr, active)
                restartScreen()
                active = clock['order'][i]

            # Update timesheet
            elif c == ord('U'):
                pauseScreen()
                updateTimes(clock, start)
                outfile = jobsfile

                if outfile is None:
                    c = ord('n')
                else:
                    stdscr.addstr(maxy - 1, 0, "Use file:" + outfile + " [(y)es]/(n)o/(c)ancel?")
                    c = stdscr.getch(maxy - 1, 40)

                if is_enter(c):
                    writeJobs(outfile, clock)
                    message = "Updated " + outfile
                elif c == ord('n'):
                    printHours(clock, stdscr, active)
                    stdscr.addstr(maxy - 1, 0, "Filename: ")
                    outfile = stdscr.getstr(maxy - 1, 10, 30)
                    writeJobs(outfile, clock)
                    message = "Updated " + outfile
                restartScreen()
                clock['current'] = "None"
                active = "None"

            # Save timesheet
            elif c == ord('S'):
                pauseScreen()
                updateTimes(clock, start)
                writetime = datetime.datetime.now()
                writetime = writetime - datetime.timedelta(days = 1)
                writeTimesheet(savefile, clock, writetime)
                clock['current'] = "None"
                active = "None"
                message = "Timesheet appended to " + savefile
                restartScreen()

            # Reset all jobs to 0.0 hours
            elif c == ord('R'):
                pauseScreen()
                stdscr.addstr(maxy-1, 0, "Are you sure you wish to reset [y/n]? ")
                c = stdscr.getch(maxy-1, 38)
                if c == ord('y'):
                    resetJobs(clock)
                restartScreen()

            # Quit the program
            elif c == ord('q'):
                updateTimes(clock, start)
                writeJobs(jobsfile, clock)
                curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
                exit()


def main():
    opts = clioptions.parseArgs()
    settings = configreader.read_config(opts['configfile'])

    savefile = settings['savefile']

    if settings['jobsfile'] == None:
        clock = {'order': ['MyJob', 'None'],
                 'timesheet': {'MyJob': 0, 'None': 0}}
    else:
        clock = readJobs(settings['jobsfile'])

    # initialize curses
    stdscr = curses.initscr()
    stdscr.keypad(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.nodelay(0)

    restartScreen()

    # First job is none
    clock['current'] = "None"

    eventLoop(clock, stdscr, settings['jobsfile'], settings['savefile'])

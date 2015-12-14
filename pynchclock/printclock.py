import math
import curses


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


import curses
from clioptions import *
from database import *
from .printclock import *
from .eventloop import *


def main():
    options = parseArgs()

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

import curses
from clioptions import *
from database import *
from .printobjects import *
from .eventloop import *


def main():
    options = parseArgs()

    pynchdb = options['pynchdb']
    savefile = 'savefile.csv'

    checkfiles(pynchdb)
    clock = readClockDB(pynchdb)
    timesheet = readTimesheetDB(pynchdb)

    # initialize curses
    stdscr = curses.initscr()
    stdscr.keypad(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.nodelay(0)

    restartScreen()

    # First job is none
    clock['current'] = "None"

    eventLoopClock(clock, timesheet, stdscr, pynchdb, savefile)

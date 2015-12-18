import datetime
from clioptions import *
from database import *
from displaystats import *
from printclock import *
from editclock import *

def is_enter(c):
    return c == curses.KEY_ENTER or (c < 256 and chr(c) == "\n")

def eventLoop(clock, stdscr, pynchdb, savefile):
    start = None
    active = clock['current']
    message = None
    icon_shift = 1
    allhours = readTimesheet(savefile)

    while 1:
        maxy, maxx = stdscr.getmaxyx()

        printClock(clock, stdscr, active)

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
        njobs = len(clock['hours'].keys())
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
                updateClock(pynchdb, clock, clock['current'])
                clock['current'] = active

            # Pause
            elif c == ord('p'):
                start = updateTimes(clock, start)
                updateClock(pynchdb, clock, clock['current'])
                active = "None"
                clock['current'] = active

            # Add a new job
            elif c == ord('A'):
                start = updateTimes(clock, start)
                updateClock(pynchdb, clock, clock['current'])
                clock['current'] = "None"
                pauseScreen()
                addJob(clock, stdscr, active, pynchdb)
                restartScreen()

            # Delete a job
            elif c == ord('D'):
                pauseScreen()
                updateClock(pynchdb, clock, clock['current'])
                if active == "None":
                    message = "Cannot delete `None`"
                else:
                    deleteJob(clock, stdscr, active)
                active = "None"
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
                    updateClock(pynchdb, clock, clock['current'])

            # Update jobs list
            elif c == ord('U'):
                pauseScreen()
                start = updateTimes(clock, start)
                updateClock(pynchdb, clock, clock['current'])
                message = "Updated " + pynchdb
                restartScreen()
                clock['current'] = "None"
                active = "None"


            # Save hours
            elif c == ord('S'):
                pauseScreen()
                start = updateTimes(clock, start)
                writetime = datetime.datetime.now()
                writetime = writetime - datetime.timedelta(days = 1)
                allhours = writeTimesheet(savefile, clock, writetime, allhours)
                clock['current'] = "None"
                active = "None"
                message = "hours appended to " + savefile
                restartScreen()

            # Reset all jobs to 0.0 hours
            elif c == ord('R'):
                pauseScreen()
                printClock(clock, stdscr, active)
                stdscr.addstr(maxy-1, 0, "Are you sure you wish to reset [y/n]? ")
                c = stdscr.getch(maxy-1, 38)
                if c == ord('y'):
                    resetJobs(clock)
                restartScreen()

            # Quit the program
            elif c == ord('Q'):
                start = updateTimes(clock, start)
                updateClock(pynchdb, clock, clock['current'])
                curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
                exit()

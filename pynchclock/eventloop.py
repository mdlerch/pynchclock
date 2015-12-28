import datetime
from clioptions import *
from database import *
from displaystats import *
from printclock import *
from editclock import *
from edittimesheet import *

def eventLoopClock(clock, timesheet, stdscr, pynchdb, savefile):
    start = None
    active = clock['current']
    message = None
    icon_shift = 1

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
                start = updateClock(clock, start, pynchdb)
                clock['current'] = active

            # Pause
            elif c == ord('p'):
                start = updateClock(clock, start, pynchdb)
                active = "None"
                clock['current'] = active

            # Add a new job
            elif c == ord('A'):
                start = updateClock(clock, start, pynchdb)
                clock['current'] = "None"
                pauseScreen()
                addToClock(clock, stdscr, active, pynchdb)
                restartScreen()

            # Delete a job
            elif c == ord('D'):
                pauseScreen()
                start = updateClock(clock, start, pynchdb)
                if active == "None":
                    message = "Cannot delete `None`"
                else:
                    deleteFromClock(clock, stdscr, active, pynchdb)
                active = "None"
                restartScreen()

            # Show job stats
            elif c == ord('V'):
                if active != "None":
                    start = updateClock(clock, start, pynchdb)
                    if active in timesheet.keys():
                        displayStats(timesheet, clock, active, stdscr)
                    else:
                        message = "No stats on " + active
                    start = updateClock(clock, start, pynchdb)

            # Update jobs list
            elif c == ord('U'):
                pauseScreen()
                start = updateClock(clock, start, pynchdb)
                message = "Updated " + pynchdb
                restartScreen()
                clock['current'] = "None"
                active = "None"


            # Save today's hours
            elif c == ord('S'):
                pauseScreen()
                start = updateClock(clock, start, pynchdb)
                writedate = (datetime.datetime.now() - datetime.timedelta(days = 1)).strftime("%Y-%m-%d")
                updateTimesheet(timesheet, clock, writedate, pynchdb)
                # writeDateTimesheet(pynchdb, clock, writetime, timesheet)
                clock['current'] = "None"
                active = "None"
                message = pynchdb + " updated"
                restartScreen()

            # Reset all jobs to 0.0 hours
            elif c == ord('R'):
                pauseScreen()
                printClock(clock, stdscr, active)
                stdscr.addstr(maxy-1, 0, "Are you sure you wish to reset [y/n]? ")
                c = stdscr.getch(maxy-1, 38)
                if c == ord('y'):
                    resetJobs(clock, pynchdb)
                restartScreen()

            elif c == ord('T'):
                if active != "None":
                    start = updateClock(clock, start, pynchdb)
                    eventLoopTimesheet(timesheet, clock, active, stdscr, pynchdb)
                    restartScreen()
                    start = updateClock(clock, start, pynchdb)


            # Quit the program
            elif c == ord('Q'):
                start = updateClock(clock, start, pynchdb)
                curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
                exit()



def eventLoopTimesheet(timesheet, clock, jobname, stdscr, pynchdb):
    active = -1
    while 1:
        maxy, maxx = stdscr.getmaxyx()
        maxdates = printTimesheet(timesheet, clock, jobname, active, stdscr)
        c = stdscr.getch()

        # note: indexing is backwards for timesheet

        # UP means more older means more negative
        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if -active < maxdates:
                active += -1
        # DOWN means more recent means less negative
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if active < 0:
                active += 1
        elif is_enter(c):
            pauseScreen()
            if -active > 0:
                stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
                newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
                stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
                stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
                newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
                newhours = newHOURS * 3600 + newMINS * 60
                idx = maxdates + active
                date = timesheet[jobname]['date'][idx]
                editTimesheet(timesheet, jobname, date, newhours, pynchdb)
            if active == 0:
                stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
                newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
                stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
                stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
                newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
                newhours = newHOURS * 3600 + newMINS * 60
                editClock(clock, jobname, newhours, pynchdb)
            restartScreen()
        elif c == ord('A'):
            pauseScreen()
            stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
            newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
            newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            newhours = newHOURS * 3600 + newMINS * 60
            stdscr.addstr(maxy - 1, 0, "New year (YYYY): ")
            newYEAR = int(stdscr.getstr(maxy - 1, 17, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            stdscr.addstr(maxy - 1, 0, "New month: ")
            newMONTH = int(stdscr.getstr(maxy - 1, 11, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            stdscr.addstr(maxy - 1, 0, "New day: ")
            newDAY = int(stdscr.getstr(maxy - 1, 9, 30))
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            newdate = "{0:02}-{1:02}-{2:02}".format(newYEAR, newMONTH, newDAY)
            addToTimesheet(timesheet, jobname, newdate, newhours, pynchdb)
            sortTimesheet(timesheet, jobname)
            restartScreen()

        elif c == ord('D'):
            if active != 0:
                idx = maxdates + active
                date = timesheet[jobname]['date'][idx]
                deleteFromTimesheet(timesheet, jobname, date, pynchdb)
                active += 1


        elif c == ord('C'):
            break


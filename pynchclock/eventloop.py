import datetime
from clioptions import *
from database import *
from displaystats import *
from printobjects import *
from editclock import *
from edittimesheet import *
from csvfiles import *

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
        if c == curses.ERR:
            continue

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
            updateClockOrderDB(pynchdb, clock)
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

        # move jobs
        elif c == ord('J'):
            moveJob(clock, active, 1, pynchdb)

        elif c == ord('K'):
            moveJob(clock, active, -1, pynchdb)



        # Save today's hours
        elif c == ord('S'):
            pauseScreen()
            start = updateClock(clock, start, pynchdb)
            maxy, maxx = stdscr.getmaxyx()
            stdscr.addstr(maxy - 1, 0, "Save clock as how many days ago: ")
            daysago = int(stdscr.getstr(maxy - 1, 50, 50))
            writedate = (datetime.datetime.now() - datetime.timedelta(days = daysago)).strftime("%Y-%m-%d")
            for j, t  in clock['hours'].iteritems():
                if j in timesheet.keys():
                    if writedate in timesheet[j]['date']:
                        editTimesheet(timesheet, j, writedate, t, pynchdb)
                    else:
                        addToTimesheet(timesheet, j, writedate, t, pynchdb)
                else:
                    addToTimesheet(timesheet, j, writedate, t, pynchdb)

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
                eventLoopTimesheet(timesheet, clock, active, stdscr, start, pynchdb)
                restartScreen()
                start = updateClock(clock, start, pynchdb)

        elif c == ord('W'):
            start = updateClock(clock, start, pynchdb)
            writeClockCSV(clock, "clock.csv")
            message = "Clock written to " + "clock.csv"

        elif c == ord('I'):
            pauseScreen()
            stdscr.addstr(maxy-1, 0, "Clock source file: ")
            infile = stdscr.getstr(maxy - 1, 20, 90)
            readClockCSV(infile, clock, pynchdb)
            start = updateClock(clock, start, pynchdb)
            restartScreen()



        # Quit the program
        elif c == ord('Q'):
            updateClockOrderDB(pynchdb, clock)
            start = updateClock(clock, start, pynchdb)
            curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
            exit()



def eventLoopTimesheet(timesheet, clock, jobname, stdscr, start, pynchdb):
    active = 0
    first = 1
    message = None
    while 1:
        maxy, maxx = stdscr.getmaxyx()

        first, last, ndates = printTimesheet(timesheet, clock, jobname, active, first, stdscr)

        if message:
            stdscr.addstr(maxy - 1, 0, message)

        message = None

        c = stdscr.getch()

        # note: indexing is backwards for timesheet

        # UP means more older means more negative
        if c == curses.ERR:
            continue

        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if active > 0:
                active += -1
            # if active is less than first and first is the beginning
            if active < first and first > 1:
                first += -1
        # DOWN means more recent means less negative
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if active < ndates:
                active += 1
            # if active is greater than last shift
            if active > last:
                first += 1
        elif c == ord('E'):
            pauseScreen()
            if -active > 0:
                stdscr.addstr(maxy - 1, 0, "New HOURS (HH): ")
                newHOURS = int(stdscr.getstr(maxy - 1, 16, 30))
                stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
                stdscr.addstr(maxy - 1, 0, "New MINUTES (MM): ")
                newMINS = int(stdscr.getstr(maxy - 1, 18, 30))
                newhours = newHOURS * 3600 + newMINS * 60
                idx = ndates + active
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
                date = timesheet[jobname]['date'][active]
                deleteFromTimesheet(timesheet, jobname, date, pynchdb)
                active += -1

        elif c == ord('W'):
            writeTimesheetCSV(timesheet[jobname], "timesheet-" + jobname + ".csv")
            message = "Timesheet written to " + "timesheet-" + jobname + ".csv"

        elif c == ord('I'):
            pauseScreen()
            stdscr.addstr(maxy-1, 0, "Timesheet source file: ")
            infile = stdscr.getstr(maxy - 1, 25, 90)
            readTimesheetCSV(infile, timesheet, jobname, pynchdb)
            restartScreen()

        elif c == ord('C'):
            break

        # Show job stats
        elif c == ord('V'):
            if jobname in timesheet.keys():
                displayStats(timesheet, clock, jobname, stdscr)
            else:
                message = "No stats on " + active

        elif c == ord('Q'):
            start = updateClock(clock, start, pynchdb)
            updateClockOrderDB(pynchdb, clock)
            curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
            exit()

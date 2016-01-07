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
    selected = clock['current']
    message = None
    icon_shift = 1

    while 1:
        maxy, maxx = stdscr.getmaxyx()

        printClock(clock, stdscr, selected)

        if message:
            stdscr.addstr(maxy - 1, 0, message)
            icon_shift = 2

        if clock['current'] == "None":
            stdscr.addstr(maxy - icon_shift, 0, "||")
        else:
            stdscr.addstr(maxy - icon_shift, 0, "> " + clock['current'])

        message = None
        icon_shift = 1


        i = clock['order'].index(selected)
        njobs = len(clock['hours'].keys())
        c = stdscr.getch()

        # with nodelay, getch returns curses.ERR
        if c == curses.ERR:
            continue

        # Moving up or down
        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if clock['order'].index(selected) > 0:
                i = i - 1
                selected = clock['order'][i]
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if clock['order'].index(selected) < njobs - 1:
                i = i + 1
                selected = clock['order'][i]

        # Jump to top of list
        elif c == ord('g'):
            selected = clock['order'][0]

        # Jump to bottom of list
        elif c == ord('G'):
            selected = clock['order'][-1]


        # Selecting a job
        elif is_enter(c):
            start = updateClock(clock, start, pynchdb)
            updateClockOrderDB(pynchdb, clock)
            clock['current'] = selected

        # Pause
        elif c == ord('p'):
            start = updateClock(clock, start, pynchdb)
            selected = "None"
            clock['current'] = selected

        # Add a new job
        elif c == ord('A'):
            start = updateClock(clock, start, pynchdb)
            clock['current'] = "None"
            pauseScreen()
            addToClock(clock, stdscr, selected, pynchdb)
            restartScreen()

        # Delete a job
        elif c == ord('D'):
            pauseScreen()
            start = updateClock(clock, start, pynchdb)
            if selected == "None":
                message = "Cannot delete `None`"
            else:
                deleteFromClock(clock, stdscr, selected, pynchdb)
            selected = "None"
            restartScreen()

        # Show job stats
        elif c == ord('V'):
            if selected != "None":
                start = updateClock(clock, start, pynchdb)
                if selected in timesheet.keys():
                    stdscr.clear()
                    displayStats(timesheet, clock, selected, stdscr)
                    stdscr.clear()
                else:
                    message = "No stats on " + selected
                start = updateClock(clock, start, pynchdb)

        # Update jobs list
        elif c == ord('U'):
            pauseScreen()
            start = updateClock(clock, start, pynchdb)
            message = "Updated " + pynchdb
            restartScreen()
            clock['current'] = "None"
            selected = "None"

        # move jobs
        elif c == ord('J'):
            moveJob(clock, selected, 1, pynchdb)

        elif c == ord('K'):
            moveJob(clock, selected, -1, pynchdb)


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
            selected = "None"
            message = pynchdb + " updated"
            restartScreen()

        # Reset all jobs to 0.0 hours
        elif c == ord('R'):
            pauseScreen()
            printClock(clock, stdscr, selected)
            stdscr.addstr(maxy-1, 0, "Are you sure you wish to reset [y/n]? ")
            c = stdscr.getch(maxy-1, 38)
            if c == ord('y'):
                resetJobs(clock, pynchdb)
            restartScreen()

        elif c == ord('T'):
            if selected != "None":
                start = updateClock(clock, start, pynchdb)
                stdscr.clear()
                eventLoopTimesheet(timesheet, clock, selected, stdscr, start, pynchdb)
                stdscr.clear()
                restartScreen()
                start = updateClock(clock, start, pynchdb)

        elif c == ord('W'):
            start = updateClock(clock, start, pynchdb)
            writeClockCSV(clock, "clock.csv")
            message = "Clock written to " + "clock.csv"

        elif c == ord('I'):
            pauseScreen()
            infile = getString(stdscr, "Clock source file:", 90)
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
    selected = 0
    first = 1
    message = None
    while 1:
        maxy, maxx = stdscr.getmaxyx()

        first, last, ndates = printTimesheet(timesheet, clock, jobname, selected, first, stdscr)

        if message:
            stdscr.addstr(maxy - 1, 0, message)

        message = None
        # message = "{0}, {1}, {2}".format(first, last, ndates)

        c = stdscr.getch()

        # note: indexing is backwards for timesheet

        # UP means more older means more negative
        if c == curses.ERR:
            continue

        if c == curses.KEY_UP or (c < 256 and chr(c) == 'k'):
            if selected > 0:
                selected += -1
            # if selected is less than first and first is the beginning
            if selected < first and first > 1:
                first += -1
        # DOWN means more recent means less negative
        elif c == curses.KEY_DOWN or (c < 256 and chr(c) == 'j'):
            if selected < ndates:
                selected += 1
            # if selected is greater than last shift
            if selected > last:
                first += 1

        elif c == ord('g'):
            selected = 0
            first = 1
        elif c == ord('G'):
            selected = ndates
            first = ndates - (last - first)

        elif c == ord('E'):
            pauseScreen()
            if -selected > 0:
                newHOURS = getInt(stdscr, "New hours (HH):", 0, 24)
                newMINS = getInt(stdscr, "New minutes (MM):", 0, 60)
                newTIME = newHOURS * 3600 + newMINS * 60
                idx = ndates + selected
                date = timesheet[jobname]['date'][idx]
                editTimesheet(timesheet, jobname, date, newTIME, pynchdb)
            if selected == 0:
                newHOURS = getInt(stdscr, "New hours (HH):", 0, 24)
                newMINS = getInt(stdscr, "New minutes (MM)", 0, 60)
                newTIME = newHOURS * 3600 + newMINS * 60
                editClock(clock, jobname, newTIME, pynchdb)
            restartScreen()
        elif c == ord('A'):
            pauseScreen()
            newHOURS = getInt(stdscr, "New hours (HH):", 0, 24)
            newMINS = getInt(stdscr, "New minutes (MM):", 0, 60)
            newYEAR = getInt(stdscr, "New year (YYYY):", 1984, 3000)
            newMONTH = getInt(stdscr, "New month:", 1, 12)
            newDAY = getInt(stdscr, "New day:", 0, 31)
            stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
            newTIME = newHOURS * 3600 + newMINS * 60
            newDATE = "{0:02}-{1:02}-{2:02}".format(newYEAR, newMONTH, newDAY)
            addToTimesheet(timesheet, jobname, newDATE, newTIME, pynchdb)
            sortTimesheet(timesheet, jobname)
            restartScreen()

        elif c == ord('D'):
            if selected != 0:
                date = timesheet[jobname]['date'][-selected]
                deleteFromTimesheet(timesheet, jobname, date, pynchdb)
            if selected == ndates:
                selected += -1

        elif c == ord('W'):
            writeTimesheetCSV(timesheet[jobname], "timesheet-" + jobname + ".csv")
            message = "Timesheet written to " + "timesheet-" + jobname + ".csv"

        elif c == ord('I'):
            pauseScreen()
            infile = getString(stdscr, "Timesheet source file:", 90)
            readTimesheetCSV(infile, timesheet, jobname, pynchdb)
            restartScreen()

        elif c == ord('C'):
            break

        # Show job stats
        elif c == ord('V'):
            if jobname in timesheet.keys():
                stdscr.clear()
                displayStats(timesheet, clock, jobname, stdscr)
                stdscr.clear()
            else:
                message = "No stats on " + selected

        elif c == ord('Q'):
            start = updateClock(clock, start, pynchdb)
            updateClockOrderDB(pynchdb, clock)
            curses.nocbreak(); stdscr.keypad(0); curses.echo(); curses.endwin()
            exit()

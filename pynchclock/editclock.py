from database import *
import time

def addToClock(clock, stdscr, active, pynchdb):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "New job: ")
    newjob = stdscr.getstr(maxy - 1, 9, 30)
    clock['hours'][newjob] = 0.0
    idx = clock['order'].index(active)
    clock['order'].insert(idx, newjob)
    addToClockDB(pynchdb, clock, newjob)


def deleteFromClock(clock, stdscr, active, pynchdb):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "Are you sure you wish to delete " + active + " [y/n]? ")
    c = stdscr.getch(maxy - 1, 50)
    if c == ord('y'):
        if clock['current'] == active:
            clock['current'] = "None"
        clock['hours'].pop(active)
        clock['order'].remove(active)
        deleteFromClockDB(pynchdb, active)

def moveJob(clock, jobname, delta, pynchdb):
    njobs = len(clock['order'])
    idx = clock['order'].index(jobname)
    if (idx <= 0 and delta < 0) or (idx >= njobs - 2 and delta > 0):
        return
    newidx = idx + delta
    if newidx < 0:
        newidx = 0
    if newidx >= njobs - 1:
        newidx = njobs - 2
    clock['order'].pop(idx)
    clock['order'] = clock['order'][:newidx] + [jobname] + clock['order'][newidx:]


def resetJobs(clock, pynchdb):
    for j, t in clock['hours'].iteritems():
        clock['hours'][j] = 0.0
        updateClockDB(pynchdb, clock, j)

def updateClock(clock, start, pynchdb):
    if clock['current'] != "None":
        clock['hours'][clock['current']] += time.time() - start
        updateClockDB(pynchdb, clock, clock['current'])
    return time.time()

def editClock(clock, jobname, hours, pynchdb):
    clock['hours'][jobname] = hours
    editClockDB(pynchdb, jobname, hours)


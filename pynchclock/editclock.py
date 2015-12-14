import time

def addJob(clock, stdscr, active):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "New job: ")
    newjob = stdscr.getstr(maxy - 1, 9, 30)
    clock['hours'][newjob] = 0.0
    idx = clock['order'].index(active)
    clock['order'].insert(idx, newjob)

def deleteJob(clock, stdscr, active):
    maxy, maxx = stdscr.getmaxyx()
    stdscr.addstr(maxy - 1, 0, "Are you sure you wish to delete " + active + " [y/n]? ")
    c = stdscr.getch(maxy - 1, 50)
    if c == ord('y'):
        if clock['current'] == active:
            clock['current'] = "None"
        clock['hours'].pop(active)
        clock['order'].remove(active)

def resetJobs(clock):
    for j, t in clock['hours'].iteritems():
        clock['hours'][j] = 0.0

def updateTimes(clock, start):
    if clock['current'] != "None":
        clock['hours'][clock['current']] += time.time() - start
    return time.time()


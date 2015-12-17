import curses

def checkWindowSize(stdscr, x, y):

    maxy, maxx = stdscr.getmaxyx()

    if maxy < 4 or maxx < 9:
        stdscr.addstr(0, 0, ".")
        stdscr.refresh()
        return True

    if maxy < y or maxx < x:
        stdscr.addstr(0, 0, "Window")
        stdscr.addstr(1, 0, "too small")
        stdscr.refresh()
        return True

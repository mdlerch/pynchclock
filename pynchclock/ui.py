def getString(stdscr, message, maxlength):
    maxy, maxx = stdscr.getmaxyx()
    # if len(message) + maxlength >= maxx:

    stdscr.addstr(maxy - 1, 0, message)
    answer = stdscr.getstr(maxy - 1, len(message) + 1, maxlength)
    stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
    return answer.replace(" ", "_")

def getInt(stdscr, message, maxlo, maxhigh):
    answer = maxlo - 1
    maxy, maxx = stdscr.getmaxyx()
    while answer < maxlo or answer > maxhigh:
        stdscr.addstr(maxy - 1, 0, message)
        answer = int(stdscr.getstr(maxy - 1, len(message) + 1, 4))
        stdscr.addstr(maxy - 1, 0, " " * (maxx - 1))
    return answer

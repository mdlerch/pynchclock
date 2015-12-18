import sqlite3
import csv
import os.path

def checkfiles(pynchdb):
    if not os.path.isfile(pynchdb):
        conn = sqlite3.connect(pynchdb)
        c = conn.cursor()
        c.execute('''CREATE TABLE clock
                 (job text, hours real, joborder int)''')
        c.execute("INSERT INTO clock VALUES ('MyJob', 0, 1)")
        conn.commit()
        c.execute('''CREATE TABLE timesheet
                 (job text, date date, hours real)''')
        conn.commit()
        conn.close()


def readClock(pynchdb):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()

    clock = {'hours': {}}
    clock['order'] = []
    for row in c.execute('SELECT job, hours FROM clock ORDER BY joborder'):
        jobname, hours = row
        clock['hours'][jobname] = float(hours)
        clock['order'].append(jobname)

    conn.close()

    clock['hours']['None'] = 0.0
    clock['current'] = "None"
    clock['order'].append("None")
    return clock


def updateClock(pynchdb, clock, jobname):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()

    c.execute("UPDATE clock SET hours = ? WHERE job = ?",
              (clock['hours'][jobname], jobname))
    conn.commit()
    conn.close()


def addToClock(pynchdb, clock, jobname):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    c.execute("INSERT INTO clock VALUES (?, ?, ?)",
              (jobname, clock['hours'][jobname], 0))
    conn.commit()
    conn.close()
    updateClockOrder(pynchdb, clock)


def updateClockOrder(pynchdb, clock):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    idx = 0
    for jobname in clock['order']:
        idx += 1
        c.execute("UPDATE clock SET joborder = ? WHERE job = ?", (idx, jobname))
        conn.commit()
    conn.close()

def deleteFromClock(pynchdb, jobname):
    conn = sqlite3.connect(pynchdb)
    c = conn.cursor()
    c.execute("DELETE FROM clock WHERE job = ?", (jobname, ))
    conn.commit()
    conn.close()



# def readTimesheet(pynchdb):
#     conn = sqlite3.connect(pynchdb)
#     c = conn.cursor()

#     timesheet = {

# def updateTimesheet():
#     return

# def addToTimesheet(arglist):
#     return









def writeTimesheet(tfile, clock, writetime, allhours):
    year = writetime.strftime("%Y")
    month = writetime.strftime("%m")
    day = writetime.strftime("%d")

    for job in clock['order']:
        if job != "None":
            if job not in allhours['allhours'].keys():
                allhours['allhours'][job] = []
                allhours['allhours'][job] += [0] * len(allhours['dates'])
            allhours['allhours'][job] += [clock['hours'][job]]

    allhours['dates'].append(year + "-" + month + "-" + day)

    # deleted jobs
    for job in allhours['allhours'].keys():
        if job not in clock['order']:
            allhours['allhours'][job] += [0]


    with open(tfile, "wb") as timesheet_file:
        times_writer = csv.writer(timesheet_file)

        i = 0
        for date in allhours['dates']:
            datelist = date.split("-")
            year = datelist[0]
            month = datelist[1]
            day = datelist[2]
            for job in allhours['allhours'].keys():
                if job != "None":
                    jobtime = allhours['allhours'][job][i]
                    times_writer.writerow([year, month, day, job, jobtime])
            i += 1

    return allhours


def readTimesheet(tfile):
    if not os.path.isfile(tfile):
        return {'dates': [], 'allhours': {}}

    with open(tfile) as ts:
        ts_reader = csv.reader(ts)

        timesheet = {}
        dates = []

        for row in ts_reader:
            # first new date
            year = str(row[0])
            month = str(row[1])
            day = str(row[2])
            the_date = year + "-" + month + "-" + day
            if the_date not in dates:
                dates.append(the_date)
            if row[3] not in timesheet.keys():
                timesheet[row[3]] = [float(row[4])]
            else:
                timesheet[row[3]] += [float(row[4])]

    return {'dates': dates, 'allhours': timesheet}

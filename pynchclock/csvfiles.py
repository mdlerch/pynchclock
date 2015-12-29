import csv
from database import *
from edittimesheet import *

def writeClockCSV(clock, filename):
    with open(filename, "wb") as outfile:
        writer = csv.writer(outfile)

        for jobname in clock['order']:
            if jobname != "None":
                writer.writerow([jobname, clock['hours'][jobname]])

def writeTimesheetCSV(jobtime, filename):
    with open(filename, "wb") as outfile:
        writer = csv.writer(outfile)

        for i in range(0, len(jobtime['date'])):
            writer.writerow([jobtime['date'][i], jobtime['hours'][i]])

def readClockCSV(filename, clock, pynchdb):
    clock['order'].pop()
    with open(filename) as infile:
        reader = csv.reader(infile)

        for row in reader:
            clock['hours'][row[0]] = float(row[1])
            clock['order'].append(row[0])
            addToClockDB(pynchdb, clock, row[0])
    clock['order'].append("None")

def readTimesheetCSV(filename, timesheet, jobname, pynchdb):
    with open(filename) as infile:
        reader = csv.reader(infile)

        for row in reader:
            addToTimesheet(timesheet, jobname, row[0], float(row[1]), pynchdb)


import time
import csv
import math

def printHours(hours):
    i = 1
    print("")
    for k,t in hours.iteritems():
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        print("{3}.  {0}: {1:.0f} hours, {2:.2f} minutes".format(k, math.floor(h), m, i))
        i += 1
    print("")

def readJobs(file):
    with open(file) as jobs_file:
        jobs_reader = csv.reader(jobs_file)
        hours = {}
        for row in jobs_reader:
            hours[row[0]] = float(row[1])
        return hours

def writeJobs(file, hours):
    with open(file, "wb") as jobs_file:
        jobs_writer = csv.writer(jobs_file)
        for key, val in hours.items():
            jobs_writer.writerow([key, val])

jobfile = "/home/mike/.config/pynchclock/jobs.csv"
hours = readJobs(jobfile)

printHours(hours)

jobs = hours.keys()
cur_job_i = input('Pick a job (0 to quit): ')
cur_job = jobs[cur_job_i - 1]
while (cur_job != 0):
    printHours(hours)
    start = time.time()
    next_job_i = input('Pick a job (0 to quit): ')

    if next_job_i == 0:
        writeJobs(jobfile, hours)
        exit()

    next_job = jobs[next_job_i - 1]
    hours[cur_job] += time.time() - start
    cur_job = next_job




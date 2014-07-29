import time
import csv
import math

def printHours(hours):
    for k,t in hours.iteritems():
        h = t / 3600.0
        m = (h - math.floor(h)) * 60
        print("Job {0}, {1:.0f} hours, {2:.2f} minutes".format(k, math.floor(h), m))

def readJobs(file):
    with open(file) as jobs_file:
        jobs_reader = csv.reader(jobs_file)
        for row in jobs_reader:
            print row


jobs = [ 0, 1, 2, 3, 4, 5]
hours = {x: 0.0 for x in jobs}

print(jobs)

readJobs("/home/mike/.config/pynchclock/jobs.csv")

cur_job = input('Pick a job (0 to quit): ')
while (cur_job != 0):
    printHours(hours)
    start = time.time()
    next_job = input('Pick a job (0 to quit): ')
    hours[cur_job] += time.time() - start
    cur_job = next_job




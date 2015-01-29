import csv
import os.path

def writeTimesheet(tfile, clock, writetime, allhours):
    year = writetime.strftime("%Y")
    month = writetime.strftime("%m")
    day = writetime.strftime("%d")

    for job in clock['order']:
        if job != "None":
            if job not in allhours['allhours'].keys():
                allhours['allhours'][job] = []
                allhours['allhours'][job] += [0] * len(allhours['dates'])
            allhours['allhours'][job] += [clock['timesheet'][job]]

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

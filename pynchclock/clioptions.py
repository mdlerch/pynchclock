import argparse
import os.path

parse = argparse.ArgumentParser()


def parseArgs():
    default_jobsfile = "./jobs.csv"
    default_savefile = "./timesheet.csv"

    parse.add_argument("-j", "--jobsfile", default=default_jobsfile)
    parse.add_argument("-t", "--timesheet", default=default_savefile)

    args = parse.parse_args()

    opts = {'jobsfile': args.jobsfile,
            'savefile': args.timesheet}

    return opts

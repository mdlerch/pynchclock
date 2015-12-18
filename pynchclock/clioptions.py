import argparse
import os.path

parse = argparse.ArgumentParser()


def parseArgs():
    default_pynchdb = "./pynchclock.db"

    parse.add_argument("-d", "--pynchdb", default=default_pynchdb)

    args = parse.parse_args()

    opts = {'pynchdb': args.pynchdb,}

    return opts

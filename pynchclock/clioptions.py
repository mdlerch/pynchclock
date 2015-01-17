import argparse
import os.path

parse = argparse.ArgumentParser()


def parseArgs():
    default_config = os.path.expanduser("~/.config/pynchclock/pynchclockrc")
    parse.add_argument("-c", "--configfile", default=default_config)

    args = parse.parse_args()

    if not os.path.isfile(args.configfile):
        args.configfile = None

    opts = {'configfile': args.configfile}

    return opts

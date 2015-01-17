import ConfigParser
import os.path


settings = ConfigParser.ConfigParser({'savedir': '$HOME',
                                      'jobsfile': None})


def read_config(configfile):
    sett = {}
    try:
        settings.read(configfile)
        section = "main"
        options = settings.options(section)
        for option in options:
            try:
                sett[option] = settings.get(section, option)
            except:
                print("Exception on option " + option)
                sett[option] = None
    except:
        print("Issue with config file" + configfile + ".  May not exist")

    if sett['jobsfile'] is not None and not os.path.isfile(sett['jobsfile']):
        print("jobsfile does not exist")
        sett['jobsfile'] = None

    if sett['savedir'] is not None and not os.path.exists(sett['savedir']):
        print("savedir does not exist")
        sett['savedir'] = None

    return sett

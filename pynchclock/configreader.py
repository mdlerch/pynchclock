import ConfigParser
import os.path

default_save = os.path.expanduser("~")
pc_settings = ConfigParser.ConfigParser({'savedir': default_save,
                                         'jobsfile': None,
                                         'savefile': "timesheet.csv"})


def read_config(configfile):
    if configfile is None:
        return pc_settings

    settings = {}
    try:
        pc_settings.read(configfile)
        section = "main"
        options = pc_settings.options(section)
        for option in options:
            try:
                settings[option] = pc_settings.get(section, option)
            except:
                print("Exception on option " + option)
                settings[option] = None
    except:
        print("Issue with config file" + configfile + ".  May not exist")

    if settings['jobsfile'] is not None and not os.path.isfile(settings['jobsfile']):
        print("jobsfile does not exist")
        settings['jobsfile'] = None

    if settings['savedir'] is not None and not os.path.exists(settings['savedir']):
        print("savedir does not exist")
        settings['savedir'] = None

    return settings

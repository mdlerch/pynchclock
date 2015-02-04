import ConfigParser
import os.path

def read_config(options):
    configfile = options['configfile']

    def_settings = {'dir': os.path.expanduser("~"),
                   'jobs': "jobs.csv",
                   'timesheet': "timesheet.csv",
                   'dayshift': 1}

    pc_settings = def_settings

    if configfile is None:
        return pc_settings

    Config = ConfigParser.ConfigParser()

    try:
        Config.read(configfile)
        section = "main"
        options = Config.options(section)
        for option in options:
            try:
                if option == "dayshift":
                    pc_settings[option] = Config.getint("main", option)
                else:
                    pc_settings[option] = Config.get("main", option)
            except:
                print("Exception on option " + option)
    except:
        print("Issue with config file " + configfile + ". May not exist")
        pc_settings = def_settings

    if not os.path.exists(pc_settings['dir']):
        print("Directory " + pc_settings['dir'] + " does not exist")
        pc_settings['dir'] = def_settings['dir']

    if pc_settings['dir'][len(pc_settings['dir']) - 1] != "/":
            pc_settings['dir'] = pc_settings['dir'] + "/"

    return pc_settings

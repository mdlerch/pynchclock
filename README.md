`pynchclock` is a CLI app written in python to help with time tracking.

It's a simple time sheet, or punch card, or punch clock app.

Install with `pip install git+git://github.com/mdlerch/pynchclock.git`

#### Status ####

It's pretty usable _for me_.  More configuration will eventually be available.

### Configuration ###

The default config file is `$HOME/.config/pynchclock/pynchclockrc`

This is my config:

    [main]
    savedir = /home/mike/work/time/
    jobsfile = /home/mike/work/jobs.csv

`jobsfile` is a file to read and, by default, write to.  Populated this with
something like

    job 1, 0
    job 2, 0

The first column is the name of the job, the second is the current amount of
time spent in that job (in seconds).

`savedir` is the default location to save new csv's (of updated times).

That's all the configuration that is currently available.

### Keybindings ###

Enter: start timing on a job.

Up, k: scroll up on jobs.

Down, j: scroll down on jobs.

p: set job to "None".

a: add a new job.

S: save current times to a file.

R: reset all job times to 0.

### Details ###

python 2.7

---
title: pynchclock
author: by Michael Lerch
css: kultiad.css
---

About
=====

`pynchclock` is a CLI time tracker application written in `python 2.7`.

Installation
============

```
pip install git+git://github.com/mdlerch/pynchclock.git
```

Usage
=====

Controls
--------

### Clock screen ###

The main screen displays the **clock**.
The **clock** contains _today's_ jobs and their associated hours.
From the **clock** screen, use the below controls:

- Launch with `pynchclock`.
- Scroll with `j`/`k` or `UP`/`DOWN`.
- Add new job in place with `A`.
- Delete a job with `D`
- Start timing a job with `ENTER`.
- Quickly pause (job == None) with `p`.
- Reset all clock hours to 0.0 with `R`.
- Update current clock hours to disk with `U`.
- Save current clock hours to the historic **timesheet** with `S`.
- Write the clock to a csv with `W`.
- Import a csv as the clock with `I`.
- Quit the program with with with `Q`.
- Switch to **timesheet** screen with `T`.
- View a graphical display of a job's historic hours with `V`.

### Timesheet screen ###

The timesheet screen displays the historic times for a selected job.
From the timesheet screen, current (clock) and historic (timesheet) hours can
be adjusted.
Enter the timesheet screen from the main screen with `T`.

- Scroll with `j`/`k` or `UP`/`DOWN`.
- Edit the currently selected time with `E`.
- Add an additional date and hours with `A`.
- Delete the selected entry with `D`.
- Write the job's timesheet history with `W`.
- Import the job's history from a csv with `I`.
- Return to the clock screen with `C`.
- View a graphical display of the job's historic hours with `V`.
- Quit the program with `Q`.


### Graph screen ###

The graph screen provides a ascii plot of the timesheet for a particular job.
Enter the graph screen from the main screen with `V`.

- Return to the previous screen with any key.


To do
=====

- Protect against illegal user input.
- Support configuration options
    - database file
    - keys
    - colors



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

Components
----------

There are two components to `pynchclock`.
The first is the component is the **clock** which stores _today's_ job names and
hours.
The second component is the **timesheet** which stores _historic_ job names,
hours, and the dates of those hours.


Controls
--------

### Main screen ###

The main screen displays the **clock**.
From the **clock**, use the below controls:

- Launch with `pynchclock`.
- Scroll with `j`/`k` or `UP`/`DOWN`.
- Add new job in place with `A`.
- Delete a job with `D`
- Start timing a job with `ENTER`.
- Quickly pause (job == None) with `p`.
- Reset all clock hours to 0.0 with `R`.
- Update current clock hours to disk `U`.
- Save current clock hours to the historic timesheet `S`.
- Quit with `Q`.

### Edit screen ###

The edit screen can be used to adjust recorded times.
Enter the edit screen from the main screen with `E`.

- Scroll with `j`/`k` or `UP`/`DOWN`.
- Edit the currently selected time with `ENTER`.
- Add an additional date and hours with `A`.
- Delete the selected entry with `D`.
- Quit the edit screen and return to the main screen with `Q`.


### Graph screen ###

The graph screen provides a ascii plot of the timesheet for a particular job.
Enter the graph screen from the main screen with `V`.

- Return to the main screen with any key.


To do
=====

- Protect against illegal user input.
- Save clock and timesheet to csv
- Improve method of going from clock to timesheet (today's date? yesterday?  custom?)
- Support configuration options
    - database file
    - keys
    - colors



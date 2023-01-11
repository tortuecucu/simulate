import blinker

"""this module holds all the signals that are triggered and listened during simulation
"""

Tick:blinker.Signal=blinker.signal('tick')
NewDay:blinker.Signal=blinker.signal('new_day')
NewWeek:blinker.Signal=blinker.signal('new_week')
NewMonth:blinker.Signal=blinker.signal('new_month')
NewYear:blinker.Signal=blinker.signal('new_year')
ClockStop:blinker.Signal=blinker.signal('clock_stop')
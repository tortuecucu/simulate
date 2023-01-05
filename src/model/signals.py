import blinker

"""this module holds all the signals that are triggered and listened during simulation
"""

Tick:blinker.Signal=blinker.signal('tick')
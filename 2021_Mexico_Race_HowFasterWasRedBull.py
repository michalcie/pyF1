from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
import joypy
import pandas as pd
from fastf1 import plotting
import numpy as np

"""
Mexico GP 2021
Red Bull seemes to have an edge over Mercedes in the race, Hamilton refered to them during the race multiple time that
'Guys, they are too fast for us'
But how much quicker was Red Bull?
"""

laps, event = tt.crate_event(2021, 'USA', 'R') #No mistake as of now 13.11.2021 'USA' returns Mexico City GP - issue#23

"""Driver list should contain only finishers to ensure minimal number of valid laps """
# drivers_list = ['VER', 'HAM', 'PER', 'GAS', 'LEC', 'SAI', 'VET', 'ALO', 'NOR', 'GIO', 'RIC']
drivers_list = ['VER', 'HAM', 'PER','BOT']

xliml = 78
xlimr = 86
best_lap_number = 15 #notused yet
tt.ridgeline(drivers_list, laps, xliml, xlimr, best_lap_number)

"""
It seems that Red Bull was faster, median and average are about 0.2 faster than Hamilton
It doesn't seem much, but it is worth to notice, that 25 quantile is much further on both Red Bull cars
also Perez.
It might be that in Mexico Red Bull potential was much higher and Red Bull was cotrolling the situation,
but it was to hard to overtake Hamilton despite very good pace.
"""

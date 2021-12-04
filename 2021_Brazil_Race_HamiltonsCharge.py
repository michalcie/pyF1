from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
import joypy
import pandas as pd
from fastf1 import plotting
import fastf1 as ff1
import numpy as np

"""
Brazil 2021
Hamilton charges from P10 to P1, passing title rival - Verstappen and finishing over 10 seconds in front of him
It's one of this historic GPs
"""

"""
Special workaround for Brazil GP
"""
weekend = ff1.get_session(2021, 'Brazil')
weekend.data['raceName'] = "São Paulo Grand Prix"
session = ff1.core.Session(weekend, 'Race')
laps = session.load_laps(with_telemetry=True, livedata=None)

"""Driver list should contain only finishers to ensure minimal number of valid laps """
drivers_list = ['HAM','VER','BOT','PER','LEC','SAI','GAS','OCO','ALO','NOR']
# drivers_list = ['BOT','VER','SAI','PER','HAM','NOR','LEC','GAS','OCO','VET','RIC','ALO']

xliml = None
xlimr = None
best_lap_number = 15 #notused yet
tt.ridgeline(drivers_list, laps, "Brazil 2021 - Race - Hamilton Charges P10 -> P1", xliml, xlimr, best_lap_number)

"""

"""

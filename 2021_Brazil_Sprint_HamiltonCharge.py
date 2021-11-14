from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
import pandas as pd
from fastf1 import plotting
import numpy as np
import fastf1 as ff1

"""
Brasil 2021,
Hamilton charges from P20 to P5 after DRS infrigement - DRS gap bigger than 85 mm
Sprint was 24 laps with Hamilton finishing 5, ~1.5s from P4.
"""

# laps, event = tt.crate_event(2021, 19, 'Sprint Qualifying') #No mistake as of now 13.11.2021 'USA' returns Mexico City GP - issue#23

# event = ff1.get_session(2021, 19, 'SQ')
# print(event.name)
# # event = event.get_quali()
# laps = event.load_laps(with_telemetry=True, livedata=None)

weekend = ff1.get_session(2021, 'Brazil')
weekend.data['raceName'] = "São Paulo Grand Prix"
session = ff1.core.Session(weekend, 'Sprint Qualifying')
laps = session.load_laps(with_telemetry=True, livedata=None)

"""Driver list should contain only finishers to ensure minimal number of valid laps """
drivers_list = ['BOT', 'VER','SAI', 'PER', 'HAM', 'NOR', 'LEC', 'GAS', 'OCO', 'VET', 'RIC', 'ALO']

xliml = None
xlimr = None
best_lap_number = 15 #notused yet
tt.ridgeline(drivers_list, laps, "Brazil 2021 - Sprint Qualifying - Hamilton Charges P20 -> P5", xliml, xlimr, best_lap_number)

"""

"""

from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
import matplotlib
import matplotlib.dates as dates

import datetime
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

laps, event = tt.crate_event(2021, 'Mexico', 'R')

"""Driver list should contain only finishers to ensure minimal number of valid laps """
# drivers_list = ['VER', 'HAM', 'PER', 'GAS', 'LEC', 'SAI', 'VET', 'ALO', 'NOR', 'GIO', 'RIC']
drivers_list = ['VER', 'HAM', 'PER', 'BOT']

xliml = None
xlimr = None
best_lap_number = 15  # notused yet
# tt.ridgeline(drivers_list, laps, "Mexico 2021 - How Fast was Redbull?", xliml, xlimr, best_lap_number)

"""
It seems that Red Bull was faster, median and average are about 0.2 faster than Hamilton
It doesn't seem much, but it is worth to notice, that 25 quantile is much further on both Red Bull cars
also Perez.
It might be that in Mexico Red Bull potential was much higher and Red Bull was cotrolling the situation,
but it was to hard to overtake Hamilton despite very good pace.
"""

"""
Max dirty trick
"""

# Bottas is +2 Laps in the results
BOT = laps.pick_driver('BOT')
# print(BOT[['LapNumber', 'LapTime', 'Stint', 'Time', 'IsAccurate']].loc[63:67])
BOT65 = BOT[BOT['LapNumber'] == 65].iloc[0]
BOT66 = BOT[BOT['LapNumber'] == 66].iloc[0]
BOT67 = BOT[BOT['LapNumber'] == 67].iloc[0]

VER = laps.pick_driver('VER')
VER67 = VER[VER['LapNumber'] == 67].iloc[0]
VER68 = VER[VER['LapNumber'] == 68].iloc[0]
VER69 = VER[VER['LapNumber'] == 69].iloc[0]
VER70 = VER[VER['LapNumber'] == 70].iloc[0]


fig, ax = tt.overlay_laps(BOT65, VER67, 'Dirty Max', 'Bottas L65', 'Verstappen L67',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])

size = len(ax)
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 2296, 2400, color='g')
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 2568, 2867, color='g')
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 2959, 3062, color='g')
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 3238, 3352, color='g')

plt.show()

fig, ax = tt.overlay_laps(BOT65, VER67, 'Dirty Max', 'Bottas L65', 'Verstappen L67',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'],
                          mode='time', timeMode='Date')
plt.show()

print('Lead lap 68 - Accurate for Bottas (L66), Stint 4')
print('Bottas:')
print(BOT66['LapTime'])
print('Verstappen:')
print(VER68['LapTime'])

fig, ax = tt.overlay_laps(BOT66, VER68, 'Dirty Max', 'Bottas L66', 'Verstappen L68',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 524, 564, color='c')
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 2180, 2220, color='c')
for i in range(size):
    ax = tt.overlay_highlight(ax, i, 4280, 4320, color='c')
plt.show()

fig, ax = tt.overlay_laps(BOT66, VER68, 'Dirty Max', 'Bottas L66', 'Verstappen L68',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'],
                          mode='time', timeMode='Date')
plt.show()

VER = VER.pick_fastest()
fig, ax = tt.overlay_laps(VER, BOT66, 'Why was not Bottas fast?', 'Verstappen fastest', 'Bottas attempt',
                          graph=['speed', 'delta', 'throttle', 'brake'])
plt.show()

drvs = [VER, BOT66]
tt.overlay_map_multi(drvs, event, mode='manual')
plt.show()

from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np

"""
Qualifying ####################################################################
"""

laps, event = tt.crate_event(2021, 'AbuDhabi', 'Q')

""" To tow or not to tow
What a differance tow made Max towed by Perez - 1st timed lap
Perez towed by Max - 1st timed lap
Closing gap in S2 to Mercedes??
"""

MAX = laps.pick_driver('VER')
PER = laps.pick_driver('PER')
HAM = laps.pick_driver('HAM')

"""
Max Quali time in Q3 is 1.22.109 which is L15 - he was towed by Perez
Second timed lap was abandoned by Max - L18
Perez was towed by Max on his L20

For No tow:
Max Q2 best (1.22.800) - L12 #looks like he was towed after all
Max Q1 best (1.23.332) - L5 #finally no tow

HAM Q1/Q3 1.22.845 - L5, best

More no tow laps for Max:
Q2 - 1.23.189 - L8
"""

# print(HAM[['LapNumber', 'LapTime', 'Time']])

MAX_towed = MAX[MAX['LapNumber'] == 15].iloc[0]
# MAX_notow = MAX[MAX['LapNumber'] == 12].iloc[0] #looks like he was towed after all
MAX_notow = MAX[MAX['LapNumber'] == 5].iloc[0]  # finally, no tow
HAM_notow = HAM[HAM['LapNumber'] == 5].iloc[0]
# MAX_notow = MAX[MAX['LapNumber'] == 8].iloc[0]  #one more attempt to find Max no tow - tow
MAX_aband = MAX[MAX['LapNumber'] == 18].iloc[0]
PER_towed = PER[PER['LapNumber'] == 20].iloc[0]
HAM_Q1lap = HAM[HAM['LapNumber'] == 5].iloc[0]

HAM_best = HAM.pick_fastest()
PER_best = PER.pick_fastest()

fig, ax = tt.overlay_laps(MAX_towed, HAM_best, 'To Tow: Best Lap Comparison', 'Max', 'Hamilton ',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])
plt.show()

fig, ax = tt.overlay_laps(MAX_notow, HAM_best, 'Not to tow: lap comparison Q2/Q3', 'Max - Q2', 'Hamilton - Q3 - best',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])
plt.show()

fig, ax = tt.overlay_laps(MAX_notow, HAM_notow, 'Not to tow: lap comparison Q2/Q1', 'Max - Q2', 'Hamilton - Q1',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])
plt.show()

print('#############################')
print(' ')
print('SPEED COMPARISON')
print(' ')
print('Lewis best - no tow:')
print('Lewis Speed Trap: ')
print(HAM_best[['SpeedST']])
print('Lewis telemetry max speed:')
print(HAM_best.telemetry['Speed'].max(), ' kmh')

print(' ')
print('Lewis Q1:')
print('Lewis Speed Trap: ')
print(HAM_notow[['SpeedST']])
print('Lewis telemetry max speed:')
print(HAM_notow.telemetry['Speed'].max(), ' kmh')

print(' ')
print('Max towed:')
print('Max towed Speed Trap: ')
print(MAX_towed[['SpeedST']])
print('Max telemetry max speed:')
print(MAX_towed.telemetry['Speed'].max(), ' kmh')

print(' ')
print('Max no tow:')
print('Max no tow Speed Trap: ')
print(MAX_notow[['SpeedST']])
print(MAX_notow.telemetry['Speed'].max(), ' kmh')
print('#############################')

"""
Red Bull gap to Merc in S2
"""
print(' ')
print('SECTOR GAP')
print(' ')
print('Max - No tow:')
print(MAX_notow[['Sector1Time', 'Sector2Time', 'Sector3Time']])
print('Max - Tow:')
print(MAX_towed[['Sector1Time', 'Sector2Time', 'Sector3Time']])
print('Lewis best:')
print(HAM_best[['Sector1Time', 'Sector2Time', 'Sector3Time']])
print('Lewis notow:')
print(HAM_notow[['Sector1Time', 'Sector2Time', 'Sector3Time']])

drivers = ['HAM', 'VER']
tt.overlay_map_multi(drivers, laps, rotate=1)

"""
RACE ###########################################################################
"""

laps, event = tt.crate_event(2021, 'AbuDhabi', 'R')

drivers_list = ['VER']
ref_driver = 'HAM'

fig, ax = tt.plot_cumulative_time(laps, drivers_list, ref_driver)
comment_list = [['Checo is a legend', (19, -5), 5, 9, -20, (20, -10)],
                ['Max Chase - 23 laps younger hard tires', (44, -14.5), 22, 5, 20, (34, -22)],
                ['Max falling behind', (27, -4), 20, 4, -20, (37, -2)]]
ax = tt.annotation(ax, comment_list)
plt.show()

tt.plot_driver_tire_data(['VER'], laps)
plt.show()

tt.plot_driver_tire_data(['HAM'], laps)
plt.show()

drivers_list = ['VER', 'HAM', 'SAI', 'TSU', 'GAS', 'BOT', 'NOR']
tt.ridgeline(drivers_list, laps, 'Abu Dhabi Season Showdown', None, None, None)
plt.show()

"""
RACE
Checo is a legend L20
"""

VER = laps.pick_driver('VER')
VER = VER[VER['LapNumber'] == 20].iloc[0]
HAM = laps.pick_driver('HAM')
HAM = HAM[HAM['LapNumber'] == 20].iloc[0]

fig, ax = tt.overlay_laps(VER, HAM, 'Checo is a legend - L20', 'Max', 'Hamilton ',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])
plt.show()

VER = laps.pick_driver('VER')
VER = VER[VER['LapNumber'] == 21].iloc[0]
HAM = laps.pick_driver('HAM')
HAM = HAM[HAM['LapNumber'] == 21].iloc[0]

fig, ax = tt.overlay_laps(VER, HAM, 'Checo is a legend - L21', 'Max', 'Hamilton ',
                          graph=['speed', 'delta', 'throttle', 'DistanceToDriverAhead'])
plt.show()

"""
Max VSC stop gain
"""
# When the VSC was deloyed
HAM = laps.pick_driver('HAM')
HAM_VSC = HAM.TrackStatus.reset_index(drop=True)

drivers_list = ['VER']
ref_driver = 'HAM'
fig, ax = tt.plot_cumulative_time(laps, drivers_list, ref_driver)
comment_list = [['Checo is a legend', (19, -5), 5, 9, -20, (20, -10)],
                ['Max Chase - 23 laps younger hard tires', (44, -14.5), 22, 5, 20, (34, -22)],
                ['Max falling behind', (27, -4), 20, 4, -20, (37, -2)]]
ax = tt.annotation(ax, comment_list)
ax = tt.track_status(HAM_VSC, 'SC', ax, -26, 90)
ax = tt.track_status(HAM_VSC, 'VSC', ax, -26, 90)

# Normal stop
ax = tt.overlay_highlight(ax, -1, 11, 13)
l1 = np.array((12.25, -26))
ax.text(*l1, 'Normal stop', fontsize=12,
        rotation=90, rotation_mode='anchor', alpha=0.75)
plt.show()

# VSC stop
# Already highlighted

# Gain
# Manual analysis needed at this point


"""
Hard tire pushing and long term performance max vs ham
23L tire age differance
"""
# Time gained a lap with 23 laps younger tires

from path.source import track_telemetry as tt
from matplotlib import pyplot as plt


"""
Max mishap on an superbly quick lap in Saudi Arabia Quali - Max hit wall in last
turn forfeiting any chance on pole and damaging car
"""
#
# drivers = ['VER', 'HAM']
# laps, event = tt.crate_event(2021, 'SaudiArabia', 'Q')
#
# MAX = laps.pick_driver('VER').loc[18] # L18 is Final Lap Max Did in Q
# LEWIS = laps.pick_driver('HAM').pick_fastest()
#
# MAX['LapTime'] = LEWIS['LapTime'] #setting a dummy as Max had no time (NaT) this lap
#
# tt.overlay_laps(MAX, LEWIS, 'Max Mishap', 'Max Final Lap', 'Hamilton Fastest')
# tt.overlay_map_multi(drivers, laps, rotate = 1)

"""
Collision during race between Max and Lewis
L37
"""

laps2, event2 = tt.crate_event(2021, 'SaudiArabia', 'R')

CollisionLap = 37

MAX = laps2.pick_driver('VER')
MAX = MAX[MAX['LapNumber'] == CollisionLap].iloc[0]
HAM = laps2.pick_driver('HAM')
HAM = HAM[HAM['LapNumber'] == CollisionLap].iloc[0]

fig, ax = tt.overlay_laps_rework(MAX, HAM, 'Collision', 'Max ', 'Hamilton ',
            graph = ['speed', 'throttle', 'brake', 'longAcc'],
            start = 5000, end = 5600, highlight = [5420, 5470])
plt.show()


"""
Implement Time based overlay for laps - to show who braked first -- Is it really needed??
"""


"""
Overlay map with laps instead of driver list - with not finnished laps - Max in Q Saudi Arabia
"""


"""
Max Tire performance vs Lewis tire performance - Tire plus graph
"""

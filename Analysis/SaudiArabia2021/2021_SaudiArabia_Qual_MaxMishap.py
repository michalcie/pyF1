from path.source import track_telemetry as tt
from matplotlib import pyplot as plt


"""

"""
drivers = ['VER', 'HAM']
laps, event = tt.crate_event(2021, 'SaudiArabia', 'Q')
MAX = laps.pick_driver('VER').loc[18]
LEWIS = laps.pick_driver('HAM').pick_fastest()
MAX['LapTime'] = LEWIS['LapTime']
print(MAX.Driver) #NaT...
tt.overlay_laps(MAX, LEWIS, 'tit', 'lrg1', 'leg2')
tt.overlay_map_multi(drivers, laps, rotate = 1)

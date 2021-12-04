# from path.source import track_telemetry as tt
# from matplotlib import pyplot as plt
# import joypy
# import pandas as pd
# from fastf1 import plotting
# import fastf1 as ff1
# import numpy as np
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd

# Setup plotting
plotting.setup_mpl()

# Enable the cache
# ff1.Cache.enable_cache('../cache')

# Get rid of some pandas warnings that are not relevant for us at the moment
pd.options.mode.chained_assignment = None

# Load the session data

# race = ff1.get_session(2021, 'Monza', 'R')
# laps = race.load_laps(with_telemetry=True)


weekend = ff1.get_session(2021, 'Brazil')
weekend.data['raceName'] = "São Paulo Grand Prix"
session = ff1.core.Session(weekend, 'Race')
laps = session.load_laps(with_telemetry=True, livedata=None)


# Get laps of the drivers (BOT and HAM)
# laps_ric = laps.pick_driver('RIC')
# laps_ver = laps.pick_driver('VER')

laps_ric = laps.pick_driver('VER')
laps_ver = laps.pick_driver('HAM')

print(laps_ver['Stint'])
plt.plot(laps_ver['LapNumber'],laps_ver['Stint'])
# We are only analyzing stint 1, so select that one
Stint = 4
laps_ric = laps_ric.loc[laps_ric['Stint'] == Stint]
laps_ver = laps_ver.loc[laps_ver['Stint'] == Stint]



laps_ric['RaceLapNumber'] = laps_ric['LapNumber'] - 1
laps_ver['RaceLapNumber'] = laps_ver['LapNumber'] - 1

full_distance_ver_ric = pd.DataFrame()
summarized_distance_ver_ric = pd.DataFrame()

for lap in laps_ver.iterlaps():
    telemetry = lap[1].get_car_data().add_distance().add_driver_ahead()

    # Only run this loop when driver ahead is RIC, otherwise we compare wrong distance gaps
    telemetry = telemetry.loc[telemetry['DriverAhead'] == "3"]

    if len(telemetry) != 0:
        print('in telemetry')
        # Full distance
        lap_telemetry = telemetry[['Distance', 'DistanceToDriverAhead']]
        lap_telemetry.loc[:, 'Lap'] = lap[0] + 1

        full_distance_ver_ric = full_distance_ver_ric.append(lap_telemetry)

        # Average / median distance
        distance_mean = np.nanmean(telemetry['DistanceToDriverAhead'])
        distance_median = np.nanmedian(telemetry['DistanceToDriverAhead'])

        summarized_distance_ver_ric = summarized_distance_ver_ric.append({
            'Lap': lap[0] + 1,
            'Mean': distance_mean,
            'Median': distance_median
        }, ignore_index = True)

plt.rcParams['figure.figsize'] = [10, 6]

fig, ax = plt.subplots(2)
fig.suptitle("RIC vs VER opening stint comparison")

ax[0].plot(laps_ric['LapNumber'], laps_ric['LapTime'], label='RIC')
ax[0].plot(laps_ver['LapNumber'], laps_ver['LapTime'], label='VER')
ax[0].set(ylabel='Laptime', xlabel='Lap')
ax[0].legend(loc="upper center")

ax[1].plot(summarized_distance_ver_ric['Lap'], summarized_distance_ver_ric['Mean'], label='Mean', color='red')
ax[1].plot(summarized_distance_ver_ric['Lap'], summarized_distance_ver_ric['Median'], label='Median', color='grey')
ax[1].set(ylabel='Distance (meters)', xlabel='Lap')
ax[1].legend(loc="upper center")
# ax[1].plot(summarized_distance_ver_ric['Mean'], label='Mean', color='red')
# ax[1].plot(summarized_distance_ver_ric['Median'], label='Median', color='grey')
# ax[1].set(ylabel='Distance (meters)', xlabel='Lap')
# ax[1].legend(loc="upper center")

# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()

plt.show()

################################################

# """
# Brazil 2021
#
# """
#
# """
# Special workaround for Brazil GP
# """
# weekend = ff1.get_session(2021, 'Brazil')
# weekend.data['raceName'] = "São Paulo Grand Prix"
# session = ff1.core.Session(weekend, 'Race')
# laps = session.load_laps(with_telemetry=True, livedata=None)
#
# ver = laps.pick_driver('VER')
# ham = laps.pick_driver('HAM')
#
# ver['RaceLapNumber'] = ver['LapNumber'] - 1
# ham['RaceLapNumber'] = ham['LapNumber'] - 1
#
# # ver = ver.loc[ver['Stint'] == 1]
# # ham = ham.loc[ham['Stint'] == 1]
#
# full_distance = pd.DataFrame()
# sum_distance = pd.DataFrame()
#
# for lap in ver.iterlaps():
#     telemetry = lap[1].get_car_data().add_distance().add_driver_ahead()
#     telemetry = telemetry.loc[telemetry['DriverAhead'] == "44"]
#
#     if len(telemetry) != 0:
#
#         lap_telemetry = telemetry[['Distance', 'DistanceToDriverAhead']]
#         lap_telemetry.loc[:, 'Lap'] = lap[0] + 1
#
#         full_distance = full_distance.append(lap_telemetry)
#
#         distance_mean = np.nanmean(telemetry['DistanceToDriverAhead'])
#         distance_median = np.nanmedian(telemetry['DistanceToDriverAhead'])
#
#         sum_distance = sum_distance.append({
#             'Lap': lap[0] + 1,
#             'Mean': distance_mean,
#             'Median': distance_median
#         }, ignore_index = True)
#
# if len(telemetry) != 0:
#     plt.plot(sum_distance['Median'], 'b')

#
# for lap in ham.iterlaps():
#     telemetry = lap[1].get_car_data().add_distance().add_driver_ahead()
#     telemetry = telemetry.loc[telemetry['DriverAhead'] == "33"]
#
#     if len(telemetry) != 0:
#
#         lap_telemetry = telemetry[['Distance', 'DistanceToDriverAhead']]
#         lap_telemetry.loc[:, 'Lap'] = lap[0] + 1
#
#         full_distance = full_distance.append(lap_telemetry)
#
#         distance_mean = np.nanmean(telemetry['DistanceToDriverAhead'])
#         distance_median = np.nanmedian(telemetry['DistanceToDriverAhead'])
#
#         sum_distance = sum_distance.append({
#             'Lap': lap[0] + 1,
#             'Mean': distance_mean,
#             'Median': distance_median
#         }, ignore_index = True)
#
#
# if len(telemetry) != 0:
#     plt.plot(sum_distance['Median'], 'r')


plt.show()

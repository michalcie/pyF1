import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
import pandas as pd
from path.source import track_telemetry as tt


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


lap_ver = laps.pick_driver('VER')
lap_ham = laps.pick_driver('HAM')
#
# lap_ver = tt.data_list(['VER'], laps, 'all')


colision = 48
addition = 1
lap_ver_0 = lap_ver.loc[lap_ver['LapNumber'] == colision]
lap_ver_1 = lap_ver.loc[lap_ver['LapNumber'] == colision+addition]
lap_ham_0 = lap_ham.loc[lap_ham['LapNumber'] == colision]
lap_ham_1 = lap_ham.loc[lap_ham['LapNumber'] == colision+addition]
print(lap_ver['LapNumber'])

telemetry_ver_0 = lap_ver_0.get_car_data().add_distance()
telemetry_ver_1 = lap_ver_1.get_car_data().add_distance()
telemetry_ham_0 = lap_ham_0.get_car_data().add_distance()
telemetry_ham_1 = lap_ham_1.get_car_data().add_distance()



plt.plot(telemetry_ver_0['Distance'],telemetry_ver_0['Brake'], 'b')
plt.plot(telemetry_ver_1['Distance'],telemetry_ver_1['Brake'], 'b--')
plt.plot(telemetry_ham_0['Distance'],telemetry_ham_0['Brake'], 'r')
plt.plot(telemetry_ham_1['Distance'],telemetry_ham_1['Brake'], 'r--')
plt.show()

"""

"""
# fastest = 30
# tsunodad = 33
# fastest_slice = Ver_Q_laps[0].loc[fastest]
# tsunodad_slice = Ver_Q_laps[0].loc[tsunodad]

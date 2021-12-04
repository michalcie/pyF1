from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
import pandas as pd
from fastf1 import plotting
import numpy as np
import fastf1 as ff1
import numpy as np

"""
Brazil 2021
Hamilton disqualified from friday's qualifying session for DRS Infrigement - DRS opening more than allowed 85 mm
How much advantage is it? Can it be even seen? I have no idea, but can give a crack. Even though that the result may not my credible
"""

"""
Special workaround for Brazil GP
"""

weekend = ff1.get_session(2021, 'Brazil')
weekend.data['raceName'] = "São Paulo Grand Prix"
session = ff1.core.Session(weekend, 'Qualifying')
laps = session.load_laps(with_telemetry=True, livedata=None)


"""
Driver list to compare - Mercedes (Mercedes), Red Bull (Honda), Ferrari (Ferrari) and McLaren (Mercedes)
"""
drivers_list = [['HAM','BOT'],['VER','PER'],['SAI','LEC'],['NOR','RIC']]

"""
Using Speed Trap located at Start/Finish line and only fastest lap
"""

# for n in range(len(drivers_list)):
#     list = tt.data_list(drivers_list[n], laps, 'fastest')
#     spd = []
#     for i in range(len(list)):
#         spd.append(list[i]['SpeedFL'])
#         print(list[i]['Driver'], ': ', list[i]['SpeedFL'], 'km/h', ' ', list[i]['LapTime'])
#     print(np.diff(spd)[0])
# print(' ')

"""
Using multiple good laps from qualifying session with given threshold
Using same Speed Trap at the Start/Finish line and
Using telemetry data from same laps - maximum speed achieved during the lap taken into account
"""
for n in range(len(drivers_list)):
    list = tt.data_list(drivers_list[n], laps, 'all')
    spdFL = []
    meanFL = []
    spdT = []
    meanT = []
    for i in range(len(list)):
        spdFL.append(list[i].pick_accurate().pick_quicklaps(threshold=1.01)['SpeedFL'])
        meanFL.append(np.mean(spdFL))
        # print(list[i].iloc[0])
        telemetry_data = list[i].pick_accurate().pick_quicklaps(threshold=1.01)
        for j in range(len(telemetry_data)):
            spdT.append(telemetry_data.iloc[j].telemetry['Speed'].max())
            # print(spdT)
        meanT.append(np.mean(spdT))
        spdT = []
        spdFL = []
    print(list[0]['Team'].iloc[0])
    print('From Telemetry:     ',-np.round_(np.diff(meanT)[0], decimals = 2), 'km/h')
    print('From FL Speed Trap: ',-np.round_(np.diff(meanFL)[0], decimals=2), 'km/h')

"""
Seems that Hamilton gains more straight line speed than Bottas, but can it be due to setup? Hamilton is to take
5 grid places penalty, so it make sense to give him more speed to ease overtaking.
"""

"""
One more apprach is possible - How much more speed Hamilton gained using DRS compared to Bottas?
How much more compared to other cars Mercedes gains?
"""
list = tt.data_list(['HAM', 'BOT'], laps, 'fastest')
speeds = []
maxspeeds = []
for i in range(len(list)):
    print(list[i]['Driver'])
    drs_diff = list[i].telemetry['DRS'].diff()
    idx_on = drs_diff.index[drs_diff > 1]
    idx_off = drs_diff.index[drs_diff < -3]
    speed_on = list[i].telemetry['Speed'].loc[idx_on[0]-1]
    speed_off = list[i].telemetry['Speed'].loc[idx_off[1]-1]
    speed_diff = speed_off - speed_on
    speeds.append(speed_diff)
    maxspeeds.append(speed_off)
    print('Speed gained with DRS: ')
    print(speed_diff, 'km/h')
    print("Speed on DRS off:")
    print(speed_off, 'km/h')
    print(' ')

print('Gained Speed diffenace between drivers:',(np.diff(speeds)[0]), 'km/h')
print('Top Speed differance between drivers:', np.diff(maxspeeds)[0],'km/h')


"""
To me it seems that there is no significant differance.
And it is probably true as the gap measured was 85.2 mm
"""

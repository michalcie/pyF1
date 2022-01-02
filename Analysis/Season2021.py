from path.source import track_telemetry as tt
import logging

""" Disable logger messages from fastf1 """
logger = logging.getLogger()
logger.disabled = True

"""
Event list where Max and Lewis has finished
"""
# MAX and Lewis
# no 6, 10, 14 removed as DNF happened
event_list = [1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 22]
drvs_list = ['VER', 'HAM']

# MAX, LEWIS, BOTTAS
# event_list = [1,3,4,7,8,9,12,13,15,16,17,18,19,21,22]

# No DNFs deletion - all
# event_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]

# DEBUG
# event_list = [16,19]
#

# def calculate_from_telemetry(laps):
#     # time = None
#
#     time_cumsum = laps['LapTime'].fillna(laps['Time'] - laps['LapStartTime']).cumsum()
#     # print(time_cumsum.iloc[-1])
#     return time_cumsum.iloc[-1]
#
#
# def find_driver_by_code(drv, driver, laps):
#     time = None
#     try:
#         if drv['Driver']['code'] == driver:
#             time = pd.to_timedelta(float(drv['Time']['millis']), unit='ms')
#
#     except (ValueError, BaseException, OSError, NameError):
#         print(driver)
#         print('\t Data Error: Working around that')
#         driver_code = drv['Driver']['code']
#         drv_laps = laps.pick_driver(driver_code)
#         time = calculate_from_telemetry(drv_laps)
#     finally:
#         return time
#
#
# def season_total_time(drvs_list, event_list):
#     drvs_df = pd.DataFrame(drvs_list)
#     drvs_df = drvs_df.rename(columns={0: 'Driver'})
#     drvs_df['Cumsum'] = pd.Series(0)
#     drvs_df.set_index('Driver', inplace=True)
#
#     drvs_df = drvs_df.assign(Cumsum=pd.Timedelta("0 days"))
#
#     with alive_bar(len(event_list)) as bar:
#         for item in event_list:
#             # print(item)
#             laps, event = tt.crate_event(2021, item, 'R')
#             for drv in event.results:
#
#                 for name in drvs_df.iterrows():
#                     temp = find_driver_by_code(drv, name[0], laps)
#                     if temp is not None:
#                         drvs_df['Cumsum'][name[0]] = drvs_df['Cumsum'][name[0]] + temp
#             bar()
#
#     print('#######################')
#     print(drvs_df)
#     drvs_df = drvs_df.sort_values('Cumsum')
#     drvs_diff_df = drvs_df.sort_values('Cumsum').diff()
#     print(drvs_diff_df)
#     print(' ')
#     print('Percentage differance P1-P2:')
#     print(round(float((drvs_diff_df.iloc[1] / drvs_df.iloc[0]) * 100), 3), '%')

tt.season_total_time(drvs_list, event_list)

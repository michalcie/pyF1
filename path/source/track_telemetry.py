import fastf1 as ff1
import numpy as np
import pandas as pd
from fastf1 import plotting
from fastf1 import utils
from matplotlib import pyplot as plt
from scipy import interpolate
import os
plt.style.use('dark_background')

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'cache')
print(filename)
# ff1.utils.enable_cache(
#     r'C:\Users\Dell\PycharmProjects\pyF1_Analysis\path\to\folder\for\cache')  # optional but recommended
ff1.api.Cache.enable_cache(filename)

def crate_event(year, gp, session):
    quali = ff1.get_session(year, gp, session)
    laps = quali.load_laps(with_telemetry=True, livedata=None)

    return laps


def overlay_drv(drv1, drv2):
    fig, ax = plt.subplots(2)
    fig.canvas.set_window_title("".join(('Driver overlay: ', drv1.Driver, ' vs ', drv2.Driver)))
    fig.suptitle("".join((drv1.Driver, ' vs. ', drv2.Driver)))
    ax[0].plot(drv1.telemetry['Distance'], drv1.telemetry['Speed'],
               color=plotting.TEAM_COLORS[drv1['Team']],
               label="".join((drv1.Driver, ' ', str(drv1.LapTime).split(':', 1)[1][:-3])))
    ax[0].plot(drv2.telemetry['Distance'], drv2.telemetry['Speed'],
               color=plotting.TEAM_COLORS[drv2['Team']],
               label="".join((drv2.Driver, ' ', str(drv2.LapTime).split(':', 1)[1][:-3])))
    legend_x = 1.1
    legend_y = 0.75
    ax[0].legend(loc='upper center',
                 bbox_to_anchor=(0.83, 0.15),
                 shadow=False,
                 ncol=2)
    ax[0].set_xlabel('Lap Distance [m]')
    ax[0].set_ylabel('Velocity [kmh]')
    delta,ref_tel,dump2 = utils.delta_time(drv2, drv1)
    ax[1].plot(ref_tel['Distance'], delta,
               '--', color=plotting.TEAM_COLORS[drv1['Team']])
    ax[1].set_xlabel('Lap Distance [m]')
    ax[1].set_ylabel("".join(('Relative time delta\n(', drv1.Driver, ' to ', drv2.Driver, ')')))
    plt.show()


def overlay_drivers(driver_list, session):
    drvs = data_list(driver_list, session, 'fastest')
    driver1 = drvs[0]
    driver2 = drvs[1]
    overlay_drv(driver1, driver2)
    # plt.show()
    # return driver1, driver2


def index(drv):
    index0 = drv.telemetry['Distance'].index[0]
    space0 = drv.telemetry['Distance'].loc[index0]
    index_end = drv.telemetry['Distance'].index[-1]
    space_end = drv.telemetry['Distance'].loc[index_end]

    return index0, index_end, space0, space_end


def spln(drv, idx0, idxe, name1, name2):
    x = drv.telemetry[name1].loc[idx0:idxe]
    y = drv.telemetry[name2].loc[idx0:idxe]
    lookup = interpolate.InterpolatedUnivariateSpline(x, y, k=1)
    return lookup


def index_multi(drvs):
    size = len(drvs)
    output = np.empty((2, size))
    for i in range(size):
        output[0][i] = drvs[i].telemetry['Distance'].index[0]
        output[1][i] = drvs[i].telemetry['Distance'].index[-1]
    idx = pd.DataFrame({'Index zero': output[0][:],
                        'Index omega': output[1][:]},
                       index=[drvs[value].Driver for value in range(size)])
    return idx


def data_list(driver_list, laps, type):
    size = len(driver_list)
    if type == 'fastest':
        drvs = [laps.pick_driver(driver_list[i]).pick_fastest() for i in range(size)]
    elif type == 'all':
        drvs = [laps.pick_driver(driver_list[i]) for i in range(size)]
    return drvs


def multi_spline(drvs, idx):
    size = len(drvs)
    output = [[None] * size for j in range(3)]

    for i in range(size):
        output[0][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver], 'Distance',
                            'Time')
        output[1][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver], 'Distance',
                            'X')
        output[2][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver], 'Distance',
                            'Y')
    splns = pd.DataFrame({'Space/Time': output[0][:],
                          'Space/X': output[1][:],
                          'Space/Y': output[2][:]},
                         index=[drvs[value].Driver for value in range(size)])
    return splns


# noinspection PyUnboundLocalVariable
def segment_times(splines, segments, drvs):
    sgn_len = len(segments)

    for i in range(len(splines)):
        if i == 0:
            temp = pd.to_timedelta(np.diff(splines['Space/Time'][drvs[i].Driver](segments)))
            output = pd.DataFrame([temp], columns=list(i + 1 for i in range(sgn_len - 1)), index=[drvs[i].Driver])
        elif i > 0:
            temp = pd.to_timedelta(np.diff(splines['Space/Time'][drvs[i].Driver](segments)))
            temp_df = pd.DataFrame([temp], columns=list(i + 1 for i in range(sgn_len - 1)), index=[drvs[i].Driver])
            output = output.append(temp_df)
    return output


def fastest_segments(segments):
    output = [None] * segments.shape[1]
    for i in range(segments.shape[1]):
        output[i] = segments[[i + 1]].idxmin().to_string()[-3:]

    return output


def plot_limits(drvs, idx):
    limit_min = min(drvs[0].telemetry['X'].loc[idx['Index zero'][drvs[0].Driver]:idx['Index omega'][drvs[0].Driver]])
    limit_max = max(drvs[0].telemetry['X'].loc[idx['Index zero'][drvs[0].Driver]:idx['Index omega'][drvs[0].Driver]])

    for i in range(len(drvs)):
        temp_min = min(
            drvs[i].telemetry['X'].loc[idx['Index zero'][drvs[i].Driver]:idx['Index omega'][drvs[i].Driver]].min(),
            drvs[i].telemetry['Y'].loc[idx['Index zero'][drvs[i].Driver]:idx['Index omega'][drvs[i].Driver]].min())
        temp_max = max(
            drvs[i].telemetry['X'].loc[idx['Index zero'][drvs[i].Driver]:idx['Index omega'][drvs[i].Driver]].min(),
            drvs[i].telemetry['Y'].loc[idx['Index zero'][drvs[i].Driver]:idx['Index omega'][drvs[i].Driver]].min())
        if temp_min < limit_min:
            limit_min = temp_min
        if temp_max > limit_max:
            limit_max = temp_max

    return [limit_min, limit_max]


def search(name, drvs):
    output = [element['Team'] for element in drvs if element['Driver'] == name]
    return output[0]


def overlay_map_plot(drvs, segments, time_differance, splines):
    sector_point = np.ceil(1100 / len(segments))
    fig, ax = plt.subplots()
    fig.canvas.set_window_title("".join('Fastest mini sectors'))

    for i in range(len(segments) - 1):
        distance = [value for value in (np.arange(segments[i], segments[i + 1], sector_point))]
        X = splines['Space/X'][time_differance[i]](distance)
        Y = splines['Space/Y'][time_differance[i]](distance)
        ax.plot(X, Y, color=plotting.TEAM_COLORS[search(time_differance[i], drvs)])
    ax.axes.set_aspect('equal')
    plt.show()


def overlay_map_multi(driver_list, session):
    sectors = 100
    sector_point = np.ceil(1100 / sectors)

    drvs = data_list(driver_list, session, 'fastest')
    idx = index_multi(drvs)
    splines = multi_spline(drvs, idx)
    track_length = max([drvs[i].telemetry['Distance'].loc[idx['Index omega'][drvs[i].Driver]] for i in range(len(drvs))])
    segments = [value for value in track_length * (np.arange(sectors + 1)) / sectors]
    segments_time = segment_times(splines, segments, drvs)
    time_differance = fastest_segments(segments_time)
    limits = plot_limits(drvs, idx)
    overlay_map_plot(drvs, segments, time_differance, splines)


def tire_comparison():

    return 0


def race_tire_comparison():

    return 0


def quali_tire_comparison():

    return 0


def tire_degradation():

    return 0


def plot_tire_data():

    return 0


def plot_driver_tire_data(driver_list, laps):
    drvs = data_list(driver_list, laps, 'all')
    # hard = drvs[0].loc[np.logical_and(drvs[0]['Compound'] == 'HARD', drvs[0]['IsAccurate'] == True)]
    # medium = drvs[0].loc[np.logical_and(drvs[0]['Compound'] == 'MEDIUM', drvs[0]['IsAccurate'] == True)]
    # soft = drvs[0].loc[np.logical_and(drvs[0]['Compound'] == 'SOFT', drvs[0]['IsAccurate'] == True)]
    # print(max(pd.unique(drvs[0]['Stint'])))
    fig, ax = plt.subplots(2)
    # print(np.unique(drvs[0]['Stint']))
    for i in range(max(pd.unique(drvs[0]['Stint']))):
        current_stint = drvs[0].loc[np.logical_and(drvs[0]['Stint'] == i+1, drvs[0]['IsAccurate'] == True)].pick_quicklaps(threshold=1.07)
        if not current_stint.empty:
            # print(i+1)
            # print(min(current_stint['TyreLife']))
            # print(max(current_stint['TyreLife']))
            times = current_stint['LapTime'].dt.total_seconds()
            # print(np.logical_and(current_stint['Compound'] == 'SOFT', 1).all())
            if np.logical_and(current_stint['Compound'] == 'SOFT', 1).all():
                color = 'r'
            elif np.logical_and(current_stint['Compound'] == 'MEDIUM', 1).all():
                color = 'y'
            elif np.logical_and(current_stint['Compound'] == 'HARD', 1).all():
                color = 'w'

            ax[0].plot(current_stint['TyreLife'], times, '.', color=color)
            lookup = np.polyfit(current_stint['TyreLife'], times,2)
            x = np.linspace(min(current_stint['TyreLife']), max(current_stint['TyreLife']),100)
            lookup = np.poly1d(lookup)
            y = lookup(x)
            ax[0].plot(x,y,'-',color=color)

            ax[1].plot(current_stint['LapNumber'], times, '.', color=color)
            lookup = np.polyfit(current_stint['LapNumber'], times,2)
            x = np.linspace(min(current_stint['LapNumber']), max(current_stint['LapNumber']),100)
            lookup = np.poly1d(lookup)
            y = lookup(x)
            ax[1].plot(x,y,'-',color=color)

    plt.draw()

    # times = soft['LapTime'].dt.total_seconds()
    # plt.plot(soft['TyreLife'], times, '.')
    # lookup = np.polyfit(soft['TyreLife'], times,2)
    # x = np.linspace(min(soft['TyreLife']), max(soft['LapNumber']),100)
    # lookup = np.poly1d(lookup)
    # y = lookup(x)
    # plt.plot(x,y)
    # plt.show()


    return 0

def session_plot(driver_list, laps):
    fig, ax = plt.subplots()
    drvs = data_list(driver_list, laps, 'all')
    y = drvs[0].loc[drvs[0]['IsAccurate'] == True]
    ax.plot(y['LapNumber'], y['LapTime'].dt.total_seconds())

    lookup = np.polyfit(y['LapNumber'], y['LapTime'].dt.total_seconds(),2)
    x = np.linspace(min(y['LapNumber']), max(y['LapNumber']),100)
    lookup = np.poly1d(lookup)
    y = lookup(x)
    ax.plot(x,y)
    plt.show()

def tire_data():

    return 0


def tire_by_lap(session):
    fig, ax = plt.subplots(2)

    medians = []
    i = 0
    for element in ["SOFT", "MEDIUM", "HARD"]:
        tyre = session.pick_tyre(element).pick_accurate().pick_quicklaps(threshold=1.05)
        x = tyre["LapNumber"]
        y = tyre["LapTime"].dt.total_seconds()
        y_avg = pd.to_numeric(tyre['LapTime'].dt.total_seconds()).groupby(tyre['LapNumber'])
        y_avg = y_avg.mean().to_frame().reset_index(level = 0)

        if element == "SOFT":
            color = 'r'
            soft = y_avg.set_index('LapNumber')
            tire_idx = 1

        elif element == "MEDIUM":
            color = 'y'
            medium = y_avg.set_index('LapNumber')
            tire_idx = 2

        elif element == "HARD":
            color = 'w'
            hard = y_avg.set_index('LapNumber')
            tire_idx = 3

        ax[0].plot(x,y, '.',color = color, alpha = 0.5)
        ax[0].plot(y_avg["LapNumber"], y_avg["LapTime"], 'o', color = color, alpha = 0.9)

        ax[1].plot(np.random.normal(tire_idx, 0.04, size=len(y)), y, 'o', color = color, alpha = 0.5)
        bp = ax[1].boxplot(y, positions = [tire_idx])
        medians.append(max(bp['medians'][0].get_ydata()))
        ax[1].set_xticks([1,2,3], minor=False)
        ax[1].set_xticklabels(['SOFT','MEDIUM','HARD'], fontdict=None, minor=False)
        i = i + 1

    xline = np.linspace(0.8, 3.2, 50)
    lookup = np.polyfit([1,2,3], medians, 1)
    lookup = np.poly1d(lookup)
    yline = lookup(xline)
    ax[1].plot(xline, yline, 'g', linewidth = 1)


    sof_med = medium - soft
    med_har = hard - medium
    sof_har = hard - soft

    sof_med_avg = sof_med.median()
    med_har_avg = med_har.median()
    sof_har_avg = sof_har.median()

    # isofuel delta - created from upper plot data
    print('Soft - Medium delta:')
    print(round(sof_med_avg["LapTime"], 3))
    print('Medium - Hard delta:')
    print(round(med_har_avg["LapTime"], 3))
    print('Soft - Hard delta:')
    print(round(sof_har_avg["LapTime"], 3))

    plt.grid(which = 'both')
    plt.show()


    # for :
    #     x = softs["LapNumber"]
    #     y = softs["LapTime"].dt.total_seconds()
    #     y_avg = pd.to_numeric(softs['LapTime'].dt.total_seconds()).groupby(softs['LapNumber'])
    #     y_avg = y_avg.mean().to_frame().reset_index(level = 0)
    #     ax.plot(x,y,'r.', alpha = 0.5)
    #     ax.plot(y_avg["LapNumber"], y_avg["LapTime"],'ro', alpha = 1)
    #
    #
    # plt.show()

    return 0


# def driver_tire_data(driver_list, laps):
#     drvs = data_list(driver_list, laps, 'all')
#     print(drvs[0]['Compound'])
#     return 0

# def ten_best(driver_list, session):
#     drvs = data_list(driver_list, session, 'all')
#     for i in range(len(drvs)):
#         print(drvs[i].Driver, ' Lap Time:\n', drvs[i].LapTime)
#
#     return 1

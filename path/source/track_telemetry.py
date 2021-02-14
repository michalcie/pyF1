import fastf1 as ff1
import numpy as np
import pandas as pd
from fastf1 import plotting
from fastf1 import utils
from matplotlib import pyplot as plt
from scipy import interpolate

ff1.utils.enable_cache(
    r'C:\Users\Dell\PycharmProjects\pyF1_Analysis\path\to\folder\for\cache')  # optional but recommended


def crate_event(year, gp, session):
    quali = ff1.get_session(year, gp, session)
    laps = quali.load_laps()

    return laps


def overlay_drv(drv1, drv2):
    fig, ax = plt.subplots(2)
    fig.canvas.set_window_title("".join(('Driver overlay: ', drv1.Driver, ' vs ', drv2.Driver)))
    fig.suptitle("".join((drv1.Driver, ' vs. ', drv2.Driver)))
    ax[0].plot(drv1.telemetry['Space'], drv1.telemetry['Speed'],
               color=plotting.TEAM_COLORS[drv1['Team']],
               label="".join((drv1.Driver, ' ', str(drv1.LapTime).split(':', 1)[1][:-3])))
    ax[0].plot(drv2.telemetry['Space'], drv2.telemetry['Speed'],
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
    ax[1].plot(drv2.telemetry['Space'], utils.delta_time(drv2, drv1),
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
    index0 = drv.telemetry['Space'].index[0]
    space0 = drv.telemetry['Space'].loc[index0]
    index_end = drv.telemetry['Space'].index[-1]
    space_end = drv.telemetry['Space'].loc[index_end]

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
        output[0][i] = drvs[i].telemetry['Space'].index[0]
        output[1][i] = drvs[i].telemetry['Space'].index[-1]
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
        output[0][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver], 'Space',
                            'Time')
        output[1][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver], 'Space',
                            'X')
        output[2][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver], 'Space',
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
    track_length = max([drvs[i].telemetry['Space'].loc[idx['Index omega'][drvs[i].Driver]] for i in range(len(drvs))])
    segments = [value for value in track_length * (np.arange(sectors + 1)) / sectors]
    segments_time = segment_times(splines, segments, drvs)
    time_differance = fastest_segments(segments_time)
    limits = plot_limits(drvs, idx)
    overlay_map_plot(drvs, segments, time_differance, splines)


def ten_best(driver_list, session):
    drvs = data_list(driver_list, session, 'all')
    for i in range(len(drvs)):
        print(drvs[i].Driver, ' Lap Time:\n', drvs[i].LapTime)

    return 1

# overlay_drivers(['VER', 'HAM'])
# overlay_map_multi(['VER', 'HAM', 'LEC'])
# plt.show()
# ff1.utils.clear_cache()

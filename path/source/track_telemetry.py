import fastf1 as ff1
import numpy as np
import pandas as pd
from fastf1 import plotting
from fastf1 import utils
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse
import matplotlib.ticker as mticker
from scipy import interpolate
import os
import joypy
from alive_progress import alive_bar

plt.style.use('dark_background')

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'cache')
print(filename)
ff1.api.Cache.enable_cache(filename)


def crate_event(year, gp, session):
    ### Description:
    ### input:
    ### output:
    event = ff1.get_session(year, gp, session)
    # print(event.name)
    print(event.weekend.name)
    laps = event.load_laps(with_telemetry=True, livedata=None)

    return laps, event


def ridgeline(drivers_list, laps, title, xliml, xlimr, best_lap_number):
    def find_nearest(array, values):
        ### Description:
        ### input:
        ### output:
        indices = np.abs(np.subtract.outer(array, values[0])).argmin(0)
        return indices

    def statistics(ax, values, color, alpha):
        ### Description:
        ### input:
        ### output:
        for i in range(len(values)):
            y_min = 0
            y_max_med = ax[i].lines[1].get_ydata()
            x_data = ax[i].lines[1].get_xdata()
            ind = find_nearest(x_data, values[i])
            y_max = y_max_med[ind]
            ax[i].set_axisbelow(False)
            ax[i].plot([values[i][0], values[i][0]], [y_min, y_max], c=color, alpha=alpha, zorder=200)

    """Driver list"""
    driver_list = data_list(drivers_list, laps, 'all')

    """
    Preparing data, and creating ridgeline plots
    """
    c = []
    median = []
    mean = []
    q25 = []
    q75 = []
    for i in range(len(driver_list)):
        if i == 0:
            df = driver_list[i].pick_accurate().sort_values(by='LapTime').reset_index(drop=True)
            df = df[['LapTime']]
            df = pd.DataFrame(data=df.rename(columns={'LapTime': driver_list[i].Driver.iloc[0]})[
                driver_list[i].Driver.iloc[0]].dt.total_seconds())
            df_temp = df
        if i != 0:
            df_temp = driver_list[i].pick_accurate().sort_values(by='LapTime').reset_index(drop=True)
            df_temp = df_temp[['LapTime']]
            df_temp = pd.DataFrame(data=df_temp.rename(columns={'LapTime': driver_list[i].Driver.iloc[0]})[
                driver_list[i].Driver.iloc[0]].dt.total_seconds())

            df = df.join(df_temp)

            """
            Some statistical insight might be useful
            """

        c.append(plotting.team_color(driver_list[i]['Team'].iloc[0]))
        median.append(df_temp.median(axis=0))
        mean.append(df_temp.mean(axis=0))
        q25.append(df_temp.quantile(q=0.25, axis=0, numeric_only=True))
        q75.append(df_temp.quantile(q=0.75, axis=0, numeric_only=True))

    """
    Let's finally plot graph
    """
    # print(c)
    fig, ax = joypy.joyplot(df, overlap=0.9, color=c, linecolor='w', linewidth=.5, alpha=1, title=title,
                            figsize=(11.5, 7))
    fig.canvas.set_window_title("".join(('Ridgeline plot: ', title)))
    # fig.suptitle("".join((title)))

    """
    Adding some statistical data for nerds, let's also set better x axis limits
    """
    statistics(ax, median, 'r', 1)
    statistics(ax, mean, 'k', 0.6)
    statistics(ax, q25, 'k', 0.3)
    statistics(ax, q75, 'k', 0.3)
    for i in range(len(ax)):
        ax[i].set_xlim(left=xliml, right=xlimr)
    """
    Printing out statistical data for some additional insight
    """
    print("Median: ")
    print(median)
    print("Average: ")
    print(mean)
    print("Quantile 25: ")
    print(q25)
    print("Quantile 75: ")
    print(q75)
    plt.show()


def overlay_drivers(driver_list, session):
    ### Description:
    ### input:
    ### output:
    drvs = data_list(driver_list, session, 'fastest')
    driver1 = drvs[0]
    driver2 = drvs[1]
    fig, ax = overlay_laps(driver1, driver2, "title", driver1.Driver, driver2.Driver)
    # overlay_drv(driver1, driver2)
    # plt.show()
    # return driver1, driver2
    return fig, ax


def overlay_highlight(ax, axes_counter, xlim, xlim2, **kwargs):
    ### Description: plots a highlighted area on a graph
    ### input: xlim, xlim3: <'float'> - highlight limit
    ###         ax: <'Matplotlib Axes'>, axes_counter: <'int'>
    ### output: ax: <'Matplotlib Axes'>

    if 'color' in kwargs:
        color = kwargs['color']
    else:
        color = 'g'

    if axes_counter != -1:
        ax[axes_counter].axvspan(xlim, xlim2, facecolor=color, alpha=0.5)
    if axes_counter == -1:
        ax.axvspan(xlim, xlim2, facecolor=color, alpha=0.5)
    return ax


def overlay_laps(lap1, lap2, title, legl1, legl2, **kwargs):
    ### Description:
    ###     Single lap telemetry overlay of 2 drivers
    ###     Speed, time and so on in distance
    ### input:
    ###     lap1, lap2: <class 'fastf1.core.Lap'>
    ###     title, legl, legl2:  <'string'>
    ### output:
    ###     matplotlib fig, ax
    ###     plt.show() needed to show graphs
    major_base = 20
    minor_base = 5


    def timeTicksMajor(x, pos):
        hours = int(x // 3600)
        minutes = int((x % 3600) // 60)
        seconds = int(x % 60)
        if timeMode == 'Time':
            return "{:02d}:{:02d}".format(minutes, seconds)
        elif timeMode == 'SessionTime':
            return "{:01d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        else:
            return "{:01d}:{:02d}:{:02d}".format(hours, minutes, seconds)


    def timeTicksMinor(x, pos):
        hours = int(x // 3600)
        minutes = int((x % 3600) // 60)
        seconds = int(x % 60)

        return ":{:02d}".format(seconds)

    def plot_overlay_axes(ax, axes_counter, lap, graph):
        ### Description: plots data given in 'graph' from 'lap' in 'ax' Axes
        ### input:
        ### output:
        nonlocal time_mode

        if not time_mode:
            ax[axes_counter].plot(lap.telemetry['Distance'], lap.telemetry[graph],
                                  color=plotting.team_color(lap['Team']),
                                  label="".join((lap.Driver, ' ', str(lap.LapTime).split(':', 1)[1][:-3])))
        if time_mode:
            if timeMode == 'Time' or timeMode == 'Session':
                ax[axes_counter].plot(lap.telemetry[timeMode].dt.total_seconds(), lap.telemetry[graph],
                                      color=plotting.team_color(lap['Team']),
                                      label="".join((lap.Driver, ' ', str(lap.LapTime).split(':', 1)[1][:-3])))
            elif timeMode == 'Date':
                day = pd.Timestamp(year=lap.telemetry['Date'].iloc[0].year,
                                   month=lap.telemetry['Date'].iloc[0].month,
                                   day=lap.telemetry['Date'].iloc[0].day, hour=0, minute=0, second=0)
                time_axis = (lap.telemetry['Date'] - day).dt.total_seconds()
                ax[axes_counter].plot(time_axis, lap.telemetry[graph],
                                      color=plotting.team_color(lap['Team']),
                                      label="".join((lap.Driver, ' ', str(lap.LapTime).split(':', 1)[1][:-3])))

            formatter_major = mticker.FuncFormatter(timeTicksMajor)
            formatter_minor = mticker.FuncFormatter(timeTicksMinor)
            ax[axes_counter].xaxis.set_major_formatter(formatter_major)
            ax[axes_counter].xaxis.set_minor_formatter(formatter_minor)
            ax[axes_counter].xaxis.set_major_locator(mticker.MultipleLocator(base=major_base))
            ax[axes_counter].xaxis.set_minor_locator(mticker.MultipleLocator(base=minor_base))
        return ax

    def plot_overlay_axes_settings(ax, axes_counter, xlabel, ylabel, xlim, xlim2):
        ### Description: Apply setting to selected axes
        ### input:
        ### output:
        ax[axes_counter].set_xlim([xlim, xlim2])
        ax[axes_counter].set_xlabel(xlabel)
        ax[axes_counter].set_ylabel(ylabel)
        ax[axes_counter].grid(which='both', axis='both', linestyle='--', linewidth=0.5, color='#77773c')

        return ax

    # fig, ax = plt.subplots(len(kwargs['graph']))
    if 'start' in kwargs:
        start_distance = kwargs['start']
    else:
        start_distance = None

    if 'mode' in kwargs:

        if kwargs['mode'] == 'time':
            time_mode = True
        else:
            time_mode = False

        if 'timeMode' in kwargs:
            if kwargs['timeMode'] == 'Time':
                timeMode = 'Time'

            elif kwargs['timeMode'] == 'SessionTime':
                timeMode = 'SessionTime'

            elif kwargs['timeMode'] == 'Date':
                timeMode = 'Date'

            else:
                timeMode = 'Time'

        else:
            timeMode = 'Time'

    else:
        time_mode = False

    if 'end' in kwargs:
        end_distance = kwargs['end']
    else:
        end_distance = None

    if 'highlight' in kwargs:
        highlight_start = kwargs['highlight'][0]
        highlight_end = kwargs['highlight'][1]
    else:
        highlight_start = None
        highlight_end = None

    if 'graph' in kwargs:

        # main function
        ratios = [1] * len(kwargs['graph'])
        ratios[0] = 2
        fig, ax = plt.subplots(nrows=len(kwargs['graph']), ncols=1, gridspec_kw={'height_ratios': ratios})
        fig.canvas.set_window_title("".join((title, ' ', legl1, ' vs ', legl2)))
        fig.suptitle("".join((legl1, ' vs. ', legl2)))
        fig.set_size_inches(11.5, 7)
        axes_counter = 0

        if 'speed' in kwargs['graph']:
            ax = plot_overlay_axes(ax, axes_counter, lap1, 'Speed')
            ax = plot_overlay_axes(ax, axes_counter, lap2, 'Speed')
            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            'Velocity [kmh]', start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            ax[axes_counter].legend(loc='upper center',
                                    bbox_to_anchor=(0.8, 0.15),
                                    shadow=False,
                                    ncol=2)
            axes_counter = axes_counter + 1

        if 'delta' in kwargs['graph']:
            delta, ref_tel, dump2 = utils.delta_time(lap2, lap1)

            if not time_mode:
                ax[axes_counter].plot(ref_tel['Distance'], delta,
                                      '--', color=plotting.team_color(lap1['Team']))
            elif time_mode:
                if timeMode == 'Time' or timeMode == 'SessionTime':
                    ax[axes_counter].plot(ref_tel[timeMode].dt.total_seconds(), delta,
                                          '--', color=plotting.team_color(lap1['Team']))

                elif timeMode == 'Date':
                    day = pd.Timestamp(year=ref_tel['Date'].iloc[0].year,
                                       month=ref_tel['Date'].iloc[0].month,
                                       day=ref_tel['Date'].iloc[0].day, hour=0, minute=0, second=0)
                    time_axis = (ref_tel['Date'] - day).dt.total_seconds()
                    ax[axes_counter].plot(time_axis, delta,
                                          '--', color=plotting.team_color(lap1['Team']))
                formatter_major = mticker.FuncFormatter(timeTicksMajor)
                formatter_minor = mticker.FuncFormatter(timeTicksMinor)
                ax[axes_counter].xaxis.set_major_formatter(formatter_major)
                ax[axes_counter].xaxis.set_minor_formatter(formatter_minor)
                ax[axes_counter].xaxis.set_major_locator(mticker.MultipleLocator(base=major_base))
                ax[axes_counter].xaxis.set_minor_locator(mticker.MultipleLocator(base=minor_base))

            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            "".join(('Relative time delta\n(', lap1.Driver,
                                                     ' to ', lap2.Driver, ')')), start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            axes_counter = axes_counter + 1

        if 'throttle' in kwargs['graph']:
            ax = plot_overlay_axes(ax, axes_counter, lap1, 'Throttle')
            ax = plot_overlay_axes(ax, axes_counter, lap2, 'Throttle')
            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            'Throttle [%]', start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            axes_counter = axes_counter + 1

        if 'brake' in kwargs['graph']:
            ax = plot_overlay_axes(ax, axes_counter, lap1, 'Brake')
            ax = plot_overlay_axes(ax, axes_counter, lap2, 'Brake')
            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            'Brake [%]', start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            axes_counter = axes_counter + 1

        if 'DistanceToDriverAhead' in kwargs['graph']:
            ax = plot_overlay_axes(ax, axes_counter, lap1, 'DistanceToDriverAhead')
            ax = plot_overlay_axes(ax, axes_counter, lap2, 'DistanceToDriverAhead')
            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            'DistanceToDriverAhead [m]', start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            axes_counter = axes_counter + 1

        # Not maintained since 0.3.1
        if 'longAcc' in kwargs['graph']:
            Y = lap1.get_telemetry()['Speed'].diff() / 3.6 / lap1.get_telemetry()['Time'].dt.total_seconds().diff()
            ax[axes_counter].plot(lap1.get_telemetry()['Distance'], (Y / 9.81).rolling(5, min_periods=1).mean(),
                                  color=plotting.team_color(lap1['Team']),
                                  label="".join((lap1.Driver, ' ', str(lap1.LapTime).split(':', 1)[1][:-3])))

            Y = lap2.get_telemetry()['Speed'].diff() / 3.6 / lap2.get_telemetry()['Time'].dt.total_seconds().diff()
            ax[axes_counter].plot(lap2.get_telemetry()['Distance'], (Y / 9.81).rolling(5, min_periods=1).mean(),
                                  color=plotting.team_color(lap2['Team']),
                                  label="".join((lap2.Driver, ' ', str(lap2.LapTime).split(':', 1)[1][:-3])))

            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            'Long Acc [G]', start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            axes_counter = axes_counter + 1

        if 'gear' in kwargs['graph']:
            ax = plot_overlay_axes(ax, axes_counter, lap1, 'nGear')
            ax = plot_overlay_axes(ax, axes_counter, lap2, 'nGear')
            ax = plot_overlay_axes_settings(ax, axes_counter, 'Lap Distance [m]',
                                            'Gear', start_distance, end_distance)
            ax = overlay_highlight(ax, axes_counter, highlight_start, highlight_end)
            axes_counter = axes_counter + 1
    else:
        # default plots - ensures backwards compatibility
        fig, ax = plt.subplots(nrows=2, ncols=1, gridspec_kw={'height_ratios': [2, 1]})
        fig.canvas.set_window_title("".join(('Driver overlay: Hot Lap: ', legl1, ' vs ', legl2)))
        fig.suptitle("".join((legl1, ' vs. ', legl2)))
        fig.set_size_inches(11.5, 7)
        ax = plot_overlay_axes(ax, 0, lap1, 'Speed')
        ax = plot_overlay_axes(ax, 0, lap2, 'Speed')
        ax = plot_overlay_axes_settings(ax, 0, 'Lap Distance [m]',
                                        'Velocity [kmh]', start_distance, end_distance)
        ax = overlay_highlight(ax, 0, highlight_start, highlight_end)
        ax[0].legend(loc='upper center',
                     bbox_to_anchor=(0.8, 0.15),
                     shadow=False,
                     ncol=2)

        delta, ref_tel, dump2 = utils.delta_time(lap2, lap1)
        ax[1].plot(ref_tel['Distance'], delta,
                   '--', color=plotting.team_color(lap1['Team']))

        ax = plot_overlay_axes_settings(ax, 1, 'Lap Distance [m]',
                                        "".join(('Relative time delta\n(', lap1.Driver,
                                                 ' to ', lap2.Driver, ')')), start_distance, end_distance)
        ax = overlay_highlight(ax, 1, highlight_start, highlight_end)

    return fig, ax


def index(drv):
    ### Description:
    ### input:
    ### output:
    index0 = drv.telemetry['Distance'].index[0]
    space0 = drv.telemetry['Distance'].loc[index0]
    index_end = drv.telemetry['Distance'].index[-1]
    space_end = drv.telemetry['Distance'].loc[index_end]

    return index0, index_end, space0, space_end


def data_list(driver_list, laps, type):
    ### Description:
    ### input:
    ### output:
    size = len(driver_list)
    if type == 'fastest':
        drvs = [laps.pick_driver(driver_list[i]).pick_fastest() for i in range(size)]
    elif type == 'all':
        drvs = [laps.pick_driver(driver_list[i]) for i in range(size)]
    return drvs


def overlay_map_multi(driver_list, session, **kwargs):
    ### Description:
    ### input:
    ### output:
    def spln(drv, idx0, idxe, name1, name2):
        ### Description:
        ### input:
        ### output:
        x = drv.telemetry[name1].loc[idx0:idxe]
        y = drv.telemetry[name2].loc[idx0:idxe]
        lookup = interpolate.InterpolatedUnivariateSpline(x, y, k=1)
        return lookup

    def index_multi(drvs):
        ### Description:
        ### input:
        ### output:
        size = len(drvs)
        output = np.empty((2, size))
        for i in range(size):
            output[0][i] = drvs[i].telemetry['Distance'].index[0]
            output[1][i] = drvs[i].telemetry['Distance'].index[-1]
        idx = pd.DataFrame({'Index zero': output[0][:],
                            'Index omega': output[1][:]},
                           index=[drvs[value].Driver for value in range(size)])
        return idx

    def multi_spline(drvs, idx):
        ### Description:
        ### input:
        ### output:
        size = len(drvs)
        output = [[None] * size for j in range(3)]

        for i in range(size):
            # noinspection PyTypeChecker
            output[0][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver],
                                'Distance',
                                'Time')
            # noinspection PyTypeChecker
            output[1][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver],
                                'Distance',
                                'X')
            # noinspection PyTypeChecker
            output[2][i] = spln(drvs[i], idx['Index zero'][drvs[i].Driver], idx['Index omega'][drvs[i].Driver],
                                'Distance',
                                'Y')
        splns = pd.DataFrame({'Space/Time': output[0][:],
                              'Space/X': output[1][:],
                              'Space/Y': output[2][:]},
                             index=[drvs[value].Driver for value in range(size)])
        return splns

    def plot_limits(drvs, idx):
        ### Description:
        ### input:
        ### output:
        limit_min = min(
            drvs[0].telemetry['X'].loc[idx['Index zero'][drvs[0].Driver]:idx['Index omega'][drvs[0].Driver]])
        limit_max = max(
            drvs[0].telemetry['X'].loc[idx['Index zero'][drvs[0].Driver]:idx['Index omega'][drvs[0].Driver]])

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
        ### Description:
        ### input:
        ### output:
        output = [element['Team'] for element in drvs if element['Driver'] == name]
        return output[0]

    # noinspection PyUnboundLocalVariable
    def segment_times(splines, segments, drvs):
        ### Description:
        ### input:
        ### output:
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
        ### Description:
        ### input:
        ### output:
        output = [None] * segments.shape[1]
        for i in range(segments.shape[1]):
            output[i] = segments[[i + 1]].idxmin().to_string()[-3:]

        return output

    def overlay_map_plot(drvs, segments, time_differance, splines, **kwargs):
        ### Description:
        ### input:
        ### output:
        sector_point = np.ceil(1100 / len(segments))
        fig, ax = plt.subplots()
        fig.canvas.set_window_title("".join('Driver overlay: Fastest mini sectors'))
        driver_title = [drvs[value].Driver for value in range(len(drvs))]
        title = driver_title[0]
        for i in range(len(driver_title) - 1):
            title = "".join((title, " vs. ", driver_title[i + 1]))
        fig.suptitle(title)
        legend = [''] * len(drvs)
        legend_color = [''] * len(drvs)
        for i in range(len(drvs)):
            legend[i] = drvs[i].Driver
            legend_color[i] = plotting.team_color(drvs[i]['Team'])
        patch = [mpatches.Patch(color=legend_color[i], label=legend[i]) for i in range(len(legend))]
        # print(patch)
        for i in range(len(segments) - 1):
            distance = [value for value in (np.arange(segments[i], segments[i + 1], sector_point))]
            X = splines['Space/X'][time_differance[i]](distance)
            Y = splines['Space/Y'][time_differance[i]](distance)
            if len(kwargs) > 0 and 'rotate' in kwargs:
                if kwargs['rotate'] == 0:
                    ax.plot(X, Y, color=plotting.team_color(search(time_differance[i], drvs)))
                if kwargs['rotate'] == 1:
                    ax.plot(Y, -X, color=plotting.team_color(search(time_differance[i], drvs)))
            else:
                ax.plot(X, Y, color=plotting.team_color(search(time_differance[i], drvs)))

        ax.axes.set_aspect('equal')
        ax.set_xlabel("X coordinate")
        ax.set_ylabel("Y coordinate")
        plt.legend(handles=patch)
        fig.set_size_inches(11.5, 7)
        # plt.grid(which = 'both', axis='both', linestyle='--', linewidth=0.5, color='#77773c')
        plt.show()

    sectors = 100
    sector_point = np.ceil(1100 / sectors)

    if 'mode' in kwargs:
        if kwargs['mode'] == 'manual':
            drvs = driver_list
        else:
            drvs = data_list(driver_list, session, 'fastest')
    else:
        drvs = data_list(driver_list, session, 'fastest')


    idx = index_multi(drvs)
    splines = multi_spline(drvs, idx)
    track_length = max(
        [drvs[i].telemetry['Distance'].loc[idx['Index omega'][drvs[i].Driver]] for i in range(len(drvs))])
    segments = [value for value in track_length * (np.arange(sectors + 1)) / sectors]
    segments_time = segment_times(splines, segments, drvs)
    time_differance = fastest_segments(segments_time)
    limits = plot_limits(drvs, idx)
    if len(kwargs) > 0 and 'rotate' in kwargs:
        print(kwargs)
        print(kwargs['rotate'])
        if kwargs['rotate'] == 1:
            rotated = 1
            overlay_map_plot(drvs, segments, time_differance, splines, rotate=rotated)
        if kwargs['rotate'] == 0:
            rotated = 0
            overlay_map_plot(drvs, segments, time_differance, splines, rotate=rotated)
    else:
        overlay_map_plot(drvs, segments, time_differance, splines)


def plot_driver_tire_data(driver_list, laps):
    ### Description:
    ### input:
    ### output:
    drvs = data_list(driver_list, laps, 'all')
    if len(drvs) > 1:
        print("WIP: in plot_driver_tire_data: only one driver taken into account:")
    print(int(max(pd.unique(drvs[0]['Stint']))))
    # hard = drvs[0].loc[np.logical_and(drvs[0]['Compound'] == 'HARD', drvs[0]['IsAccurate'] == True)]
    # medium = drvs[0].loc[np.logical_and(drvs[0]['Compound'] == 'MEDIUM', drvs[0]['IsAccurate'] == True)]
    # soft = drvs[0].loc[np.logical_and(drvs[0]['Compound'] == 'SOFT', drvs[0]['IsAccurate'] == True)]
    # print(max(pd.unique(drvs[0]['Stint'])))
    fig, ax = plt.subplots(2)
    # print(np.unique(drvs[0]['Stint']))
    for i in range(int(max(pd.unique(drvs[0]['Stint'])))):
        current_stint = drvs[0].loc[
            np.logical_and(drvs[0]['Stint'] == i + 1, drvs[0]['IsAccurate'] == True)].pick_quicklaps(threshold=1.07)
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

            fig.suptitle("Tire overview")
            ax[0].plot(current_stint['TyreLife'], times, '.', color=color)
            lookup = np.polyfit(current_stint['TyreLife'], times, 2)
            x = np.linspace(min(current_stint['TyreLife']), max(current_stint['TyreLife']), 100)
            lookup = np.poly1d(lookup)
            y = lookup(x)
            # ax[0].set_title("Tire age")
            ax[0].set_xlabel("Tires age [Laps]")
            ax[0].set_ylabel("Lap time [s]")
            ax[0].plot(x, y, '-', color=color)

            ax[1].plot(current_stint['LapNumber'], times, '.', color=color)
            lookup = np.polyfit(current_stint['LapNumber'], times, 2)
            x = np.linspace(min(current_stint['LapNumber']), max(current_stint['LapNumber']), 100)
            lookup = np.poly1d(lookup)
            y = lookup(x)
            # ax[1].set_title("Tire in Race")
            ax[1].set_xlabel("Race Laps")
            ax[1].set_ylabel("Lap time [s]")
            ax[1].plot(x, y, '-', color=color)
    fig.set_size_inches(11.5, 7)
    plt.draw()
    plt.show()

    return 0


def session_plot(driver_list, laps):
    ### Description:
    ### input:
    ### output:
    # fig, ax = plt.subplots()
    drvs = data_list(driver_list, laps, 'all')
    if len(drvs) > 1:
        print("WIP:in session_plot: only one driver taken into account:")
        # print(drvs[0]['Driver'])
    y = drvs[0].loc[drvs[0]['IsAccurate'] == True]
    # ax.plot(y['LapNumber'], y['LapTime'].dt.total_seconds())

    lookup = np.polyfit(y['LapNumber'], y['LapTime'].dt.total_seconds(), 2)
    x = np.linspace(min(y['LapNumber']), max(y['LapNumber']), 100)
    lookup = np.poly1d(lookup)
    y = lookup(x)
    plt.plot(x, y)
    plt.show()


def tire_by_lap(session, event):
    ### Description:
    ### input:
    ### output:
    fig, ax = plt.subplots(2)
    print(event.name)
    if event.name == 'Qualifying':
        threshold = 1.01
    else:
        threshold = 1.05
    medians = []
    i = 0
    for element in ["SOFT", "MEDIUM", "HARD"]:
        # tyre = session.pick_tyre(element).pick_accurate().pick_quicklaps(threshold=1.05)
        tyre = session.pick_tyre(element)

        if len(tyre) > 0:
            tyre = tyre.pick_accurate().pick_quicklaps(threshold=threshold)
            x = tyre["LapNumber"]
            y = tyre["LapTime"].dt.total_seconds()
            y_avg = pd.to_numeric(tyre['LapTime'].dt.total_seconds()).groupby(tyre['LapNumber'])
            y_avg = y_avg.mean().to_frame().reset_index(level=0)

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

            ax[0].plot(x, y, '.', color=color, alpha=0.5)
            ax[0].plot(y_avg["LapNumber"], y_avg["LapTime"], 'o', color=color, alpha=0.9)

            ax[1].plot(np.random.normal(tire_idx, 0.04, size=len(y)), y, 'o', color=color, alpha=0.5)
            bp = ax[1].boxplot(y, positions=[tire_idx])
            medians.append(max(bp['medians'][0].get_ydata()))
            ax[1].set_xticks([1, 2, 3], minor=False)
            ax[1].set_xticklabels(['SOFT', 'MEDIUM', 'HARD'], fontdict=None, minor=False)
            i = i + 1

    if 'soft' in locals():
        print('Soft median:', round(soft.median()['LapTime'], 3))

    if 'medium' in locals():
        print('Medium median:', round(medium.median()['LapTime'], 3))

    if 'hard' in locals():
        print('Hard median:', round(hard.median()['LapTime'], 3))

    print('\033[1m' + 'Isofuel based:' + '\033[0m')
    if 'soft' in locals() and 'medium' in locals() and 'hard' in locals():
        xline = np.linspace(0.8, 3.2, 50)
        lookup = np.polyfit([1, 2, 3], medians, 1)
        lookup = np.poly1d(lookup)
        yline = lookup(xline)
        ax[1].plot(xline, yline, 'g', linewidth=1)

        # isofuel delta - created from upper plot data
    if ('soft' in locals()) and ('medium' in locals()):
        sof_med = medium - soft
        sof_med_avg = sof_med.median()
        print('Soft - Medium delta:')
        print(round(sof_med_avg["LapTime"], 3))
    if 'medium' in locals() and 'hard' in locals():
        med_har = hard - medium
        med_har_avg = med_har.median()
        print('Medium - Hard delta:')
        print(round(med_har_avg["LapTime"], 3))
    if 'soft' in locals() and 'hard' in locals():
        sof_har = hard - soft
        sof_har_avg = sof_har.median()
        print('Soft - Hard delta:')
        print(round(sof_har_avg["LapTime"], 3))

    plt.grid(which='both')
    fig.set_size_inches(11.5, 7)
    plt.show()

    return 0


def plot_cumulative_time(laps, driver_list, ref_driver):
    ref = laps.pick_driver(ref_driver)
    ref2 = ref
    ref = ref['LapTime'].fillna(ref['Time'] - ref['LapStartTime']).cumsum()
    ref = ref.dt.total_seconds().reset_index(drop=True)

    fig, ax = plt.subplots(1)
    fig.canvas.set_window_title("".join(('Race Time Gap: Reference to ', ref_driver)))
    fig.suptitle("".join(('Reference to ', ref_driver)))
    fig.set_size_inches(11.5, 7)

    for driver in driver_list:
        driver = laps.pick_driver(driver)
        lapTimeCumsum = driver['LapTime'].fillna(driver['Time'] - driver['LapStartTime']).cumsum()
        # print(driver['Driver'].iloc[0])
        # print(lapTimeCumsum.iloc[-1])
        driver_cumsum = lapTimeCumsum.dt.total_seconds().reset_index(drop=True)
        cumsumDiff = ref - driver_cumsum
        ax.plot(cumsumDiff,
                color=plotting.team_color(driver['Team'].iloc[0]),
                label="".join((driver.Driver.iloc[0])))

    ax.plot(ref - ref, color=plotting.team_color(ref2['Team'].iloc[0]),
            label="".join(ref2['Driver'].iloc[0]))
    ax.grid(which='both', axis='both', linestyle='--', linewidth=0.5, color='#77773c')
    ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    ax.set_xlabel("Race Laps")
    ax.set_ylabel("".join(('Gap to ', ref2['Driver'].iloc[0], ' [s]')))
    # plt.show()

    return fig, ax


def annotation(ax, comment_list):
    alpha = 0.65
    for comment in comment_list:
        el = Ellipse(comment[1], comment[2], comment[3], angle=comment[4], edgecolor='white', linestyle=':',
                     linewidth=1.5, facecolor='none', alpha=alpha)
        ax.annotate(comment[0], xy=comment[1], xytext=comment[5], size=10,
                    arrowprops=dict(arrowstyle="->", patchB=el, color='white', linewidth=1.5))
        ax.add_patch(el)

    return ax


def track_status(drv_lap, type, ax, text_posy, text_ang):
    alpha_text = 0.7
    alpha_span = 0.5
    c = 0
    a = []
    for item in drv_lap:
        if ((str(6) in item) or (str(7) in item)) and type == 'VSC':
            a.append(c)
        elif (str(4) in item) and type == 'SC':
            a.append(c)
        c = c + 1

    boundary = [[]]
    boundary_index = 0
    if len(a) > 0:
        for i in range(len(a)):
            if i == 0:
                boundary_index = 0
                temp = a[i]
                boundary[boundary_index].append(temp)

            if i > 0:
                if a[i] == temp + 1:
                    temp = a[i]
                if not boundary[boundary_index]:
                    boundary[boundary_index].append(temp - 1)

                if (a[i] > temp + 1) or i == len(a) - 1:
                    boundary[boundary_index].append(temp)
                    boundary.append([])
                    temp = a[i]
                    boundary_index = boundary_index + 1
    if len(boundary) > 0:
        boundary = boundary[0:-1]

        angle = text_ang
        for event in boundary:
            ax.axvspan(event[0], event[1], facecolor='y', alpha=alpha_span)
            l1 = np.array((event[0] / 2 + event[1] / 2 + 0.5, text_posy))
            if type == 'SC':
                th1 = ax.text(*l1, 'Safety Car', fontsize=12,
                              rotation=angle, rotation_mode='anchor', alpha=alpha_text)
            if type == 'VSC':
                th1 = ax.text(*l1, 'VSC', fontsize=12,
                              rotation=angle, rotation_mode='anchor', alpha=alpha_text)

    return ax


def season_total_time(drvs_list, event_list):
    def calculate_from_telemetry(laps):
        time_cumsum = laps['LapTime'].fillna(laps['Time'] - laps['LapStartTime']).cumsum()
        return time_cumsum.iloc[-1]

    def find_driver_by_code(drv, driver, laps):
        time = None
        try:
            if drv['Driver']['code'] == driver:
                time = pd.to_timedelta(float(drv['Time']['millis']), unit='ms')

        except (ValueError, BaseException, OSError, NameError):
            print(driver)
            print('\t Data Error: Working around that')
            driver_code = drv['Driver']['code']
            drv_laps = laps.pick_driver(driver_code)
            time = calculate_from_telemetry(drv_laps)
        finally:
            return time

    drvs_df = pd.DataFrame(drvs_list)
    drvs_df = drvs_df.rename(columns={0: 'Driver'})
    drvs_df['Cumsum'] = pd.Series(0)
    drvs_df.set_index('Driver', inplace=True)

    drvs_df = drvs_df.assign(Cumsum=pd.Timedelta("0 days"))

    with alive_bar(len(event_list)) as bar:
        for item in event_list:
            # print(item)
            laps, event = crate_event(2021, item, 'R')
            for drv in event.results:

                for name in drvs_df.iterrows():
                    temp = find_driver_by_code(drv, name[0], laps)
                    if temp is not None:
                        drvs_df['Cumsum'][name[0]] = drvs_df['Cumsum'][name[0]] + temp
            bar()

    print('#######################')
    print(drvs_df)
    drvs_df = drvs_df.sort_values('Cumsum')
    drvs_diff_df = drvs_df.sort_values('Cumsum').diff()
    print(drvs_diff_df)
    print(' ')
    print('Percentage differance P1-P2:')
    print(round(float((drvs_diff_df.iloc[1] / drvs_df.iloc[0]) * 100), 3), '%')

from path.source import track_telemetry as tt
from matplotlib import pyplot as plt


"""
Mexico GP 2021
Was Mex Verstappen Tsunoda'd in Qualifying as mentioned by Christian Horner?
On Max final lap he wasn't able to improve, as Yuki Tsunoda had an off in front of him
There were no yellow flags, but there was confusion as Yuki caused Perez to go off track too
Did Yuki and Perez caused distraction to Max, as they were returing to the track?
Let's answer that question.

There was no point loss for Max in championship battle, however confusion arose to Christian Horner's words,
That were very unsupportive towards Red Bull Junior Driver Program protege
"""
driver = 'VER'
laps, event = tt.crate_event(2021, 'Mexico', 'Q')
Ver_Q_laps = tt.data_list(['VER'], laps, 'all')
print("Max Qualifying Lap Time:")
print(Ver_Q_laps[0]['LapTime'])

"""
Lap 30 is Verstappen fastest laps
Lap 33 is where he was Tsunondad
"""
fastest = 30
tsunodad = 33
fastest_slice = Ver_Q_laps[0].loc[fastest]
tsunodad_slice = Ver_Q_laps[0].loc[tsunodad]

print("Max Verstappen Best Lap:")
print("Laptime:")
print(fastest_slice['LapTime'])
print("Session time:")
print(fastest_slice['Time'])
print("Max Verstappen Lap where he was Tsunonda'd")
print("Laptime:")
print(tsunodad_slice['LapTime'])
print("Session time:")
print(tsunodad_slice['Time'])

"""
HIGHLIGHT:
Green: Where Max was Tsunoda'd
Red: Subsequent mistakes
"""

""" Overlay two laps in question """
fig, ax = tt.overlay_laps(tsunodad_slice, fastest_slice, "Was Max Tsunoda'd", 'Fastest lap', "Tsunoda'd lap")

""" Mark important parts """
distance_a = 2870
distance_b = 2990
ax[1].axvspan(distance_a, distance_b, facecolor = 'g', alpha = 0.5)
ax[0].axvspan(distance_a, distance_b, facecolor = 'g', alpha = 0.5)

distance_a = 3750
distance_b = 3820
ax[1].axvspan(distance_a, distance_b, facecolor = 'r', alpha = 0.5)
ax[0].axvspan(distance_a, distance_b, facecolor = 'r', alpha = 0.5)

distance_a = 3610
distance_b = 3500
ax[1].axvspan(distance_a, distance_b, facecolor = 'r', alpha = 0.5)
ax[0].axvspan(distance_a, distance_b, facecolor = 'r', alpha = 0.5)

plt.show()

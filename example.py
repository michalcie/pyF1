import fastf1 as ff1
from matplotlib import pyplot as plt

# ff1.utils.enable_cache('path/to/folder/for/cache')  # optional but recommended

monza_quali = ff1.get_session(2019, 'Monza', 'Q')

# vettel = monza_quali.get_driver('VET')
# print(f"Pronto {vettel.name}?")
# Pronto Sestian?

laps = monza_quali.load_laps(with_telemetry=True, livedata=None)
fast_leclerc = laps.pick_driver('LEC').pick_fastest()
fast_hamilton = laps.pick_driver('HAM').pick_fastest()
yLEC = fast_leclerc.telemetry['Y']
xLEC = fast_leclerc.telemetry['X']
yHAM = fast_hamilton.telemetry['Y']
xHAM = fast_hamilton.telemetry['X']

# The rest is just plotting
fig, ax = plt.subplots()
ax.plot(yLEC, xLEC, label='Leclerc')
ax.plot(yHAM, xHAM, label='Hamilton')
ax.set_xlabel('Y')
ax.set_ylabel('X')
ax.set_title('Leclerc is Karolek')
ax.legend()
plt.show()

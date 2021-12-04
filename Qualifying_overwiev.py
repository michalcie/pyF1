from path.source import track_telemetry as tt
from matplotlib import pyplot as plt


# session = tt.crate_event(2020, 'Italy', 'Q')
# tt.overlay_drivers(['VER', 'HAM'], session)
# tt.overlay_map_multi(['HAM', 'VER', 'NOR'], session)

### Qualifying overview shows selected metrics from qualifing session
### at this point only standard qualifing is supported - no sprint races
driver = ['VER', 'HAM']
session, event = tt.crate_event(2021, 'Mexico', 'R')
tt.overlay_drivers(driver, session)
plt.show()
# tt.overlay_map_multi(driver, session)
# tt.plot_driver_tire_data(driver, session)
# tt.session_plot(driver, session)
# tt.tire_by_lap(session, event)

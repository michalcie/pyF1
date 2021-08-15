from path.source import track_telemetry as tt


# session = tt.crate_event(2020, 'Italy', 'Q')
# tt.overlay_drivers(['VER', 'HAM'], session)
# tt.overlay_map_multi(['HAM', 'VER', 'NOR'], session)
driver = 'VER'
session = tt.crate_event(2021, 'Hungary', 'R')
# tt.plot_driver_tire_data([driver], session)
# tt.session_plot([driver], session)
tt.tire_by_lap(session)

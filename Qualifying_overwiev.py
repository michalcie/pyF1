import track_telemetry as tt


session = tt.crate_event(2020, 'Italy', 'Q')
tt.overlay_drivers(['VER', 'HAM'], session)
tt.overlay_map_multi(['HAM', 'VER', 'NOR'], session)
tt.ten_best(['HAM', 'VER'], session)



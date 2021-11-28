from path.source import track_telemetry as tt
from matplotlib import pyplot as plt
import sys, os
import logging


#############################################################

""" TEST PREPARATION """#######################################

""" Disable logging messages from fastf1 """
logger = logging.getLogger()
logger.disabled = True


""" Hiding all prints"""
class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

print(" ")
print("##############################################")
print("TESTING")


#############################################################

""" FUNCTIONAL SET """#######################################

print(" ")
print("#Functional Tests")

""" Parameters """ ##########################################
driver_list_1 = ['VER', 'HAM']
driver_list_2 = ['VER', 'HAM', 'SAI', 'NOR']
passed_f = 0
failed_f = 0
passed_r = 0
failed_r = 0

#############################################################

""" CE_1: Create event: Mexico 2021: Qualifying """
try:
    with HiddenPrints():
        laps_FS1, event_FS1 = tt.crate_event(2021, 'Mexico', 'Q')

    print("ID: CE_1 \t passed")
    passed_f = passed_f + 1
except:
  print("ID: CE_1 \t failed")
  failed_f = failed_f + 1


""" CE_2: Create event: Mexico 2021: Race """
try:
    with HiddenPrints():
        laps_FS2, event_FS2 = tt.crate_event(2021, 'Mexico', 'R')
    print("ID: CE_2 \t passed")
    passed_f = passed_f + 1
except:
  print("ID: CE_2 \t failed")
  failed_f = failed_f + 1


""" OD_1: Overlay Drivers: Max, Lewis """
try:
    tt.overlay_drivers(driver_list_1, laps_FS1)
    plt.show()
    print("ID: OD_1 \t passed")
    passed_f = passed_f + 1
except:
    print("ID: OD_1 \t failed")
    failed_f = failed_f + 1


""" MAP_1: Overlay Map Multi: Max, Lewis """
try:
    tt.overlay_map_multi(driver_list_2, laps_FS1)
    print("ID: MAP_1 \t passed")
    passed_f = passed_f + 1
except:
    print("ID: MAP_1 \t failed")
    failed_f = failed_f + 1


""" RDG_1: Ridgeline Plot: Max, Lewis, Sainz, Norris """
try:
    with HiddenPrints():
        tt.ridgeline(driver_list_2, laps_FS2, 'title', None, None, None)
    print("ID: RDG_1 \t passed")
    passed_f = passed_f + 1
except:
    print("ID: RDG_1 \t failed")
    failed_f = failed_f + 1


# with HiddenPrints():
    # session, event = tt.crate_event(2021, 'USA', 'R')

""" WIP - only first driver"""
""" TDP_1: Tire Driver Plot: Max, Lewis """
try:
    with HiddenPrints():
        tt.plot_driver_tire_data(driver_list_1, laps_FS2) ### Why I see only 2 stints on MED?
    print("ID: TDP_1 \t passed")
    passed_f = passed_f + 1
except:
    print("ID: TDP_1 \t failed")
    failed_f = failed_f + 1


""" Heavy WIP """
# try:
#     with HiddenPrints():
#         tt.session_plot(driver_list_1, session)
#     print("ID: SP_1 \t passed")
#     passed_f = passed_f + 1
# except:
#     print("ID: SP_1 \t failed")
#     failed_f = failed_f + 1


""" TDP_1: Tire by Laps: all drivers in session """
try:
    with HiddenPrints():
        tt.tire_by_lap(laps_FS2, event_FS2)
    print("ID: TBL_1 \t passed")
    passed_f = passed_f + 1
except:
    print("ID: TBL_1 \t failed")
    failed_f = failed_f + 1


#############################################################

""" REGRESION SET """########################################

print(" ")
print("#Regression Tests")


try:
    with HiddenPrints():
        exec(open("2021_Mexico_Qual_WasMaxTsunodad.py").read())
    print("ID: REG_1 \t passed")
    passed_r = passed_r + 1
except:
    failed_r = failed_r + 1
    print("ID: REG_1 \t passed")


try:
    with HiddenPrints():
        exec(open("2021_Brazil_Race_HamiltonsCharge.py").read())
    print("ID: REG_2 \t passed")
    passed_r = passed_r + 1
except:
    failed_r = failed_r + 1
    print("ID: REG_2 \t passed")


try:
    with HiddenPrints():
        exec(open("2021_Brazil_QSandRACE_HamiltonsCharge.py").read())
    print("ID: REG_3 \t passed")
    passed_r = passed_r + 1
except:
    failed_r = failed_r + 1
    print("ID: REG_3 \t passed")


#############################################################

""" RESULTS """########################################

print(" ")
print("#RESULTS:")

"""Functional Results"""
print("Functional:")
pass_ratio_f = passed_f*100/(failed_f + passed_f)
print("Tests passed: \t", passed_f)
print("Tests failed: \t", failed_f)
print("Pass ratio: \t", pass_ratio_f, "%")

print(" ")
"""Regression Results"""
print("Regression:")
pass_ratio_r = passed_r*100/(failed_r + passed_r)
print("Tests passed: \t", passed_r)
print("Tests failed: \t", failed_r)
print("Pass ratio: \t", pass_ratio_r, "%")


print(" ")
print("##############################################")

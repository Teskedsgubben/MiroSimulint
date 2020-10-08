# IMPORT LINE:
# from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI

# This file decides which API MiroSimulint will use.
# Some functionality may not have full support from both APIs.
# The SelectedAPI variable is imported as MiroAPI across
# the library and should point to either chronoAPI to use
# PyChrono or to agxAPI to use agx Dynamics. 

# Note: Changing API will most likely require you to change 
# Python interpreter, unless you have specifically made sure
# to install all dependencies into the same environment.

# Set to 'chrono' or 'agx'
API = 'chrono'

if API == 'agx':
    import MiroClasses.MiroAPI_agx as agxAPI
    SelectedAPI = agxAPI
elif API == 'chrono':
    import MiroClasses.MiroAPI_chrono as chronoAPI
    SelectedAPI = chronoAPI
else:
    import sys
    sys.exit('API configuration invalid, open MiroClasses -> MiroAPI_selector to fix.')



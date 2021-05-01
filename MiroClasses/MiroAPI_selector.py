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

# Set to 'PyChrono' or 'AGX'
API = 'AGX'

import os
if(not os.path.isfile('MiroClasses/MiroAPI_local.py')):
    if API == 'PyChrono':
        import MiroClasses.MiroAPI_chrono as SelectedAPI
    elif API == 'AGX':
        import MiroClasses.MiroAPI_agx as SelectedAPI
    else:
        import sys
        sys.exit('API configuration invalid, open MiroClasses -> MiroAPI_selector to fix.')
else:
    from MiroClasses import MiroAPI_local
    SelectedAPI = MiroAPI_local.SelectedAPI

# To create a local API configuration file, simply create a file in the same directory 
# named 'MiroAPI_local.py' that contains only one of these lines:
# import MiroClasses.MiroAPI_chrono as SelectedAPI
# import MiroClasses.MiroAPI_agx as SelectedAPI
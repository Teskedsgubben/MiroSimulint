
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import sys
try:
    import agx
except:
    sys.exit("Could not import AGX for playground, run \"C:\Program Files\Algoryx\AGX-2.29.2.0\setup_env.bat\" in terminal, including citation marks.")

import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxModel
import agxRender
import agxDriveTrain
from agxPythonModules.models.wheel_loaders import WheelLoaderL70
from agxPythonModules.utils.environment import simulation, root, application, init_app
from agxPythonModules.utils.callbacks import StepEventCallback, KeyboardCallback as Input, GamepadCallback as Gamepad

import time
import math
import numpy as np

try:
    import socketio
except:
    print('Socketio import failed')

def RunPureAGX(MiroSystem):
    # This is the entry point for running pure agx code in the MiroSim environment.
    # This function will be called with SystemList = [sim, app, root] and you can
    # set Args to be whatever you want from the Main function. 
    [sim, app, root] = MiroSystem.Get_APIsystem()

    return
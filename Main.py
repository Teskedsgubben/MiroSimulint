#------------------------------------------------------------------------------
# Name:         Miro Simulint
# 
# Purpose:      Main script to run a launcher + lander simulation designed for
#               Physics students at Umeå University
# 
# Usage:        Create a lander in the Landers.py file, or modify the DemoLander.
#               Likewise, create a launcher in Launchers.py. This Main file will
#               then insert your modules into the MIT environment where you test
#               them out. You can also compute and pass along input arguments to
#               use when creating your modules.
#
# Authors:      Felix Djuphammar, William Nordberg, Marcus Lindbergh, 
#               Johan Jonsson, Franz Wikner, Niklas Edlund
#
#-------------------------------------------------------------------------------
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses import MiroSystem as MS
from src import Environments
from src import Props
import numpy as np

# Import Demomodules
import DemoModules

# Function that runs the simulation
def buildScene():
    # Initialize a Miro System
    Simulation = MS.MiroSystem()

    # Set the environment to MIT place.
    # If the simulation is too slow, set Speedmode to True.
    Simulation.Set_Speedmode(False)
    Simulation.Set_Environment(Environments.MIT_place)

    # Add a DemoModule to the system with a name and position.
    Simulation.Add_MiroModule(DemoModules.DemoRobot1(), 'MyRobot', [11, 8,-3])

    # Set camera viewing perspective, options are:
    # 1: '2nd (ground) floor front view'
    # 2: '2nd (ground) floor side view'
    # 3: '3rd floor staircase'
    # 4: '4th floor behind lander'
    # 5: '4th floor observing launcher'
    # 6: 'target' 
    # 0: 'default'
    # Special: 'follow', 'Module Name', [x, y, z]
    # Use mouse, scroll wheel, arrow keys and pg up & pg down to move
    # Press I and see the help section for a full list of controls
    Simulation.Set_Perspective('4th floor observing launcher')

    # Entry point for custom AGX code
    if MiroAPI.API == 'AGX':
        from agx_playground import RunPureAGX
        RunPureAGX(Simulation)

    Simulation.Run()

# Initializes and runs the system
MS.MiroSetup(buildScene)

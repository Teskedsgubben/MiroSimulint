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
    Simulation.Add_MiroModule(DemoModules.DemoRobot1(), 'MyRobot', [-3.2, 0, 3])

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

    # ----- SWEEPING FUNCTIONS FOR RECORDING -----
    # Sweeping across the map
    #Simulation.Add_Camview('last_sweep_pos', [11, 6,-7], [0,0,0], look_at_point=[1,1,-1])
    #Simulation.Set_Perspective('last_sweep_pos')
    #Simulation.Set_CameraSweep([[11, 6,-7],[3,7,-7],[-4,3,-7],[-3,7,-5],[2,5,-7],[4,2,-6],[8,6,-7]], [[0,0,0],[0,0,0],[0,0,0],[-1.5,1.5,3],[-1,0.5,3],[1,1,2],[0,0,0]])

    # Sweep onto the stage
    # MiroSystem.py line 178: sweep_divs = 1000
    # src -> MIT_Props.py line 104: Comment out the MeasureBox.
    #Simulation.Add_Camview('last_sweep_pos', [0,0.8,-4], [0,0,0], look_at_point=[-3.5,1.2,-7])
    #Simulation.Set_Perspective('last_sweep_pos')
    #Simulation.Set_CameraSweep([[7, 2.7,8],[-1,3,-2]], [[-3,1,-7],[-3.5,1.2,-7]])   

    # Entry point for custom AGX code
    if MiroAPI.API == 'AGX':
        from agx_playground import RunPureAGX
        RunPureAGX(Simulation)

    Simulation.Run()

# Initializes and runs the system
MS.MiroSetup(buildScene)

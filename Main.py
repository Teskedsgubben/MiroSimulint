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
#               Johan Jonsson, Franz Wikner
#
#-------------------------------------------------------------------------------

from MiroClasses import MiroSystem as ms
from src import Environments as env
from src import Props
import numpy as np

# Import any local files first, otherwise use repo files
try:
    import Landers_local as Landers
except:
    import Landers

try:
    import Launchers_local as Launchers
except:
    import Launchers

# Initialize a Miro System
simulation_system  = ms.MiroSystem()

# Set the environment to MIT place.
# If the simulation is too slow, set Speedmode to True.
simulation_system.Set_Speedmode(False)
simulation_system.Set_Environment(env.MIT_place)

# Get the position of the target as [x, y, z]
target = simulation_system.Get_Target()

# COMPUTE THE ARGUMENTS YOU NEED FOR YOUR LAUNCHER AND LANDER HERE
# You can pass any arguments you want to your launcher or lander
# that you compute from the target coordinates
aim = -10      # Example of direction to shoot
pullback = 5   # Example of how much strength is needed

# Add the DemoLauncher to the system at the specified position
launcher_position = [10, 6.69, -2.2]
simulation_system.Add_MiroModule(Launchers.DemoLauncher([aim, pullback]), 'Launcher', launcher_position)

# Add the DemoLander to the system
simulation_system.Add_MiroModule(Landers.DemoLander([aim, pullback]), 'Lander')

# Move the Lander to the point set by the Launcher
simulation_system.MoveToReference('Lander', 'Launcher')

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
simulation_system.Set_Perspective('4th floor observing launcher')

# Run the system simulation at [w, h] resolution and X seconds delay to let
# the lander settle in before pausing (which is then released by SPACEBAR)
config = {
    'resolution': [1920, 1080],
    'delay': 3,
    'datalog': False,
    'print module info': True,
}
simulation_system.Run(config)

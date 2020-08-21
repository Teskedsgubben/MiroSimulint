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


import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import Launchers as launchers
import MiroSystem as ms

# Initialize a Miro System
simulation_system  = ms.MiroSystem()

# Set the environment to MIT place
simulation_system.Set_Speedmode(False)
simulation_system.Set_Environment(env.MIT_place)

# Set camera viewing perspective, options are:
# 1: '2nd (ground) floor front view'
# 2: '2nd (ground) floor side view'
# 3: '3rd floor staircase'
# 4: '4th floor behind lander'
# 5: '4th floor observing launcher'
# 6: 'target' 
# 0: 'default'
# Use mouse, scroll wheel, arrow keys and pg up & pg down to move
simulation_system.Set_Perspective('target')

# Get the position of the target as [x, y, z]
target = simulation_system.Get_Target()
# COMPUTE THE ARGUMENTS YOU NEED FOR YOUR LAUNCHER AND LANDER HERE
# You can pass any arguments you want to your launcher or lander
# that you compute from the target coordinates
aim = -10         # Example of direction to shoot
pullback = 5   # Example of how much strength is needed

# Add the Launcher to the system at the specified position
simulation_system.Add_MiroModule(launchers.DemoLauncher([aim, pullback]), 'Launcher', [10, 8.05, -2.2])

# Add the Lander to the system
simulation_system.Add_MiroModule(landers.DemoLander([aim, pullback]), 'Lander')

# Move the Lander to the point set by the Launcher
simulation_system.MoveToReference('Lander', 'Launcher')

# Run the system simulation
simulation_system.Run([1920, 1080], 3)

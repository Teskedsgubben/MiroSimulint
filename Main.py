#------------------------------------------------------------------------------
# Name:         Miro Simulint
# 
# Purpose:      Main script to run a lander simulation designed to temporarilty 
#               replace the physically 3D-printed modules that are normally used
#               in the course. This is a virtual adaption due to COVID-19.
# 
# Usage:        Create a lander in the Landers.py file, or modify the DemoLander.
#               This Main file will then insert that lander into the MIT place at
#               the predetermined coordinates and throw it over the edge. 
#
# Authors:      Felix Djuphammar, William Nordberg, Marcus Lindbergh, Johan Jonsson, Franz Wikner
#
#-------------------------------------------------------------------------------


import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms

# Initialize a Miro System
simulation_system  = ms.MiroSystem()

# Set the environment to MIT place
simulation_system.Set_Environment(env.MIT_place)

# Add the Demo Lander to the system
simulation_system.Add_MiroModule(landers.DemoLander)

# Run the system simulation
simulation_system.Run()

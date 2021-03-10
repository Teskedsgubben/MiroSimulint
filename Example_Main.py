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
from MiroClasses.MiroSystem import MiroSystem
from MiroClasses.MiroSystem import MiroSetup
from src import Environments
import Example_MiroBots as MiroBots
import Example_BotController as CustomController

import TestController

# Function that runs the simulation
def buildScene():
    # Initialize a Miro System
    Simulation = MiroSystem()
    Simulation.Set_Environment(Environments.MIT_place)

    # Add the DemoRobot to the system at the specified position
    BotPosition1 = [9.3, 7.6, 1.7]
    BotPosition2 = [9.3, 7.8, 1.7]
    Simulation.Add_MiroModule(MiroBots.DemoRobot1(), 'MyBot1', BotPosition1)
    Simulation.Add_MiroModule(MiroBots.DemoRobot2(), 'MyBot2', BotPosition2)

    # Set the camera perspective
    view = [BotPosition1[0]-0.17, BotPosition1[1], BotPosition1[2]+0.17]
    Simulation.Add_Camview('testpos', [10.3, 8.2, 2.65], [-0.25,-0.2,-1],look_at_point=view)
    Simulation.Set_Perspective('follow_default', follow_module_name='MyBot1', cycle=True)

    TestController.AddDummController(Simulation, 'MyBot1')
    # CustomController.ControlModule(Simulation.Get_MiroModule('MyBot2'))
    
    Simulation.Run()

# Initializes and runs the system
MiroSetup(buildScene)

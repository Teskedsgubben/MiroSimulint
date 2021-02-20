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

from Example_Controller import MyController as Mycontrol
import TestBots as TB


# Function that runs the simulation
def buildScene():
    # Initialize a Miro System
    simulation_system = MS.MiroSystem()

    # Set the environment to MIT place.
    # If the simulation is too slow, set Speedmode to True.
    simulation_system.Set_Speedmode(False)
    simulation_system.Set_Environment(Environments.MIT_place)

    #Creates robot defined in 'TestBots.py', adds controller defined in 'Example_Controller.py' to robot.
    MyBot = TB.MyRobot()
    MyBot.AddController(Mycontrol)
    MyBot.Set_Max_Force(100)

    #Adds robot to system
    simulation_system.Add_MiroModule(MyBot, 'MyBot', [6,2,0])

    #Camera settings
    simulation_system.Add_Camview('at_origo', position=[3,2,-2], look_at_point=[6,0,0])
    simulation_system.Set_Perspective('at_origo')
    #simulation_system.Set_Perspective('follow_default', follow_module_name = 'MyTireBot', follow_distance=2)
    
    config = {
        'resolution': [1920, 1080],
        'delay': 3,
        'datalog': False,
        'print module info': True,
    }

    simulation_system.Run(config)

# Initializes and runs the system
MS.MiroSetup(buildScene)

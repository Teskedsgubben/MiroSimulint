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
import Example_Controller as Controller


# Function that runs the simulation
def buildScene():
    # Initialize a Miro System
    Simulation = MiroSystem()
    Simulation.Set_Environment(Environments.MIT_place)

    # Add the DemoRobot to the system at the specified position
    BotPosition1 = [0.75, 0.5, 3.25]
    MyBot1 = MiroBots.DemoRobot1()
    Simulation.Add_MiroModule(MyBot1, 'MyBot1', BotPosition1)
    MyBot1.AddController(Controller.MyController, Controller.controls)
    MyBot1.AddControllerAI(Controller.sensor_Controller)

    # BotPosition2 = [9.3, 7.8, 1.7]
    # MyBot2 = MiroBots.DemoRobot2()
    # Simulation.Add_MiroModule(MyBot2, 'MyBot2', BotPosition2)

    # Set the camera perspective
    Simulation.Add_Camview('Robotcourse', [0,20,0], [0,0,0],look_at_point=[0,0,0])
    Simulation.Set_Perspective('Robotcourse')

    # Set follow cam
    # Simulation.Set_Perspective('follow_default', follow_module_name='MyBot1', follow_distance=3, follow_height=1.25)
    
    Simulation.Run()

# Initializes and runs the system
MiroSetup(buildScene)

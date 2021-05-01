#------------------------------------------------------------------------------
# Name:         Miro Simulint
# 
# Purpose:      Main script to run modular rigid body simulations with a simple 
#               interface. Designed by and for students at Umeå University.
# 
# Usage:        Create local copies of the Example files and rename with suffix
#               "_local" to indicate them as your local files. You will then have
#               the original Example files intact to refer back to.
# 
#               Adjust the imports at the top of the files in your Main file to
#               your chosen name for your local files. Example if your local file
#               is named MyRobots_local.py:
#                   import Example_MiroBots as MiroBots
#                        - becomes -
#                   import MyRobots_local as MiroBots
#               
#               Now, modify modules and controllers in your local files however
#               you like! View the file MiroComponents Specs.pdf in the documents
#               directory to see what predefined components you can use, and when
#               you're ready you can create your own components.
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

    # Create and orient DemoRobot1
    BotPosition = [3.2, 0.6, 0.1]  # Starting point
    MyBot = MiroBots.DemoRobot1()  # Create robot
    MyBot.RotateModuleY(-90)       # Rotate robot

    # Add the robot and controllers to the system 
    Simulation.Add_MiroModule(MyBot, 'MyBot', BotPosition)
    MyBot.AddControllerGUI(Controller.MyController, Controller.controls_arrows)
    MyBot.AddControllerAI(Controller.SensorController)

    # Set the camera perspective using free camera
    Simulation.Add_Camview('Robotcourse', [10,10,-1], [0,0,0],look_at_point=[0,-1,-1])
    Simulation.Set_Perspective('Robotcourse')

    # Set the camera perspective to follow the robot 
    # Simulation.Set_Perspective('follow_default', follow_module_name='MyBot', follow_distance=3, follow_height=1.25)
    
    Simulation.Run()

# Initializes and runs the system
MiroSetup(buildScene)

import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

from src import Components
from src import Boosters
from src import Sensors

try:
    import CustomComponents_local as CustomComponents
except:
    import CustomComponents

# To learn how to modify the Lander, start by changing the components for the
# Bottom and Top plates on lines 31 and 32 to change the Lander dimension.
# Then change the rods on lines 36-39 to another component model to see how 
# the lander changes. 

def DemoLander(args):
    aim = args[0]
    tilt = -args[1]
    Lander = MM.Module()

    # Add top and bottom plates
    # MC component arguments are rotation, position and fixed (true/false)
    # Defaults to [0,0,0], [0,0,0], False if arguments are not provided
    # Note: Use Lander.RotateX, Y or Z if you are making several rotations to
    #       a component, as the order the rotations are made in is significant. 
    Lander.AddComponent(Components.MC035([ 0, 90, 0], [0,0,0], False), 'Bottom plate')
    Lander.AddComponent(Components.MC035([ 0, 90, 0]), 'Top plate')
    Lander.RotateX('Top plate', 180)

    # Add vertical rods
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod A')
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod B')
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod C')
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod D')
    
    Lander.AddSensor(Sensors.MSA02([180,0,0]), 'Accelerometer')
    
    Lander.RotateComponentsZ(tilt)
    Lander.RotateComponentsY(aim)

    # Connect Rods to bottom plate
    # It connects the first component to the second by
    # moving the second component so the points match
    Lander.ConnectComponents('Bottom plate', 'A', 'Rod A', 'A')
    Lander.ConnectComponents('Bottom plate', 'B', 'Rod B', 'A')
    Lander.ConnectComponents('Bottom plate', 'C', 'Rod C', 'A')
    Lander.ConnectComponents('Bottom plate', 'D', 'Rod D', 'A')

    # Connect Top plate to rods (note the order compared to above)
    Lander.ConnectComponents('Rod A', 'B', 'Top plate', 'C')
    Lander.ConnectComponents('Rod B', 'B', 'Top plate', 'D')
    Lander.ConnectComponents('Rod C', 'B', 'Top plate', 'A')
    Lander.ConnectComponents('Rod D', 'B', 'Top plate', 'B')

    # Connect sensor to the module, behaves just like a component
    Lander.ConnectComponents('Top plate', 'E', 'Accelerometer', 'Linkpoint')

    return Lander

# Example of how to set a trigger function to a booster 
def RocketLander(args):
    Lander = MM.Module()
    # The trigger function will get position, velocity and acceleration on the form [x,y,z]
    # You choose when to trigger the rocket by deciding under what conditions to return True
    def trigger_function(position, velocity, acceleration):
        if position[1] < 2.5:
            print('Triggered!')
            return True
        else:
            return False
    Lander.AddBooster(Boosters.MCB01(trigger_function), 'Booster')
    Lander.RotateZ('Booster', 10)
    return Lander
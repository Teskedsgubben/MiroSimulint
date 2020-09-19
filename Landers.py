import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

from src import Components
from src import Sensors

def DemoLander(args):
    aim = args[0]
    tilt = -args[1]
    Lander = MM.Module()

    # Add top and bottom plates
    # MC component arguments are rotation, position and fixed (true/false)
    # Defaults to [0,0,0], [0,0,0], False if arguments are not provided
    Lander.AddComponent(Components.MC035([  0,90,0], [0,0,0], False), 'Bottom plate')
    Lander.AddComponent(Components.MC035([180,90,0]), 'Top plate')

    # Add vertical rods
    Lander.AddComponent(Components.MC113([0, 0, 90]), 'Rod A')
    Lander.AddComponent(Components.MC113([0, 0, 90]), 'Rod B')
    Lander.AddComponent(Components.MC113([0, 0, 90]), 'Rod C')
    Lander.AddComponent(Components.MC113([0, 0, 90]), 'Rod D')
    
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

    # Connect sensor to the module, behave just like a component
    Lander.ConnectComponents('Top plate', 'E', 'Accelerometer', 'Linkpoint')

    return Lander

def KristersLandare(args):
    aim = args[0]
    tilt = -args[1]
    Lander = MM.Module()

    Lander.AddComponent(KristerK([0, 0, 0]), 'Custom K')
    
    # Lander.AddSensor(Sensors.MSA02([180,0,0]), 'Kristerometer')
    
    # Lander.ConnectComponents('Custom K', 'A', 'Kristerometer', 'Linkpoint')

    Lander.RotateComponentsZ(tilt)
    Lander.RotateComponentsY(aim)

    return Lander

# Custom Component Example
def KristerK(rot = [0,0,0], pos = [0,0,0], Fixed = False): 
    # Create blank MiroComponent
    CustomComponent = MC.MiroComponent()
    
    # Import .obj file from object_files directory and set color [R, G, B]
    CustomComponent.ImportObj('K.obj', color = [1, 0.2, 0.6])
    
    # Add linkpoints to enable connecting with other components
    CustomComponent.AddLinkPoint('A', [0, 1, 0], [0, 0.0235/2, 0])
    CustomComponent.AddLinkPoint('B', [0,-1, 0], [0,-0.0235/2, 0])
    
    CustomComponent.Rotate(rot)
    CustomComponent.MoveToPosition(pos)

    return CustomComponent
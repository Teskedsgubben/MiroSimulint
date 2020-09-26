import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

from src import Components
from src import Sensors

import CustomComponents

# To learn how to modify the Launcher, start by changing the component 'Main arm' on line 26
# to one of different length and calibrate the spring constant on line 77. 
# The Launcher can hit the target with modifications to only these two things.

def DemoLauncher(args):
    # Extract arguments into local variables
    aim = args[0]
    angle = args[1]

    # Start by creating a new module
    Launcher = MM.Module()

    # Add some components
    Launcher.AddComponent(Components.MC907([0,0,0]), 'Base')
    Launcher.AddComponent(Components.MC906([0,0,0]), 'Pillar')
    Launcher.AddComponent(Components.MC144([0,0,-angle]), 'Main arm')
    Launcher.AddComponent(Components.MC095([0,90,-angle]), 'Launch plate')

    Launcher.AddComponent(Components.MC115([0,90,180-angle]), 'Stop holder')
    Launcher.AddComponent(Components.MC221([90,0,0]), 'Rotation pole out') # Appearance only
    Launcher.AddComponent(Components.MC221([90,0,0]), 'Rotation pole in') # Appearance only

    Launcher.AddComponent(CustomComponents.KristerK([-90,-150,0]), 'Custom K') # Custom Component

    # Example of how to set the reference point for where to put the lander
    # This puts the reference point 8cm above the Launch plate
    Launcher.SetReferenceComponent('Launch plate', [0, 0.08, 0])

    # Reference point rotates when ALL components rotate
    Launcher.RotateComponentsY(aim)

    # Connect the components. The first remains in position, and the second component is moved to match
    Launcher.ConnectComponents('Base', 'E', 'Pillar', 'C')
    Launcher.ConnectComponents('Pillar', 'A', 'Main arm', 'C', 0.025) # Here, the 0.025 is to leave space between
    Launcher.ConnectComponents('Main arm', 'H', 'Launch plate', 'E')
    Launcher.ConnectComponents('Launch plate', 'A', 'Stop holder', 'H')
    Launcher.ConnectComponents('Launch plate', 'B', 'Stop holder', 'G')
    Launcher.ConnectComponents('Main arm', 'D', 'Rotation pole out', 'B')
    Launcher.ConnectComponents('Main arm', 'C', 'Rotation pole in', 'A')
    Launcher.ConnectComponents('Pillar', 'F', 'Custom K', 'C')

    # To find the global coordinate of a link point, you can print it like this
    # print(Launcher.GetLinkPointXYZ('Main arm', 'B'))

    # To visualize where a link point is, you can use this function, or the DUMMY component. 
    # Make sure to do this after connecting all the components.
    Launcher.MarkLinkpoint('Base', 'B', color='blue')

    # Set a spring to make the catapult launch. You can use any values, but they must be fixed 
    # (i.e. not computed from input arguments)
    # State which two connection points you want to connect the spring to, then choose a rest length and spring constant.
    # Rest length: How long the spring is when it exerts no force. If it is made shorter then this length, 
    #    it is compressed and will push out to expand. If it is made longer, it is streched and will pull to contract.
    # Spring constant: How powerful the spring is. Higher value means more force.
    # The spring is not visible, but the connection points are visualized by small spheres. You can change the default appearance or remove these with input arguments.
    Launcher.SetSpring('Base', 'A', 'Main arm', 'E', 1.1, 17000)

    # Fixate the moving parts so that they initially do not move. This is released after the initial delay.
    Launcher.Fixate('Main arm')

    return Launcher
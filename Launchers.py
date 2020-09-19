import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

from src import Components
from src import Sensors

def DemoLauncher(args):
    # Extract arguments into local variables
    aim = args[0]
    angle = args[1]

    # Start by creating a new module
    Launcher = MM.Module()

    # Add some components
    Launcher.AddComponent(Components.MC007([0,0,0]), 'Base')
    Launcher.AddComponent(Components.MC106([0,0,0]), 'Pillar')
    Launcher.AddComponent(Components.MC143([0,0,-angle]), 'Main arm')
    Launcher.AddComponent(Components.MC095([0,90,-angle]), 'Launch plate')
    
    Launcher.AddComponent(Components.MC115([0,90,180-angle]), 'Stop holder')
    Launcher.AddComponent(Components.MC221([90,0,0]), 'Rotation pole out') # Appearance only
    Launcher.AddComponent(Components.MC221([90,0,0]), 'Rotation pole in') # Appearance only

    # Example of how to find the reference point
    # by pulling arm back before aiming
    rc = [0.0, 0.79, 0.225]
    arm = [1.0-0.115,0.135,0]
    armrot = [
         arm[0]*np.cos(np.deg2rad(angle)) + arm[1]*np.sin(np.deg2rad(angle)),
        -arm[0]*np.sin(np.deg2rad(angle)) + arm[1]*np.cos(np.deg2rad(angle)),
        0
    ]
    Launcher.SetReferencePoint([rc[0]+armrot[0], rc[1]+armrot[1], rc[2]+armrot[2]])


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

    # Launcher.ConnectComponents('Pillar', 'E', 'Custom K', 'A', 0.5)

    # To find the global coordinate of a link point, you can print it like this
    # print(Launcher.GetComponent('Main arm').GetLinkPointXYZ('B'))

    # To visualize where a link point is, you can use the DUMMY component
    Launcher.AddComponent(Components.DUMMY(), 'Dummy')
    Launcher.ConnectComponents('Base', 'A', 'Dummy', 'A')
    
    # You can also identify a component by marking it in a certain color
    Launcher.MarkComponent('Dummy', 'blue')

    # Set a spring to make the catapult launch. You can use any values, but they must be fixed 
    # (i.e. not computed from input arguments)
    Launcher.SetSpring('Base', 'A', 'Main arm', 'E', 1.1, 30000)

    # Fixate the moving parts so that they initially do not move. This is released when resuming after the initial pause.
    Launcher.Fixate('Main arm')

    return Launcher
import pychrono.core as chrono
import numpy as np

import MiroModule as mm
import Components as mc

def DemoLauncher(args):
    # Extract arguments into local variables
    aim = args[0]
    angle = args[1]

    # Start by creating a new module
    Launcher = mm.Module()

    # Add some components
    Launcher.AddComponent(mc.MC007([0,0,0]), 'Base')
    Launcher.AddComponent(mc.MC106([0,0,0]), 'Pillar')
    Launcher.AddComponent(mc.MC071([0,0,90-angle]), 'Main arm')
    Launcher.AddComponent(mc.MC004([0,90,-angle]), 'Launch plate')
    Launcher.AddComponent(mc.MC001([0,90,180-angle]), 'Stop plate')
    Launcher.AddComponent(mc.MC013([90,0,0]), 'Rotation pole out') # Appearance only
    Launcher.AddComponent(mc.MC013([90,0,0]), 'Rotation pole in') # Appearance only

    # Example of how to find the reference point
    # by pulling arm back before aiming
    rc = [0.0, 1.19, 0.225]
    arm = [1.425,0.15,0]
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
    Launcher.ConnectComponents('Pillar', 'A', 'Main arm', 'B', 0.025) # Here, the 0.025 is to leave space between
    Launcher.ConnectComponents('Main arm', 'F', 'Launch plate', 'E')
    Launcher.ConnectComponents('Launch plate', 'A', 'Stop plate', 'A')
    Launcher.ConnectComponents('Launch plate', 'B', 'Stop plate', 'B')
    Launcher.ConnectComponents('Main arm', 'A', 'Rotation pole out', 'B')
    Launcher.ConnectComponents('Main arm', 'B', 'Rotation pole in', 'A')

    # To find the global coordinate of a link point, you can print it like this
    # print(Launcher.GetComponent('Main arm').GetLinkPointXYZ('B'))

    # To visualize where a link point is, you can use the DUMMY component
    Launcher.AddComponent(mc.DUMMY(), 'Dummy')
    Launcher.ConnectComponents('Base', 'A', 'Dummy', 'A')

    Launcher.SetSpring('Base', 'A', 'Main arm', 'C', 1.15, 17500)
# 
    Launcher.Fixate('Main arm')
    return Launcher
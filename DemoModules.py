from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses.MiroModule import Module as MiroModule
from MiroClasses.MiroComponent import MiroComponent
import numpy as np

from src import Components
from src import Boosters
from src import Sensors

try:
    import CustomComponents_local as CustomComponents
except:
    import CustomComponents

### LANDER BOX
# To learn how to modify the Lander, start by changing the components for the
# Bottom and Top plates on lines 31 and 32 to change the Lander dimension.
# Then change the rods on lines 36-39 to another component model to see how 
# the lander changes. 
def DemoLander(args):
    aim = args[0]
    tilt = -args[1]
    Lander = MiroModule('Landing Box')

    # Add top and bottom plates
    # MC component arguments are rotation, position and fixed (true/false)
    # Defaults to [0,0,0], [0,0,0], False if arguments are not provided
    # Note: Use Lander.RotateX, Y or Z if you are making several rotations to
    #       a component, as the order the rotations are made in is significant. 
    Lander.AddComponent(Components.MC035([  0, 90, 0], [0,0,0], False), 'Bottom plate')
    Lander.AddComponent(Components.MC035([180, 90, 0]), 'Top plate')

    # Add vertical rods
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod A')
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod B')
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod C')
    Lander.AddComponent(Components.MC113([ 0, 0, 90]), 'Rod D')
    
    # Add a sensor to the module.
    # We need to flip it upside down as with the Top Plate.
    # This can be done after adding it to the module by .RotateX()
    Lander.AddSensor(Sensors.MSA02([ 0, 0, 0]), 'Accelerometer')
    Lander.RotateX('Accelerometer', 180)

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


### CATAPULT LAUNCHER
# To learn how to modify the Launcher, start by changing the component 'Main arm' on line 26
# to one of different length and calibrate the spring constant on line 77. 
# The Launcher can hit the target with modifications to only these two things.
def DemoLauncher(args):
    # Extract arguments into local variables
    aim = args[0]
    angle = args[1]

    # Start by creating a new module
    Launcher = MiroModule('Catapult')

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


### Little robot
def DemoRobot1():
    MyRobot = MiroModule('MyRobot')

    # Add body components
    MyRobot.AddComponent(Components.MC035(), 'Base')
    MyRobot.AddComponent(Components.MC093(), 'Top')
    MyRobot.RotateX('Top', 180)
    
    # Connect the components. The first remains in position, and the second component is moved to match
    MyRobot.ConnectComponents('Base', 'A', 'Top', 'A')
    MyRobot.ConnectComponents('Base', 'C', 'Top', 'B')

    # Add left wheel components
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Left, Back')
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Left, Front')
    MyRobot.RotateX(['Wheel: Left, Front', 'Wheel: Left, Back'], 90)
 
    # Attach the left wheels
    MyRobot.ConnectComponents('Base', 'G', 'Wheel: Left, Back', 'A')
    MyRobot.ConnectComponents('Base', 'F', 'Wheel: Left, Front', 'A')

    # # Add right wheel components
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Right, Back')
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Right, Front')
    MyRobot.RotateX(['Wheel: Right, Front', 'Wheel: Right, Back'], -90)

    # Attach the right wheels
    MyRobot.ConnectComponents('Base', 'I', 'Wheel: Right, Back', 'A')
    MyRobot.ConnectComponents('Base', 'H', 'Wheel: Right, Front', 'A')
    
    # Set custom textures
    # MyRobot.SetTexture(['Base', 'Top'], 'mirobooster.png', [1,1])
    # MyRobot.SetTexture(['Wheel: Left, Back', 'Wheel: Left, Back', 'Wheel: Left, Back', 'Wheel: Left, Back'], 'woodwheel.png', [1,1])

    # Save the robot layout to enable generating a map using NodeMap
    MyRobot.CreateModuleMap()

    return MyRobot
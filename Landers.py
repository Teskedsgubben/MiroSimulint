import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

from MiroClasses import MiroModule as mm

from src import Components as Comp

def DemoLander(args):
    aim = args[0]
    tilt = -args[1]
    Lander = mm.Module()

    # Add top and bottom plates
    # MC component arguments are rotation, position and fixed (true/false)
    # Defaults to [0,0,0], [0,0,0], False if arguments are not provided
    Lander.AddComponent(Comp.MC035([  0,90,0], [0,0,0], False), 'Bottom plate')
    Lander.AddComponent(Comp.MC035([180,90,0]), 'Top plate')

    # Add vertical rods
    Lander.AddComponent(Comp.MC113([0, 0, 90]), 'Rod A')
    Lander.AddComponent(Comp.MC113([0, 0, 90]), 'Rod B')
    Lander.AddComponent(Comp.MC113([0, 0, 90]), 'Rod C')
    Lander.AddComponent(Comp.MC113([0, 0, 90]), 'Rod D')

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

    # DemoLander.Fixate('Bottom plate')
    # DemoLander.AddComponent(mc.MC044([0,deg,0]), 'Chute')
    # DemoLander.ChuteUp('Top plate', 'E', 'Chute')

    return Lander


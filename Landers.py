import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

from MiroClasses import MiroModule as mm

from src import Components as mc

def DemoLander(args):
    aim = args[0]
    tilt = -args[1]
    Lander = mm.Module()

    # Add top and bottom plates
    # MC001 arguments are rotation, position and fixed (true/false)
    # Defaults to [0,0,0], [0,0,0], False if arguments are not provided
    Lander.AddComponent(mc.MC001([  0,90,0], [0,0,0], False), 'Bottom plate')
    Lander.AddComponent(mc.MC001([180,90,0]), 'Top plate')

    # Add vertical rods
    Lander.AddComponent(mc.MC002([0,90,0]), 'Rod A')
    Lander.AddComponent(mc.MC002([0,90,0]), 'Rod B')
    Lander.AddComponent(mc.MC002([0,90,0]), 'Rod C')
    Lander.AddComponent(mc.MC002([0,90,0]), 'Rod D')

    Lander.RotateComponentsZ(tilt)
    Lander.RotateComponentsY(aim)

    # Connect Rods to bottom plate
    # It connects the first component to the second by
    # moving the second component to the right location
    Lander.ConnectComponents('Bottom plate', 'A', 'Rod A', 'B')
    Lander.ConnectComponents('Bottom plate', 'B', 'Rod B', 'B')
    Lander.ConnectComponents('Bottom plate', 'C', 'Rod C', 'B')
    Lander.ConnectComponents('Bottom plate', 'D', 'Rod D', 'B')

    # Connect Top plate to rods (order is significant)
    Lander.ConnectComponents('Rod A', 'A', 'Top plate', 'C')
    Lander.ConnectComponents('Rod B', 'A', 'Top plate', 'D')
    Lander.ConnectComponents('Rod C', 'A', 'Top plate', 'A')
    Lander.ConnectComponents('Rod D', 'A', 'Top plate', 'B')

    # DemoLander.Fixate('Bottom plate')
    # DemoLander.AddComponent(mc.MC044([0,deg,0]), 'Chute')
    # DemoLander.ChuteUp('Top plate', 'E', 'Chute')

    return Lander


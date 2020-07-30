import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms
import MiroModule as mm
import Components as mc


deg = -45
DemoLander = mm.Module()

# Add top and bottom plates
# MC001 arguments are rotation, position and fixed (true/false)
# Defaults to [0,0,0], [0,0,0], False if arguments are not provided
DemoLander.AddComponent(mc.MC001([  0,deg,0], [0,0,0], False), 'Bottom plate')
DemoLander.AddComponent(mc.MC001([180,deg,0]), 'Top plate')

# Add vertical rods
DemoLander.AddComponent(mc.MC002([0,deg,0]), 'Rod A')
DemoLander.AddComponent(mc.MC002([0,deg,0]), 'Rod B')
DemoLander.AddComponent(mc.MC002([0,deg,0]), 'Rod C')
DemoLander.AddComponent(mc.MC002([0,deg,0]), 'Rod D')

# Connect Rods to bottom plate
# It connects the first component to the second by
# moving the second component to the right location
DemoLander.ConnectComponents('Bottom plate', 'A', 'Rod A', 'B')
DemoLander.ConnectComponents('Bottom plate', 'B', 'Rod B', 'B')
DemoLander.ConnectComponents('Bottom plate', 'C', 'Rod C', 'B')
DemoLander.ConnectComponents('Bottom plate', 'D', 'Rod D', 'B')

# Connect Top plate to rods (order is significant)
DemoLander.ConnectComponents('Rod A', 'A', 'Top plate', 'C')
DemoLander.ConnectComponents('Rod B', 'A', 'Top plate', 'D')
DemoLander.ConnectComponents('Rod C', 'A', 'Top plate', 'A')
DemoLander.ConnectComponents('Rod D', 'A', 'Top plate', 'B')


# DemoLander.AddComponent(mc.MC044([0,deg,0]), 'Chute')
# DemoLander.ChuteUp('Top plate', 'E', 'Chute')


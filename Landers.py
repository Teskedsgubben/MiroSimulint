import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms
import MiroModule as mm
import Components as mc


deg = -25
DemoLander = mm.Module()

# Add top and bottom plates
DemoLander.AddComponent(mc.MC001([0,deg,0], [0,0,0], False), 'Bottom plate')
DemoLander.AddComponent(mc.MC001([180,deg,0], [0,0,0], False), 'Top plate')

# Add vertical rods
DemoLander.AddComponent(mc.MC002([0,deg,0], [0,0,0], False), 'Rod A')
DemoLander.AddComponent(mc.MC002([0,deg,0], [0,0,0], False), 'Rod B')
DemoLander.AddComponent(mc.MC002([0,deg,0], [0,0,0], False), 'Rod C')
DemoLander.AddComponent(mc.MC002([0,deg,0], [0,0,0], False), 'Rod D')

# Connect Rods to bottom plate
DemoLander.ConnectComponents('Bottom plate', 'A', 'Rod A', 'B')
DemoLander.ConnectComponents('Bottom plate', 'B', 'Rod B', 'B')
DemoLander.ConnectComponents('Bottom plate', 'C', 'Rod C', 'B')
DemoLander.ConnectComponents('Bottom plate', 'D', 'Rod D', 'B')

# Connect Top plate to rods (order is significant)
DemoLander.ConnectComponents('Rod A', 'A', 'Top plate', 'C')
DemoLander.ConnectComponents('Rod B', 'A', 'Top plate', 'D')
DemoLander.ConnectComponents('Rod C', 'A', 'Top plate', 'A')
DemoLander.ConnectComponents('Rod D', 'A', 'Top plate', 'B')

DemoLander.Move([10.5,7,0])
DemoLander.SetVelocity([-6.5,3,0])

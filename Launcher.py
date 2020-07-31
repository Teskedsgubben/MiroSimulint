import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms
import MiroModule as mm
import Components as mc


aim = 0
Launcher = mm.Module()

# # Add top and bottom plates
# # MC001 arguments are rotation, position and fixed (true/false)
# # Defaults to [0,0,0], [0,0,0], False if arguments are not provided
# Launcher.AddComponent(mc.MC001([  0,aim,0], [0,0,0], False), 'Bottom plate')
# Launcher.AddComponent(mc.MC001([180,aim,0]), 'Top plate')

# # Add vertical rods
# Launcher.AddComponent(mc.MC002([0,aim,0]), 'Rod A')
# Launcher.AddComponent(mc.MC002([0,aim,0]), 'Rod B')
# Launcher.AddComponent(mc.MC002([0,aim,0]), 'Rod C')
# Launcher.AddComponent(mc.MC002([0,aim,0]), 'Rod D')

# # Connect Rods to bottom plate
# # It connects the first component to the second by
# # moving the second component to the right location
# Launcher.ConnectComponents('Bottom plate', 'A', 'Rod A', 'B')
# Launcher.ConnectComponents('Bottom plate', 'B', 'Rod B', 'B')
# Launcher.ConnectComponents('Bottom plate', 'C', 'Rod C', 'B')
# Launcher.ConnectComponents('Bottom plate', 'D', 'Rod D', 'B')

# # Connect Top plate to rods (order is significant)
# Launcher.ConnectComponents('Rod A', 'A', 'Top plate', 'C')
# Launcher.ConnectComponents('Rod B', 'A', 'Top plate', 'D')
# Launcher.ConnectComponents('Rod C', 'A', 'Top plate', 'A')
# Launcher.ConnectComponents('Rod D', 'A', 'Top plate', 'B')



Launcher.AddComponent(mc.MC106([0,aim,0]), 'Base')
Launcher.AddComponent(mc.MC071([0,aim,-45]), 'Main arm')

Launcher.ConnectComponents('Base', 'A', 'Main arm', 'B')

# Launcher.SetSpring('Base', 'E', 'Rod E', 'A', 1, 50)

Launcher.Fixate('Main arm')
# start_position = [10.5,8.5,0]

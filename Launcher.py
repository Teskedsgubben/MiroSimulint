import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms
import MiroModule as mm
import Components as mc


aim = 0
angle = 10

Launcher = mm.Module()

Launcher.AddComponent(mc.MC007([0,aim,0]), 'Base')
Launcher.AddComponent(mc.MC106([0,aim,0]), 'Pillar')
Launcher.AddComponent(mc.MC071([0,aim,90-angle]), 'Main arm')
Launcher.AddComponent(mc.MC001([0,90+aim,-angle]), 'Launch plate')
Launcher.AddComponent(mc.MC001([0,90+aim,180-angle]), 'Stop plate')
Launcher.AddComponent(mc.MC013([90,0,0]), 'Rotation pole') # Appearance only

Launcher.ConnectComponents('Base', 'E', 'Pillar', 'C')
Launcher.ConnectComponents('Pillar', 'A', 'Main arm', 'B')
Launcher.ConnectComponents('Main arm', 'F', 'Launch plate', 'E')
Launcher.ConnectComponents('Launch plate', 'A', 'Stop plate', 'A')
Launcher.ConnectComponents('Launch plate', 'B', 'Stop plate', 'B')
Launcher.ConnectComponents('Main arm', 'A', 'Rotation pole', 'A')


# Launcher.AddComponent(mc.MC002([0,aim,0]), 'Dummy')
# Launcher.ConnectComponents('Main arm', 'F', 'Dummy', 'B')



Launcher.SetSpring('Base', 'B', 'Main arm', 'C', 0.65, 2050)

Launcher.Fixate('Main arm')
# start_position = [10.5,8.5,0]

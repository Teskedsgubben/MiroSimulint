import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms
import MiroModule as mm
import Components as mc



DemoLander = mm.Module()

deg = 30
DemoLander.AddComponent(mc.MC_0([0,deg,0], [0,0,0], True), 'Fixed Block')
DemoLander.AddComponent(mc.MC_0([0,180+deg,0], [0,0,0], False), 'Free Block')

DemoLander.ConnectComponents('Fixed Block', 'A', 'Free Block', 'A')


DemoLander.Move([1.75,3,-0.56])

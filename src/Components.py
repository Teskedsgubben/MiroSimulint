from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses import MiroComponent as mc
import numpy as np

density = {
    'ABS': 950,
    'PVC': 1380,
    'Aluminium': 2700,
    'Steel Forged Concrete': 5000,
}

# This is a sphere to help visualization of certain points
def DUMMY(rot = [0,0,0], pos = [0,0,0], Fixed = False, radius = 0.025):
    body_ball = MiroAPI.add_sphereShape(False, radius, pos, texture='test_texture.png', scale=[0.07,0.07], Collide=False)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_ball)
    COMPONENT.AddLinkPoint('A', [ 0, 0, 0], [0, 0, 0])
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

############### MC0XX ###############
# Plate with mounting sockets in corners on one side
def MC0XX(M1, M2, M3, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = M1
    size_y = M3
    size_z = M2
    density_brick = density['ABS']   # kg/m^3
    body_brick = MiroAPI.add_boxShape(False, size_x, size_y, size_z, pos, texture='MITstol.jpg', density=density_brick, Fixed=Fixed)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    # Top
    COMPONENT.AddLinkPoint('A', [0, 1, 0], [ (size_x/2-0.02),  size_y/2,  (size_z/2-0.02)])
    COMPONENT.AddLinkPoint('B', [0, 1, 0], [-(size_x/2-0.02),  size_y/2,  (size_z/2-0.02)])
    COMPONENT.AddLinkPoint('C', [0, 1, 0], [ (size_x/2-0.02),  size_y/2, -(size_z/2-0.02)])
    COMPONENT.AddLinkPoint('D', [0, 1, 0], [-(size_x/2-0.02),  size_y/2, -(size_z/2-0.02)])
    # Bottom
    COMPONENT.AddLinkPoint('E', [0,-1, 0], [ 0, -size_y/2, 0])
    # Sides
    COMPONENT.AddLinkPoint('F', [0, 0,-1], [-(size_x/2-0.02),  0,-size_z/2])
    COMPONENT.AddLinkPoint('G', [0, 0,-1], [ (size_x/2-0.02),  0,-size_z/2])
    COMPONENT.AddLinkPoint('H', [0, 0, 1], [-(size_x/2-0.02),  0, size_z/2])
    COMPONENT.AddLinkPoint('I', [0, 0, 1], [ (size_x/2-0.02),  0, size_z/2])
    COMPONENT.AddLinkPoint('J', [-1, 0,0], [-size_x/2,  0, 0])
    COMPONENT.AddLinkPoint('K', [ 1, 0,0], [ size_x/2,  0, 0])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# MC01X
def MC011(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.08, 0.02, rot, pos, Fixed)
def MC012(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.08, 0.02, rot, pos, Fixed)
def MC013(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.08, 0.02, rot, pos, Fixed)
def MC014(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.08, 0.02, rot, pos, Fixed)
def MC015(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.08, 0.02, rot, pos, Fixed)

# MC02X
def MC021(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.12, 0.02, rot, pos, Fixed)
def MC022(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.12, 0.02, rot, pos, Fixed)
def MC023(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.12, 0.02, rot, pos, Fixed)
def MC024(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.12, 0.02, rot, pos, Fixed)
def MC025(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.12, 0.02, rot, pos, Fixed)

# MC03X
def MC031(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.16, 0.02, rot, pos, Fixed)
def MC032(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.16, 0.02, rot, pos, Fixed)
def MC033(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.16, 0.02, rot, pos, Fixed)
def MC034(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.16, 0.02, rot, pos, Fixed)
def MC035(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.16, 0.02, rot, pos, Fixed)

# MC04X
def MC041(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.20, 0.02, rot, pos, Fixed)
def MC042(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.20, 0.02, rot, pos, Fixed)
def MC043(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.20, 0.02, rot, pos, Fixed)
def MC044(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.20, 0.02, rot, pos, Fixed)
def MC045(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.20, 0.02, rot, pos, Fixed)

# MC05X
def MC051(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.24, 0.02, rot, pos, Fixed)
def MC052(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.24, 0.02, rot, pos, Fixed)
def MC053(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.24, 0.02, rot, pos, Fixed)
def MC054(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.24, 0.02, rot, pos, Fixed)
def MC055(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.24, 0.02, rot, pos, Fixed)

# MC09X
def MC091(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.08, 0.06, rot, pos, Fixed)
def MC092(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.12, 0.06, rot, pos, Fixed)
def MC093(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.16, 0.06, rot, pos, Fixed)
def MC094(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.20, 0.06, rot, pos, Fixed)
def MC095(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.24, 0.06, rot, pos, Fixed)

############### MC1XX ###############
# Mounting rod
def MC1XX(M1, M2, M3, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = M1
    size_y = M2
    size_z = M2

    density_brick = density['Aluminium']   # kg/m^3
    body_brick = MiroAPI.add_boxShape(False, size_x, size_y, size_z, pos, texture='brushsteel.jpg', density=density_brick, Fixed=Fixed)
    
    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [-1, 0, 0], [-size_x/2, 0, 0])
    COMPONENT.AddLinkPoint('B', [ 1, 0, 0], [ size_x/2, 0, 0])
    COMPONENT.AddLinkPoint('C', [ 0, 0,-1], [ 0, 0,-size_z/2])
    COMPONENT.AddLinkPoint('D', [ 0, 0, 1], [ 0, 0, size_z/2])
    COMPONENT.AddLinkPoint('E', [ 0,-1, 0], [-(size_x/2-M3),-size_y/2, 0])
    COMPONENT.AddLinkPoint('F', [ 0,-1, 0], [ (size_x/2-M3),-size_y/2, 0])
    COMPONENT.AddLinkPoint('G', [ 0, 1, 0], [-(size_x/2-M3), size_y/2, 0])
    COMPONENT.AddLinkPoint('H', [ 0, 1, 0], [ (size_x/2-M3), size_y/2, 0])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# MC11X
def MC111(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.08, 0.02, 0.02, rot, pos, Fixed)
def MC112(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.12, 0.02, 0.02, rot, pos, Fixed)
def MC113(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.16, 0.02, 0.02, rot, pos, Fixed)
def MC114(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.20, 0.02, 0.02, rot, pos, Fixed)
def MC115(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.24, 0.02, 0.02, rot, pos, Fixed)

# MC12X
def MC121(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.16, 0.04, 0.04, rot, pos, Fixed)
def MC122(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.20, 0.04, 0.04, rot, pos, Fixed)
def MC123(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.24, 0.04, 0.04, rot, pos, Fixed)
def MC124(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.36, 0.04, 0.04, rot, pos, Fixed)
def MC125(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.48, 0.04, 0.04, rot, pos, Fixed)

# MC13X
def MC131(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.50, 0.06, 0.08, rot, pos, Fixed)
def MC132(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(0.75, 0.06, 0.08, rot, pos, Fixed)
def MC133(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(1.00, 0.06, 0.08, rot, pos, Fixed)
def MC134(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(1.25, 0.06, 0.08, rot, pos, Fixed)
def MC135(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(1.50, 0.06, 0.08, rot, pos, Fixed)

# MC14X
def MC141(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(1.0, 0.08, 0.12, rot, pos, Fixed)
def MC142(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(1.5, 0.08, 0.12, rot, pos, Fixed)
def MC143(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(2.0, 0.08, 0.12, rot, pos, Fixed)
def MC144(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(2.5, 0.08, 0.12, rot, pos, Fixed)
def MC145(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC1XX(3.0, 0.08, 0.12, rot, pos, Fixed)

############### MC2XX ###############
# Disk
def MC2XX(M1, M2, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_h = M1
    size_r = M2
    density_brick = density['ABS']   # kg/m^3

    body_brick = MiroAPI.add_cylinderShape(False, size_r, size_h, density_brick, pos, Fixed=False, texture='MITstol.jpg')
    
    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [ 0, 1, 0], [0, size_h/2, 0])
    COMPONENT.AddLinkPoint('B', [ 0,-1, 0], [0,-size_h/2, 0])
    COMPONENT.AddLinkPoint('C', [ 1, 0, 0], [ size_r, 0, 0])
    COMPONENT.AddLinkPoint('D', [-1, 0, 0], [-size_r, 0, 0])
    COMPONENT.AddLinkPoint('E', [ 0, 0, 1], [ 0, 0, size_r])
    COMPONENT.AddLinkPoint('F', [ 0, 0,-1], [ 0, 0,-size_r])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

def MC211(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.025, 0.01, rot, pos, Fixed)
def MC212(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.05, 0.01, rot, pos, Fixed)
def MC213(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.01, rot, pos, Fixed)
def MC214(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.12, 0.01, rot, pos, Fixed)
def MC215(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.16, 0.01, rot, pos, Fixed)

def MC221(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.025, 0.02, rot, pos, Fixed)
def MC222(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.05, 0.02, rot, pos, Fixed)
def MC223(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.02, rot, pos, Fixed)
def MC224(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.12, 0.02, rot, pos, Fixed)
def MC225(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.16, 0.02, rot, pos, Fixed)

def MC231(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.025, 0.04, rot, pos, Fixed)
def MC232(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.05, 0.04, rot, pos, Fixed)
def MC233(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.04, rot, pos, Fixed)
def MC234(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.12, 0.04, rot, pos, Fixed)
def MC235(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.16, 0.04, rot, pos, Fixed)

def MC241(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.02, 0.04/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC242(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.02, 0.08/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC243(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.02, 0.12/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC244(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.02, 0.16/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC245(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.02, 0.20/np.sqrt(2)-0.01, rot, pos, Fixed)

def MC251(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.04, 0.04/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC252(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.04, 0.08/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC253(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.04, 0.12/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC254(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.04, 0.16/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC255(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.04, 0.20/np.sqrt(2)-0.01, rot, pos, Fixed)

def MC261(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.04/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC262(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.08/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC263(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.12/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC264(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.16/np.sqrt(2)-0.01, rot, pos, Fixed)
def MC265(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC2XX(0.08, 0.20/np.sqrt(2)-0.01, rot, pos, Fixed)

############### MC3XX ###############
# Small PVC connector
def MC3XX(M1, M2, M3, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = M1
    size_y = M3
    size_z = M2

    density_brick = density['PVC']   # kg/m^3
    body_brick = MiroAPI.add_boxShape(False, size_x, size_y, size_z, pos, texture='pvc_weave_brown.png', density=density_brick, Fixed=Fixed)
    
    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [-1, 0, 0], [-size_x/2, 0, 0])
    COMPONENT.AddLinkPoint('B', [ 1, 0, 0], [ size_x/2, 0, 0])
    COMPONENT.AddLinkPoint('C', [ 0, 0,-1], [ 0, 0,-size_z/2])
    COMPONENT.AddLinkPoint('D', [ 0, 0, 1], [ 0, 0, size_z/2])
    COMPONENT.AddLinkPoint('E', [ 0,-1, 0], [ 0,-size_y/2, 0])
    COMPONENT.AddLinkPoint('F', [ 0, 1, 0], [ 0, size_y/2, 0])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT


# MC31X
def MC311(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.005, 0.005, 0.005, rot, pos, Fixed)
def MC312(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.01, 0.005, 0.005, rot, pos, Fixed)
def MC313(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.02, 0.005, 0.005, rot, pos, Fixed)
def MC314(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.04, 0.005, 0.005, rot, pos, Fixed)
def MC315(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.06, 0.005, 0.005, rot, pos, Fixed)


def MC321(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.005, 0.01, 0.01, rot, pos, Fixed)
def MC322(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.01, 0.01, 0.01, rot, pos, Fixed)
def MC323(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.02, 0.01, 0.01, rot, pos, Fixed)
def MC324(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.04, 0.01, 0.01, rot, pos, Fixed)
def MC325(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.06, 0.01, 0.01, rot, pos, Fixed)
def MC326(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.08, 0.01, 0.01, rot, pos, Fixed)
def MC327(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.10, 0.01, 0.01, rot, pos, Fixed)


def MC333(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.02, 0.02, 0.01, rot, pos, Fixed)
def MC334(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.04, 0.02, 0.01, rot, pos, Fixed)
def MC335(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.06, 0.02, 0.01, rot, pos, Fixed)
def MC336(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.08, 0.02, 0.01, rot, pos, Fixed)
def MC337(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC3XX(0.10, 0.02, 0.01, rot, pos, Fixed)


############### MC4XX ###############
# Protective cover plate
def MC4XX(M1, M2, M3, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = M1
    size_y = M2 + 0.02
    size_z = M3 + 0.02

    density_brick = density['PVC']   # kg/m^3
    body_brick = MiroAPI.add_boxShape(False, size_x, size_y, size_z, pos, texture='pvc_weave_brown.png', density=density_brick, Fixed=Fixed)
    
    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [ 0, 0, 1], [ size_x/2,-(size_y/2-0.01),-(size_z/2-0.01)])
    COMPONENT.AddLinkPoint('B', [ 0, 0, 1], [ size_x/2,-(size_y/2-0.01),               0])
    COMPONENT.AddLinkPoint('C', [ 0, 0, 1], [ size_x/2,-(size_y/2-0.01), (size_z/2-0.01)])
    COMPONENT.AddLinkPoint('D', [ 0, 0, 1], [ size_x/2,               0,-(size_z/2-0.01)])
    COMPONENT.AddLinkPoint('E', [ 0, 0, 1], [ size_x/2,               0,               0])
    COMPONENT.AddLinkPoint('F', [ 0, 0, 1], [ size_x/2,               0, (size_z/2-0.01)])
    COMPONENT.AddLinkPoint('G', [ 0, 0, 1], [ size_x/2, (size_y/2-0.01),-(size_z/2-0.01)])
    COMPONENT.AddLinkPoint('H', [ 0, 0, 1], [ size_x/2, (size_y/2-0.01),               0])
    COMPONENT.AddLinkPoint('I', [ 0, 0, 1], [ size_x/2, (size_y/2-0.01), (size_z/2-0.01)])

    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# MC41X
def MC411(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.06, rot, pos, Fixed)
def MC412(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.08, rot, pos, Fixed)
def MC413(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.10, rot, pos, Fixed)
def MC414(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.12, rot, pos, Fixed)
def MC415(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.14, rot, pos, Fixed)
def MC416(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.16, rot, pos, Fixed)
def MC417(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.18, rot, pos, Fixed)
def MC418(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.20, rot, pos, Fixed)
def MC419(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.06, 0.22, rot, pos, Fixed)

def MC422(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.08, rot, pos, Fixed)
def MC423(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.10, rot, pos, Fixed)
def MC424(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.12, rot, pos, Fixed)
def MC425(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.14, rot, pos, Fixed)
def MC426(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.16, rot, pos, Fixed)
def MC427(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.18, rot, pos, Fixed)
def MC428(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.20, rot, pos, Fixed)
def MC429(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.08, 0.22, rot, pos, Fixed)

def MC433(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.10, rot, pos, Fixed)
def MC434(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.12, rot, pos, Fixed)
def MC435(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.14, rot, pos, Fixed)
def MC436(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.16, rot, pos, Fixed)
def MC437(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.18, rot, pos, Fixed)
def MC438(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.20, rot, pos, Fixed)
def MC439(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.10, 0.22, rot, pos, Fixed)

def MC444(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.12, 0.12, rot, pos, Fixed)
def MC445(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.12, 0.14, rot, pos, Fixed)
def MC446(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.12, 0.16, rot, pos, Fixed)
def MC447(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.12, 0.18, rot, pos, Fixed)
def MC448(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.12, 0.20, rot, pos, Fixed)
def MC449(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.12, 0.22, rot, pos, Fixed)

def MC455(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.14, 0.14, rot, pos, Fixed)
def MC456(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.14, 0.16, rot, pos, Fixed)
def MC457(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.14, 0.18, rot, pos, Fixed)
def MC458(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.14, 0.20, rot, pos, Fixed)
def MC459(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.14, 0.22, rot, pos, Fixed)

def MC466(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.16, 0.16, rot, pos, Fixed)
def MC467(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.16, 0.18, rot, pos, Fixed)
def MC468(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.16, 0.20, rot, pos, Fixed)
def MC469(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.16, 0.22, rot, pos, Fixed)

def MC477(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.18, 0.18, rot, pos, Fixed)
def MC478(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.18, 0.20, rot, pos, Fixed)
def MC479(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.18, 0.22, rot, pos, Fixed)

def MC488(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.20, 0.20, rot, pos, Fixed)
def MC489(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.20, 0.22, rot, pos, Fixed)

def MC499(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC4XX(0.005, 0.22, 0.22, rot, pos, Fixed)

############### MC5XX ###############
# Ball
def MC5XX(M1, M2, M3, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    '''Ellipsoid component, ABS plastic.\n
    M1 = radius in x\n 
    M2 = radius in y\n
    M3 = radius in z\n
    Linkpoints: A: +x, B: -x, C: +y, D: -y, E: +z, F: -z.'''
    size_rx = M1
    size_ry = M2
    size_rz = M3
    density_brick = density['ABS']   # kg/m^3
    
    body_ball = MiroAPI.add_ellipsoidShape(False, size_rx, size_ry, size_rz, pos, texture='test_texture.png', scale=[0.07,0.07], Collide=False, density=density_brick)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_ball)

    COMPONENT.AddLinkPoint('A', [ 1, 0, 0], [ size_rx, 0, 0])
    COMPONENT.AddLinkPoint('B', [-1, 0, 0], [-size_rx, 0, 0])
    COMPONENT.AddLinkPoint('C', [ 0, 1, 0], [ 0, size_ry, 0])
    COMPONENT.AddLinkPoint('D', [ 0,-1, 0], [ 0, size_ry, 0])
    COMPONENT.AddLinkPoint('E', [ 0, 0, 1], [ 0, 0, size_rz])
    COMPONENT.AddLinkPoint('F', [ 0, 0,-1], [ 0, 0,-size_rz])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT


# Big fat thunk
def MC906(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = 0.8
    size_y = 0.8
    size_z = 0.6
    density_brick = density['Steel Forged Concrete']   # kg/m^3
    body_brick = MiroAPI.add_boxShape(False, size_x, size_y, size_z, pos, texture='white_bricks.jpg', density=density_brick, Fixed=Fixed)
    
    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [0, 0, 1], [0, 0.9*size_y/2,  size_z/2])
    COMPONENT.AddLinkPoint('B', [0, 0,-1], [0, 0.9*size_y/2, -size_z/2])

    # Bottom mounting sockets
    COMPONENT.AddLinkPoint('C', [0,-1, 0], [0,-size_y/2,  size_z/4])
    COMPONENT.AddLinkPoint('D', [0,-1, 0], [0,-size_y/2, -size_z/4])
    
    # Top mounting sockets
    COMPONENT.AddLinkPoint('E', [0, 1, 0], [0, size_y/2,  size_z/4])
    COMPONENT.AddLinkPoint('F', [0, 1, 0], [0, size_y/2, -size_z/4])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# BIG Plate with mounting sockets in corners on one side
def MC907(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = 0.8
    size_y = 0.1
    size_z = 0.9
    density_brick = density['Steel Forged Concrete']    # kg/m^3
    body_brick = MiroAPI.add_boxShape(False, size_x, size_y, size_z, pos, texture='white_bricks.jpg', density=density_brick, Fixed=Fixed)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [0, 1, 0], [ 3*size_x/8,  size_y/2,  3*size_z/8])
    COMPONENT.AddLinkPoint('B', [0, 1, 0], [-3*size_x/8,  size_y/2,  3*size_z/8])
    COMPONENT.AddLinkPoint('C', [0, 1, 0], [ 3*size_x/8,  size_y/2, -3*size_z/8])
    COMPONENT.AddLinkPoint('D', [0, 1, 0], [-3*size_x/8,  size_y/2, -3*size_z/8])
    COMPONENT.AddLinkPoint('E', [0, 1, 0], [          0,  size_y/2,           0])
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT
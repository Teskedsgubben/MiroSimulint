import pychrono.core as chrono
import numpy as np

from MiroClasses import MiroComponent as mc

# This is a sphere to help visualization of certain points
def DUMMY(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    body_ball = chrono.ChBody()
    body_ball.SetBodyFixed(Fixed)
    body_ball.SetCollide(False)  

    # Visualization shape, for rendering animation
    body_ball_shape = chrono.ChSphereShape(chrono.ChSphere(chrono.ChVectorD(0, 0, 0), 0.025))
    body_ball.AddAsset(body_ball_shape)

    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/test_texture.png'))
    texture.SetTextureScale(0.07, 0.07)
    body_ball.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_ball)
    COMPONENT.AddLinkPoint('A', [ 0, 1, 0], chrono.ChVectorD(0, 0, 0))
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

############### MC0XX ###############
# Plate with mounting sockets in corners on one side
def MC0XX(size_x, size_y, size_z, rot, pos, Fixed):
    density_brick = 950   # kg/m^3
    mass_brick = density_brick * size_x * size_y * size_z

    inertia_brick_xx = (size_y**2 + size_z**2)*mass_brick/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass_brick/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))     

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITstol.jpg'))
    texture.SetTextureScale(1, 1)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    # Top
    COMPONENT.AddLinkPoint('A', [0, 1, 0], chrono.ChVectorD( (size_x/2-0.02),  size_y/2,  (size_z/2-0.02)))
    COMPONENT.AddLinkPoint('B', [0, 1, 0], chrono.ChVectorD(-(size_x/2-0.02),  size_y/2,  (size_z/2-0.02)))
    COMPONENT.AddLinkPoint('C', [0, 1, 0], chrono.ChVectorD( (size_x/2-0.02),  size_y/2, -(size_z/2-0.02)))
    COMPONENT.AddLinkPoint('D', [0, 1, 0], chrono.ChVectorD(-(size_x/2-0.02),  size_y/2, -(size_z/2-0.02)))
    # Bottom
    COMPONENT.AddLinkPoint('E', [0,-1, 0], chrono.ChVectorD( 0, -size_y/2, 0))
    # Sides
    COMPONENT.AddLinkPoint('F', [0, 0,-1], chrono.ChVectorD(-(size_x/2-0.02),  0,-size_z/2))
    COMPONENT.AddLinkPoint('G', [0, 0,-1], chrono.ChVectorD( (size_x/2-0.02),  0,-size_z/2))
    COMPONENT.AddLinkPoint('H', [0, 0, 1], chrono.ChVectorD(-(size_x/2-0.02),  0, size_z/2))
    COMPONENT.AddLinkPoint('I', [0, 0, 1], chrono.ChVectorD( (size_x/2-0.02),  0, size_z/2))
    COMPONENT.AddLinkPoint('J', [-1, 0,0], chrono.ChVectorD(-size_x/2,  0, 0))
    COMPONENT.AddLinkPoint('K', [ 1, 0,0], chrono.ChVectorD( size_x/2,  0, 0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# MC01X
def MC011(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.03, 0.08, rot, pos, Fixed)
def MC012(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.03, 0.08, rot, pos, Fixed)
def MC013(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.03, 0.08, rot, pos, Fixed)
def MC014(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.03, 0.08, rot, pos, Fixed)
def MC015(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.03, 0.08, rot, pos, Fixed)

# MC02X
def MC021(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.03, 0.12, rot, pos, Fixed)
def MC022(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.03, 0.12, rot, pos, Fixed)
def MC023(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.03, 0.12, rot, pos, Fixed)
def MC024(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.03, 0.12, rot, pos, Fixed)
def MC025(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.03, 0.12, rot, pos, Fixed)

# MC03X
def MC031(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.03, 0.16, rot, pos, Fixed)
def MC032(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.03, 0.16, rot, pos, Fixed)
def MC033(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.03, 0.16, rot, pos, Fixed)
def MC034(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.03, 0.16, rot, pos, Fixed)
def MC035(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.03, 0.16, rot, pos, Fixed)

# MC04X
def MC041(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.03, 0.20, rot, pos, Fixed)
def MC042(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.03, 0.20, rot, pos, Fixed)
def MC043(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.03, 0.20, rot, pos, Fixed)
def MC044(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.03, 0.20, rot, pos, Fixed)
def MC045(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.03, 0.20, rot, pos, Fixed)

# MC05X
def MC051(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.03, 0.24, rot, pos, Fixed)
def MC052(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.03, 0.24, rot, pos, Fixed)
def MC053(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.03, 0.24, rot, pos, Fixed)
def MC054(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.03, 0.24, rot, pos, Fixed)
def MC055(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.03, 0.24, rot, pos, Fixed)

# MC09X
def MC091(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.08, 0.06, 0.08, rot, pos, Fixed)
def MC092(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.12, 0.06, 0.12, rot, pos, Fixed)
def MC093(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.16, 0.06, 0.16, rot, pos, Fixed)
def MC094(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.20, 0.06, 0.20, rot, pos, Fixed)
def MC095(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    return MC0XX(0.24, 0.06, 0.24, rot, pos, Fixed)

############### MC1XX ###############
# Mounting rod
def MC1XX(M1, M2, M3, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_x = M1
    size_y = M2
    size_z = M2

    density_brick = 2700   # kg/m^3
    mass_brick = density_brick * size_x * size_y * size_z
    inertia_brick_xx = (size_y**2 + size_z**2)*mass_brick/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass_brick/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)
    
    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/brushsteel.jpg'))
    texture.SetTextureScale(4, 3)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [-1, 0, 0], chrono.ChVectorD(-size_x/2, 0, 0))
    COMPONENT.AddLinkPoint('B', [ 1, 0, 0], chrono.ChVectorD( size_x/2, 0, 0))
    COMPONENT.AddLinkPoint('C', [ 0, 0,-1], chrono.ChVectorD( 0, 0,-size_z/2))
    COMPONENT.AddLinkPoint('D', [ 0, 0, 1], chrono.ChVectorD( 0, 0, size_z/2))
    COMPONENT.AddLinkPoint('E', [ 0,-1, 0], chrono.ChVectorD(-(size_x/2-M3),-size_y/2, 0))
    COMPONENT.AddLinkPoint('F', [ 0,-1, 0], chrono.ChVectorD( (size_x/2-M3),-size_y/2, 0))
    COMPONENT.AddLinkPoint('G', [ 0, 1, 0], chrono.ChVectorD(-(size_x/2-M3), size_y/2, 0))
    COMPONENT.AddLinkPoint('H', [ 0, 1, 0], chrono.ChVectorD( (size_x/2-M3), size_y/2, 0))
    
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
    density_brick = 1000   # kg/m^3

    body_brick = chrono.ChBodyEasyCylinder(size_r, size_h, density_brick)
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    # body_brick.SetMass(mass_brick)
    # body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddCylinder(size_r, size_r, size_h/2) # hemi sizes
    body_brick.GetCollisionModel().BuildModel()

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITstol.jpg'))
    texture.SetTextureScale(1, 1)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [ 0, 1, 0], chrono.ChVectorD(0, size_h/2, 0))
    COMPONENT.AddLinkPoint('B', [ 0,-1, 0], chrono.ChVectorD(0,-size_h/2, 0))
    COMPONENT.AddLinkPoint('C', [ 1, 0, 0], chrono.ChVectorD( size_r, 0, 0))
    COMPONENT.AddLinkPoint('D', [-1, 0, 0], chrono.ChVectorD(-size_r, 0, 0))
    COMPONENT.AddLinkPoint('E', [ 0, 0, 1], chrono.ChVectorD( 0, 0, size_r))
    COMPONENT.AddLinkPoint('F', [ 0, 0,-1], chrono.ChVectorD( 0, 0,-size_r))
    
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


# Big fat thunk
def MC106(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.8
    size_brick_y = 0.8
    size_brick_z = 0.6
    density_brick = 5000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = (size_brick_y**2 + size_brick_z**2)*mass_brick/3
    inertia_brick_yy = (size_brick_x**2 + size_brick_z**2)*mass_brick/3
    inertia_brick_zz = (size_brick_x**2 + size_brick_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.GetRot()
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white_bricks.jpg'))
    texture.SetTextureScale(4, 4)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [0, 0, 1], chrono.ChVectorD(0, 0.9*size_brick_y/2,  size_brick_z/2))
    COMPONENT.AddLinkPoint('B', [0, 0,-1], chrono.ChVectorD(0, 0.9*size_brick_y/2, -size_brick_z/2))
    
    # Bottom mounting sockets
    COMPONENT.AddLinkPoint('C', [0,-1, 0], chrono.ChVectorD(0, -size_brick_y/2,  size_brick_z/4))
    COMPONENT.AddLinkPoint('D', [0,-1, 0], chrono.ChVectorD(0, -size_brick_y/2, -size_brick_z/4))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# Long rod
def MC071(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.2
    size_brick_y = 2.5
    size_brick_z = 0.1
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = (size_brick_y**2 + size_brick_z**2)*mass_brick/3
    inertia_brick_yy = (size_brick_x**2 + size_brick_z**2)*mass_brick/3
    inertia_brick_zz = (size_brick_x**2 + size_brick_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_ikea_style.png'))
    texture.SetTextureScale(1, 10)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [0, 0, 1], chrono.ChVectorD(0, size_brick_y/8,  size_brick_z/2))
    COMPONENT.AddLinkPoint('B', [0, 0,-1], chrono.ChVectorD(0, size_brick_y/8, -size_brick_z/2))

    COMPONENT.AddLinkPoint('C', [-1, 0, 0], chrono.ChVectorD(-size_brick_x/2, 0.9*size_brick_y/2, 0))
    COMPONENT.AddLinkPoint('D', [ 1, 0, 0], chrono.ChVectorD( size_brick_x/2, 0.9*size_brick_y/2, 0))

    COMPONENT.AddLinkPoint('E', [-1, 0, 0], chrono.ChVectorD(-size_brick_x/2, -0.9*size_brick_y/2, 0))
    COMPONENT.AddLinkPoint('F', [ 1, 0, 0], chrono.ChVectorD( size_brick_x/2, -0.9*size_brick_y/2, 0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT


# BIG Plate with mounting sockets in corners on one side
def MC007(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.8
    size_brick_y = 0.1
    size_brick_z = 0.9
    density_brick = 10000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = (size_brick_y**2 + size_brick_z**2)*mass_brick/3
    inertia_brick_yy = (size_brick_x**2 + size_brick_z**2)*mass_brick/3
    inertia_brick_zz = (size_brick_x**2 + size_brick_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)
    
    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white_bricks.jpg'))
    texture.SetTextureScale(4, 4)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', [0, 1, 0], chrono.ChVectorD( 3*size_brick_x/8,  size_brick_y/2,  3*size_brick_z/8))
    COMPONENT.AddLinkPoint('B', [0, 1, 0], chrono.ChVectorD(-3*size_brick_x/8,  size_brick_y/2,  3*size_brick_z/8))
    COMPONENT.AddLinkPoint('C', [0, 1, 0], chrono.ChVectorD( 3*size_brick_x/8,  size_brick_y/2, -3*size_brick_z/8))
    COMPONENT.AddLinkPoint('D', [0, 1, 0], chrono.ChVectorD(-3*size_brick_x/8,  size_brick_y/2, -3*size_brick_z/8))
    COMPONENT.AddLinkPoint('E', [0, 1, 0], chrono.ChVectorD(                0,  size_brick_y/2,                0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT


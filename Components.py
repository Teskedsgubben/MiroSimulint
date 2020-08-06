import pychrono.core as chrono
import MiroComponent as mc
import os

# Margin to use in collision models to avoid friction statics
d = 0.006
chrono.SetChronoDataPath(os.getcwd() + "/")

# Plate with mounting sockets in corners on one side
def MC001(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.25
    size_brick_y = 0.03
    size_brick_z = 0.16
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_z,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2-d, size_brick_y/2-d, size_brick_z/2-d) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITstol.jpg'))
    texture.SetTextureScale(1, 1)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD( 3*size_brick_x/8,  size_brick_y/2,  3*size_brick_z/8))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(-3*size_brick_x/8,  size_brick_y/2,  3*size_brick_z/8))
    COMPONENT.AddLinkPoint('C', chrono.ChVectorD( 3*size_brick_x/8,  size_brick_y/2, -3*size_brick_z/8))
    COMPONENT.AddLinkPoint('D', chrono.ChVectorD(-3*size_brick_x/8,  size_brick_y/2, -3*size_brick_z/8))
    COMPONENT.AddLinkPoint('E', chrono.ChVectorD(                0, -size_brick_y/2,                0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT


# Mounting rod
def MC002(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.025
    size_brick_y = 0.15
    size_brick_z = 0.025
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_z,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2-d, size_brick_y/2-d, size_brick_z/2-d) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)
    
    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/brushsteel.jpg'))
    texture.SetTextureScale(4, 4)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(0,  size_brick_y/2, 0))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(0, -size_brick_y/2, 0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# Parachute
def MC044(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.2
    size_brick_y = 0.01
    size_brick_z = 0.2
    density_brick = 0.05   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_z,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2-d, size_brick_y/2-d, size_brick_z/2-d) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.AddAsset(body_brick_shape)
    
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(0, -100*size_brick_y, 0))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(0, -size_brick_y/2, 0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# Big fat thunk
def MC106(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.8
    size_brick_y = 1.2
    size_brick_z = 0.6
    density_brick = 5000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick_xx = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_z,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2-d, size_brick_y/2-d, size_brick_z/2-d) # must set half sizes
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

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(0, 0.9*size_brick_y/2,  size_brick_z/2))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(0, 0.9*size_brick_y/2, -size_brick_z/2))
    
    # Bottom mounting sockets
    COMPONENT.AddLinkPoint('C', chrono.ChVectorD(0, -size_brick_y/2,  size_brick_z/4))
    COMPONENT.AddLinkPoint('D', chrono.ChVectorD(0, -size_brick_y/2, -size_brick_z/4))
    
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
    inertia_brick_xx = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_z,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2-d, size_brick_y/2-d, size_brick_z/2-d) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_ikea_style.png'))
    texture.SetTextureScale(1, 10)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(0, size_brick_y/8,  size_brick_z/2))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(0, size_brick_y/8, -size_brick_z/2))

    COMPONENT.AddLinkPoint('C', chrono.ChVectorD(-size_brick_x/2, 0.9*size_brick_y/2, 0))
    COMPONENT.AddLinkPoint('D', chrono.ChVectorD(size_brick_x/2, 0.9*size_brick_y/2, 0))

    COMPONENT.AddLinkPoint('E', chrono.ChVectorD(-size_brick_x/2, -0.9*size_brick_y/2, 0))
    COMPONENT.AddLinkPoint('F', chrono.ChVectorD(size_brick_x/2, -0.9*size_brick_y/2, 0))
    
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
    inertia_brick_xx = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_z,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2-d, size_brick_y/2-d, size_brick_z/2-d) # must set half sizes
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

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD( 3*size_brick_x/8,  size_brick_y/2,  3*size_brick_z/8))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(-3*size_brick_x/8,  size_brick_y/2,  3*size_brick_z/8))
    COMPONENT.AddLinkPoint('C', chrono.ChVectorD( 3*size_brick_x/8,  size_brick_y/2, -3*size_brick_z/8))
    COMPONENT.AddLinkPoint('D', chrono.ChVectorD(-3*size_brick_x/8,  size_brick_y/2, -3*size_brick_z/8))
    COMPONENT.AddLinkPoint('E', chrono.ChVectorD(                0,  size_brick_y/2,                0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT

# Little rotation point
def MC013(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_r = 0.045
    size_brick_y = 0.04
    density_brick = 1   # kg/m^3
    mass_brick = density_brick * size_brick_r * size_brick_r * size_brick_y * 3.14
    inertia_brick_xx = 2/5*(pow(size_brick_r,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_yy = 2/5*(pow(size_brick_r,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    inertia_brick_zz = 2/5*(pow(size_brick_y,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBodyEasyCylinder(size_brick_r-d, size_brick_y-d, 0)
    body_brick.SetBodyFixed(Fixed)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddCylinder(size_brick_r-d, size_brick_y-d, 0) # hemi sizes
    body_brick.GetCollisionModel().BuildModel()

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITstol.jpg'))
    texture.SetTextureScale(1, 1)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(0,  size_brick_y/2,  0))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(0,  -size_brick_y/2,  0))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT
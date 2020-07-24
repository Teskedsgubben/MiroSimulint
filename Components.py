import pychrono.core as chrono
import MiroComponent as mc

# Margin to use in collision models to avoid friction statics
d = 0.008


def MC_0(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.25
    size_brick_y = 0.125
    size_brick_z = 0.25
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

    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(size_brick_x/4, 0.0, size_brick_z/2))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(size_brick_x/2, 0.0, size_brick_z/2))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT


# Mounting rod
def MC_002(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    size_brick_x = 0.04
    size_brick_y = 0.15
    size_brick_z = 0.04
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

    COMPONENT = mc.MiroComponent(body_brick)

    COMPONENT.AddLinkPoint('A', chrono.ChVectorD(size_brick_x/4, 0.0, size_brick_z/2))
    COMPONENT.AddLinkPoint('B', chrono.ChVectorD(size_brick_x/2, 0.0, size_brick_z/2))
    
    COMPONENT.Rotate(rot)
    COMPONENT.MoveToPosition(pos)

    return COMPONENT
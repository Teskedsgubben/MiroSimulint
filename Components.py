import pychrono.core as chrono



def MC001(): # kubb
    size_brick_x = 0.25
    size_brick_y = 0.12
    size_brick_z = 0.12
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.GetAssets().push_back(body_brick_shape)
            
    return body_brick

def MC002(): # rund pinne
    size_brick_x = 0.25
    size_brick_y = 0.12
    size_brick_z = 0.12
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_brick_x * size_brick_y * size_brick_z
    inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias

    body_brick = chrono.ChBody()
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))       

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x/2, size_brick_y/2, size_brick_z/2)
    
    body_brick_shape.SetColor(chrono.ChColor(0.65, 0.65, 0.6)) # set gray color 
    body_brick.GetAssets().push_back(body_brick_shape)
            
    return body_brick
import pychrono.core as chrono
import Components as comps

def DemoLander(system):
    # Create a contact material (surface property)to share between all objects.
    # The rolling and spinning parameters are optional - if enabled they double
    # the computational time.
    brick_material = chrono.ChMaterialSurfaceNSC()
    brick_material.SetFriction(0.5)
    brick_material.SetDampingF(0.2)
    brick_material.SetCompliance (0.0000001)
    brick_material.SetComplianceT(0.0000001)
    # brick_material.SetRollingFriction(rollfrict_param)
    # brick_material.SetSpinningFriction(0)
    # brick_material.SetComplianceRolling(0.0000001)
    # brick_material.SetComplianceSpinning(0.0000001)
    
    
    
    # Create the set of bricks in a vertical stack, along Y axis
    
    nbricks_on_x = 1
    nbricks_on_y = 6
    
    size_brick_x = 0.25
    size_brick_y = 0.12
    
    for ix in range(0,nbricks_on_x):
        for iy in range(0,nbricks_on_y):
            # create it
            body_brick = comps.MC001()
            # set initial position
            body_brick.SetPos(chrono.ChVectorD(ix*size_brick_x, (iy+30.5)*size_brick_y, 0 ))
    
            system.Add(body_brick)

def PendulumLander(system):

    pos = chrono.ChVectorD(1,2,-0.4)
    size_brick_x = 0.2
    size_brick_y = 0.5
    size_brick_z = 0.1
    
    # Create a fixed rigid body
    
    mbody1 = chrono.ChBody()
    mbody1.SetBodyFixed(False)
    mbody1.SetCollide(True)
    mbody1.SetPos( pos )
    
    # Collision shape
    mass_brick = 1000 * size_brick_x * size_brick_y * size_brick_z
    inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    mbody1.SetMass(mass_brick)
    mbody1.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))  
    mbody1.GetCollisionModel().ClearModel()
    mbody1.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    mbody1.GetCollisionModel().BuildModel()

    system.Add(mbody1)

    mboxasset = chrono.ChBoxShape()
    mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x, size_brick_y, size_brick_z)
    mbody1.AddAsset(mboxasset)

    
    # Create a swinging rigid body
    
    mbody2 = chrono.ChBody()
    mbody2.SetBodyFixed(False)
    mbody2.SetCollide(True)
    mbody2.SetPos( pos - chrono.ChVectorD(0,0,0.2))

    # Collision shape
    mass_brick = 1000 * size_brick_x * size_brick_y * size_brick_z
    inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    mbody2.SetMass(mass_brick)
    mbody2.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))  
    mbody2.GetCollisionModel().ClearModel()
    mbody2.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    mbody2.GetCollisionModel().BuildModel()

    system.Add(mbody2)
    
    mboxasset = chrono.ChBoxShape()
    mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(0.2,0.5,0.1)
    mbody2.AddAsset(mboxasset)
    
    mboxtexture = chrono.ChTexture()
    mboxtexture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
    mbody2.GetAssets().push_back(mboxtexture)
    
    
    # Create a revolute constraint
    
    mlink = chrono.ChLinkRevolute()
    
        # the coordinate system of the constraint reference in abs. space:
    mframe = chrono.ChFrameD(pos + chrono.ChVectorD(0.1,0.3,0))
    
        # initialize the constraint telling which part must be connected, and where:
    mlink.Initialize(mbody1,mbody2, mframe)
    
    system.Add(mlink)
    
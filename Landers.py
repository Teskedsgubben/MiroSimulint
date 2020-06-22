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
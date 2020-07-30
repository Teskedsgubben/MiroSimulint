import pychrono.core as chrono
import os
import Shapes as shp 

import Environments_Johan
import Environments_Marcus
import Environments_Franz

def MIT_place(system):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")

    # Throwing paramters for lander in the environment
    start_position = [10.5,7,0]
    throw_velocity = [-6.5,3,0]

    Environments_Johan.Johan_Components(system)
    Environments_Marcus.Marcus_Components(system)
    Environments_Franz.Franz_Components(system)


    MIT_floor_x = 10
    MIT_floor_z = 10


    body_floor = chrono.ChBody()
    body_floor.SetBodyFixed(True)
    body_floor.SetPos(chrono.ChVectorD(2.5, -1, -1))
    
    # Collision shape
    body_floor.GetCollisionModel().ClearModel()
    body_floor.GetCollisionModel().AddBox(MIT_floor_x, 1, MIT_floor_z) # hemi sizes
    body_floor.GetCollisionModel().BuildModel()
    body_floor.SetCollide(True)
    
    # Visualization shape
    body_floor_shape = chrono.ChBoxShape()
    body_floor_shape.GetBoxGeometry().Size = chrono.ChVectorD(MIT_floor_x, 1, MIT_floor_z)
    body_floor.GetAssets().push_back(body_floor_shape)
    
    body_floor_texture = chrono.ChTexture()
    body_floor_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
    body_floor_texture.SetTextureScale(3.5, 3.5)
    body_floor.GetAssets().push_back(body_floor_texture)
    
    system.Add(body_floor)

    # Create the shaking table, as a box
    
    size_table_x = 1
    size_table_y = 0.2
    size_table_z = 1
    
    body_table = chrono.ChBody()
    body_table.SetPos(chrono.ChVectorD(0, -size_table_y/2, 0 ))
    
    # Collision shape
    body_table.GetCollisionModel().ClearModel()
    body_table.GetCollisionModel().AddBox(size_table_x/2, size_table_y/2, size_table_z/2) # hemi sizes
    body_table.GetCollisionModel().BuildModel()
    body_table.SetCollide(True)
    
    # Visualization shape
    body_table_shape = chrono.ChBoxShape()
    body_table_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_table_x/2, size_table_y/2, size_table_z/2)
    body_table_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_table.GetAssets().push_back(body_table_shape)
    
    body_table_texture = chrono.ChTexture()
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/bhgang.jpg'))
    body_table.GetAssets().push_back(body_table_texture)
    
    system.Add(body_table)
    
    
    # Create a constraint that blocks free 3 x y z translations and 3 rx ry rz rotations
    # of the table respect to the floor, and impose that the relative imposed position
    # depends on a specified motion law.
    
    link_shaker = chrono.ChLinkLockLock()
    link_shaker.Initialize(body_table, body_floor, chrono.CSYSNORM)
    system.Add(link_shaker)
    
    # ..create the function for imposed x horizontal motion, etc.
    mfunY = chrono.ChFunction_Sine(0,1.5,0.001)  # phase, frequency, amplitude
    link_shaker.SetMotion_Y(mfunY)
    
    # ..create the function for imposed y vertical motion, etc.
    mfunZ = chrono.ChFunction_Sine(0,1.5,0.12)  # phase, frequency, amplitude
    link_shaker.SetMotion_Z(mfunZ)


    roof(system)
    


    step_comp = chrono.ChBody()
    step_comp.SetBodyFixed(True)
    step_comp.SetPos(chrono.ChVectorD(2,1.1,-3))
    # Collision shape
    step_comp.GetCollisionModel().ClearModel()
    step_comp.GetCollisionModel().AddBox(1, 0.1, 1) # hemi sizes
    step_comp.GetCollisionModel().BuildModel()
    step_comp.SetCollide(True)
    # Visualization shape
    step_comp_shape = chrono.ChBoxShape()
    step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD(1, 0.1, 1)
    step_comp_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    step_comp.GetAssets().push_back(step_comp_shape)
    step_comp_texture = chrono.ChTexture()
    step_comp_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/test_texture.png'))
    step_comp_texture.SetTextureScale(0.05, 0.05)
    step_comp.GetAssets().push_back(step_comp_texture)


    system.Add(step_comp)

    # Note that you could use other types of ChFunction_ objects, or create
    # your custom function by class inheritance (see demo_python.py), or also
    # set a function for table rotation , etc.
    
    
    return [start_position, throw_velocity]
    
def roof(system):

    beams = 4
    for b in range(beams):
        p1 = chrono.ChVectorD(-5 + 4.2*b - 0.06, 12-0.2, 6-0.06)
        p2 = chrono.ChVectorD(-5 + 4.2*b + 0.06, 12-0.2, 6-0.06)
        d1 = chrono.ChVectorD(0,-0.08,-1)
        d2 = chrono.ChVectorD(0,-0.08,-1)
        system.Add(shp.step(p1,d1, p2,d2, 18, 0.2))
    
    beams = 10
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD(-5 + 1.4*b, 11, 6))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD(0.06, 1, 0.06)
        step_comp_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
        step_comp.GetAssets().push_back(step_comp_shape)
        system.Add(step_comp)

    beams = 4
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD(-5 +6.3, 10-0.06+(2/3)*b, 6))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD(6.3+0.06, 0.06, 0.06)
        step_comp_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
        step_comp.GetAssets().push_back(step_comp_shape)
        system.Add(step_comp)
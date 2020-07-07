import pychrono.core as chrono
import os
import numpy as np

def Johan_Components(system):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    center = chrono.ChVectorD(8, -2, 5)  # Center position for the stair
    MIT_stairs(system, center)  
    MIT_floors(system)

def MIT_stairs(system, center):
        
    size_stairs_r =  0.3        # Radius
    size_stairs_h = 10          # Hight
    size_stairs_d = 1           # Density
    dh = 0.5                    # Hight between steps
    stepNum = 16                # Number of steps
    
    # Create middle cylinder for stairs
    body_stairs = chrono.ChBodyEasyCylinder(size_stairs_r, size_stairs_h, size_stairs_d)
    body_stairs.SetBodyFixed(True)
    body_stairs.SetPos(chrono.ChVectorD(8, 2, 5))

    # Collision shape
    body_stairs.GetCollisionModel().ClearModel()
    body_stairs.GetCollisionModel().AddCylinder(size_stairs_r, size_stairs_h, size_stairs_d) # hemi sizes
    body_stairs.GetCollisionModel().BuildModel()
    body_stairs.SetCollide(True)

    # Body texture
    body_stairs_texture = chrono.ChTexture()
    body_stairs_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white_bricks.jpg'))
    body_stairs.GetAssets().push_back(body_stairs_texture)

    system.Add(body_stairs)

    for step in range(3,2*stepNum):
        h = step*dh                     
        theta = 2*step*np.pi/stepNum    # Angle between each step

        MIT_stairsStep(system, center, size_stairs_r, h, theta)

        if step % 2 == 0:
            MIT_stairsHandle(system, center, size_stairs_r, h, theta-0.4)

def MIT_stairsStep(system, center, size_stairs_r, h, theta):

    # Create steps, as a box
    size_step_x = 1
    size_step_y = 0.1
    size_step_z = 1
        
    body_step = chrono.ChBody()
    body_step.SetBodyFixed(True)
    position = 2*size_stairs_r                              # Center position for the step box
    n = chrono.ChVectorD(np.cos(theta), h, np.sin(theta))   # Normal vector
    start = center + n*position       # Start postiton for each step                              
    body_step.SetPos(start)
        
    # Collision shape
    body_step.GetCollisionModel().ClearModel()
    body_step.GetCollisionModel().AddBox(size_step_x/2, size_step_y/2, size_step_z/2) # hemi sizes
    body_step.GetCollisionModel().BuildModel()
    body_step.SetCollide(True)
        
    # Visualization shape
    body_step_shape = chrono.ChBoxShape()
    body_step_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_step_x/2, size_step_y/2, size_step_z/2)
    body_step_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_step.GetAssets().push_back(body_step_shape)
        
    body_step_texture = chrono.ChTexture()
    body_step_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white_bricks.jpg'))
    body_step.GetAssets().push_back(body_step_texture)
        
    system.Add(body_step)

def MIT_stairsHandle(system, center, size_stairs_r, h, theta):

    size_handle_r = 0.08
    size_handle_h = 0.8
    size_handle_d = 1

    # Creat a handle for stairs as a cylinder
    body_handle = chrono.ChBodyEasyCylinder(size_handle_r, size_handle_h, size_handle_d)
    body_handle.SetBodyFixed(True)
    center_corr = chrono.ChVectorD(0,size_handle_h/2,0)     # Correction for handle position
    position = 3.2*size_stairs_r
    n = chrono.ChVectorD(np.cos(theta), 2*h*size_stairs_r/position, np.sin(theta))   # Normal vector
    start = center + n*position + center_corr      # Start postiton for each step                              
    body_handle.SetPos(start)

    # Collision shape
    body_handle.GetCollisionModel().ClearModel()
    body_handle.GetCollisionModel().AddCylinder(size_handle_r, size_handle_h, size_handle_d) # hemi sizes
    body_handle.GetCollisionModel().BuildModel()
    # body_handle.SetCollide(True)

    # Body texture
    body_handle_texture = chrono.ChTexture()
    body_handle_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
    body_handle.GetAssets().push_back(body_handle_texture)

    system.Add(body_handle)

def MIT_floors(system):

    # Add floor, as a box

    floorsNum = 2
    size_floor_x = 20
    size_floor_y = 0.2
    size_floor_z = 4
    
    for floor in range(floorsNum):
        y_pos = floor*3 + 3         # Increase floor hight
        floor_pos_1 = chrono.ChVectorD(0.5, y_pos, 8)     
        floor_pos_2 = chrono.ChVectorD(11, y_pos, 0)

        MIT_add_floors(system, size_floor_x, size_floor_y, size_floor_z, floor_pos_1)
        MIT_add_floors(system, size_floor_z, size_floor_y, size_floor_x, floor_pos_2)

def MIT_add_floors(system, size_x, size_y, size_z, floor_pos):

    body_floor = chrono.ChBody()
    body_floor.SetBodyFixed(True)
    body_floor.SetPos(chrono.ChVectorD(floor_pos))
    
    # Collision shape
    body_floor.GetCollisionModel().ClearModel()
    body_floor.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # hemi sizes
    body_floor.GetCollisionModel().BuildModel()
    body_floor.SetCollide(True)
    
    # Visualization shape
    body_floor_shape = chrono.ChBoxShape()
    body_floor_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    body_floor_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_floor.GetAssets().push_back(body_floor_shape)
    
    body_floor_texture = chrono.ChTexture()
    body_floor_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/stone_floor.jpg'))
    body_floor.GetAssets().push_back(body_floor_texture)
    
    system.Add(body_floor)

# def

    # Create the table, as a box
    
    size_table_x = 1
    size_table_y = 0.2
    size_table_z = 0.3
    
    body_table = chrono.ChBody()
    body_table.SetBodyFixed(True)
    body_table.SetPos(chrono.ChVectorD(0, 0, 0 ))
    
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
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/tf-logo.jpg'))
    body_table.GetAssets().push_back(body_table_texture)
    
    system.Add(body_table)
    
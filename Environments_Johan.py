import pychrono.core as chrono
import os
import numpy as np
import Shapes as shp

def Johan_Components(system):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    center = chrono.ChVectorD(7, -2, 4)  # Center position for the stair
    MIT_stairs(system, center)  
    MIT_floors(system)

def MIT_stairs(system, center):
        
    stair_r =  0.3       # Radius
    stair_h = 9          # Hight
    stair_d = 1          # Density
    dh = 0.35             # Hight between steps
    stepNum = 14          # Number of steps
    pos_stair = center + chrono.ChVectorD(0, 5.5, 0)  # Correction for stair position

    # Create middle cylinder for stairs
    body_stairs = chrono.ChBodyEasyCylinder(stair_r, stair_h, stair_d)
    body_stairs.SetBodyFixed(True)
    body_stairs.SetPos(pos_stair)

    # Collision shape
    body_stairs.GetCollisionModel().ClearModel()
    body_stairs.GetCollisionModel().AddCylinder(stair_r, stair_h, stair_d) # hemi sizes
    body_stairs.GetCollisionModel().BuildModel()
    body_stairs.SetCollide(True)

    # Body texture
    body_stairs_texture = chrono.ChTexture()
    body_stairs_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white_bricks.jpg'))
    body_stairs.GetAssets().push_back(body_stairs_texture)

    system.Add(body_stairs)

    # Add steps to 3rd floor
    H = 4 
    dh = H/stepNum

    start_dir = [1, 0, 0]
    T_theta = 270/360*2*np.pi

    for step in range(3,stepNum):
        h = step*dh                     
        theta = 2*step*np.pi/stepNum    # Angle between each step

        MIT_stairsStep(system, center, stair_r, h, theta, theta)

        # if step % 2 == 0:           
        #     MIT_stairsHandle(system, center, stair_r, h, theta-0.4)

    # Add steps to 4th floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = 1/360*2*np.pi*(90 + 270*step/stepNum)    # Angle between each step
        theta_b = 1/360*2*np.pi*(90 + 270*(step+1)/stepNum)
        pos = center + chrono.ChVectorD(0, stair_h/2, 0)
        MIT_stairsStep(system, pos, stair_r, h, theta_f, theta_b)

        # if step % 2 == 0:           
        #     MIT_stairsHandle(system, center, stair_r, h, theta-0.4)

def MIT_stairsStep(system, center, stair_r, h, theta_f, theta_b):

    width = 1.75
    height = 0.2
    # theta_f = theta
    # theta_b = theta + 270/14*(2*np.pi/360)
    
    df = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + df*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton front of step

    db = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + db*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton back of step                              
    
    step = shp.step(pos_f, df, pos_b, db, width, height)        # Create each step
        
    system.Add(step)

def MIT_stairsHandle(system, center, stair_r, h, theta):

    size_handle_r = 0.04
    size_handle_h = 0.8
    size_handle_d = 1

    # Creat a handle for stairs as a cylinder
    body_handle = chrono.ChBodyEasyCylinder(size_handle_r, size_handle_h, size_handle_d)
    body_handle.SetBodyFixed(True)
    center_corr = chrono.ChVectorD(0, size_handle_h/2, 0)     # Correction for handle position
    position = 3.2*stair_r
    n = chrono.ChVectorD(np.cos(theta), 2*h*stair_r/position, np.sin(theta))   # Normal vector
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

    floorsNum = 2               # Number of floors
    postNum = 5                 # How many fence post there is to each side of floors center position
    size_floor_x = 20
    size_floor_y = 0.2
    size_floor_z = 4 

    for floor in range(floorsNum):
        y_pos = floor*3 + 3         # Increase floor hight
        floor_pos_1 = chrono.ChVectorD(0.5, y_pos, 8)     
        floor_pos_2 = chrono.ChVectorD(11, y_pos, 0)

        MIT_add_floors(system, size_floor_x, size_floor_y, size_floor_z, floor_pos_1)
        MIT_add_floors(system, size_floor_z, size_floor_y, size_floor_x, floor_pos_2)

        for post in range(postNum):
            # Add fence post to the rigth of the floors center position
            fence_pos_1 = chrono.ChVectorD(0.5+post, y_pos, 8-size_floor_z/2) 
            fence_pos_2 = chrono.ChVectorD(11-size_floor_z/2, y_pos, 0+post)

            MIT_fence_post(system, fence_pos_1)
            MIT_fence_post(system, fence_pos_2)

            if post > 0:
                # Add fence post to the left of the floors center position
                fence_pos_3 = chrono.ChVectorD(0.5-post, y_pos, 8-size_floor_z/2)
                fence_pos_4 = chrono.ChVectorD(11-size_floor_z/2, y_pos, 0-post)

                MIT_fence_post(system, fence_pos_3)
                MIT_fence_post(system, fence_pos_4)

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

def MIT_fence_post(system, fence_pos):

    size_fence_r =  0.05        # Radius
    size_fence_h = 0.8         # Hight
    size_fence_d = 1           # Density
    fence_corr = chrono.ChVectorD(0, size_fence_h/2, 0) # Correction for fence post postition

    # Create fence post as a cylinder
    body_fence = chrono.ChBodyEasyCylinder(size_fence_r, size_fence_h, size_fence_d)
    body_fence.SetBodyFixed(True)
    body_fence.SetPos(chrono.ChVectorD(fence_pos+fence_corr))

    # Collision shape
    body_fence.GetCollisionModel().ClearModel()
    body_fence.GetCollisionModel().AddCylinder(size_fence_r/2, size_fence_h/2, size_fence_d/2) # hemi sizes
    body_fence.GetCollisionModel().BuildModel()
    body_fence.SetCollide(True)

    # Body texture
    body_fence_texture = chrono.ChTexture()
    body_fence_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
    body_fence.GetAssets().push_back(body_fence_texture)

    system.Add(body_fence)

# def

    # # Create the table, as a box
    
    # size_table_x = 1
    # size_table_y = 0.2
    # size_table_z = 0.3
    
    # body_table = chrono.ChBody()
    # body_table.SetBodyFixed(True)
    # body_table.SetPos(chrono.ChVectorD(0, 0, 0 ))
    
    # # Collision shape
    # body_table.GetCollisionModel().ClearModel()
    # body_table.GetCollisionModel().AddBox(size_table_x/2, size_table_y/2, size_table_z/2) # hemi sizes
    # body_table.GetCollisionModel().BuildModel()
    # body_table.SetCollide(True)
    
    # # Visualization shape
    # body_table_shape = chrono.ChBoxShape()
    # body_table_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_table_x/2, size_table_y/2, size_table_z/2)
    # body_table_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    # body_table.GetAssets().push_back(body_table_shape)
    
    # body_table_texture = chrono.ChTexture()
    # body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/tf-logo.jpg'))
    # body_table.GetAssets().push_back(body_table_texture)
    
    # system.Add(body_table)

import pychrono.core as chrono
import os
import numpy as np
import Shapes as shp

def Johan_Components(system, SPEEDMODE = False):
    # Create the room: simple fixed rigid bodys with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    Height = 4              # Height between each floor
    center = chrono.ChVectorD(6.5, 0, 3)  # Center position for the stair
    MIT_stair(system, center, Height)  # Adds a spiral stair
    MIT_floors(system, Height)  # Add floors
    MIT_walls(system, Height)   # Add walls

def MIT_stair(system, center, H):
        
    stair_r =  0.3       # Radius
    stair_h = 9          # Hight
    stair_d = 1          # Density
    stepNum = 15         # Number of steps
    dh = H/stepNum       # Heigth between each step
    rad = 1/360*2*np.pi  # Degrees to radians
    texture = 'textures/white concrete.jpg' 
    pos_stair = center + chrono.ChVectorD(0, stair_h/2, 0)  # Correction for stair position

    # Add center cylinder of stair
    add_cylinderShape(system, stair_r, stair_h, stair_d, pos_stair, texture) 

    # Add steps to 3rd floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)    # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum) # Angle between each back step

        add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh, step, stepNum)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, center, stair_r, h, theta_f, theta_b)

    # Add steps to 4th floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)       # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum)   # Angle between each back step
        pos_topStair = center + chrono.ChVectorD(0, H, 0)

        add_stairStep(system, pos_topStair, stair_r, h, theta_f, theta_b, dh, step, stepNum)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, pos_topStair, stair_r, h, theta_f, theta_b)

def add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh, i, stepNum):

    # Add stair step
    width = 1.75    # Step width
    height = 0.2    # Step height
    
    dir_f = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + dir_f*stair_r + chrono.ChVectorD(0, h-0.05, 0)     # Start postiton front of step

    dir_b = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + dir_b*stair_r + chrono.ChVectorD(0, h-0.05, 0)     # Start postiton back of step                              
    
    step = shp.step(pos_f, dir_f, pos_b, dir_b, width, height)        # Create each step
        
    system.Add(step)

    # top part
    pos_f = center + dir_f*stair_r + chrono.ChVectorD(0, h+0.05, 0)     # Start postiton front of step
    pos_b = center + dir_b*stair_r + chrono.ChVectorD(0, h+0.05, 0)     # Start postiton back of step                              
    step_top = shp.step(pos_f, dir_f, pos_b, dir_b, width, height)        # Create each step  
    system.Add(step_top)

    # Add apiral rail for stair
    handle_r = 0.05     # Radius
    handle_l = 0.705    # Length
    handle_d = 1        # Density
    texture_handle = 'textures/wood_floor.jpg'
    rail_r = 0.025      # Radius
    rail_l = 0.705      # Length
    rail_d = 1          # Density
    texture_rail = 'textures/white concrete.jpg'

    dir_f.SetLength(width)
    dir_b.SetLength(width)
    n = (dir_f+dir_b)/2   
        
    pos_handle = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, 1.3, 0)  # Handle rail
    pos_rail_1 = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, 1, 0)    # Upper support rail
    pos_rail_2 = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, 0.3, 0)  # Lower support rail

    dist = np.sqrt((dir_f.x-dir_b.x)**2 + (dir_f.y-dir_b.y)**2 + (dir_f.z-dir_b.z)**2)    # Calculate distance between dir_f and dir_b
    alpha = np.arctan((dist+0.1)/dh)
    
    add_spiralRail(system, handle_r, handle_l, handle_d, pos_handle, alpha, n, texture_handle)

    if 0 < i and i < stepNum-1:
        add_spiralRail(system, rail_r, rail_l, rail_d, pos_rail_1, alpha, n, texture_rail)
        add_spiralRail(system, rail_r, rail_l, rail_d, pos_rail_2, alpha, n, texture_rail)
    
def add_spiralRail(system, radius, length, density, pos, alpha, n, texture):
    
    # Add spiral cylinder 
    body_rail = chrono.ChBodyEasyCylinder(radius, length, density) # Rail size
    body_rail.SetBodyFixed(True)
    body_rail.SetPos(pos)
    
    qr = chrono.Q_from_AngAxis(alpha, n.GetNormalized())    # Rotate the cylinder
    quaternion = qr * body_rail.GetRot()
    body_rail.SetRot(quaternion)

    # Collision shape
    body_rail.GetCollisionModel().ClearModel()
    body_rail.GetCollisionModel().AddCylinder(0.95*radius, 0.95*length, density) # hemi sizes
    body_rail.GetCollisionModel().BuildModel()
    body_rail.SetCollide(True)

    # Body texture
    body_rail_texture = chrono.ChTexture()
    body_rail_texture.SetTextureFilename(chrono.GetChronoDataFile(texture))
    body_rail.GetAssets().push_back(body_rail_texture)

    system.Add(body_rail)

def add_stairPosts(system, center, stair_r, h, theta_f, theta_b):

    width = 1.75

    dir_f = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front of step
    pos_f = center + dir_f*stair_r + chrono.ChVectorD(0, h, 0)     # Postiton front of step

    dir_b = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back of step
    pos_b = center + dir_b*stair_r + chrono.ChVectorD(0, h, 0)     # Postiton back of step

    # Add rail pole for stair
    post_r = 0.02   # Radius
    post_h = 1.3    # Height
    post_d = 1      # Density
    texture = 'textures/white concrete.jpg'
    dir_f.SetLength(width)
    dir_b.SetLength(width)
    pos_pole = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, post_h/2, 0)   # Position

    add_cylinderShape(system, post_r, post_h*0.95, post_d, pos_pole, texture)

def MIT_floors(system, H):

    # Add floor, as a box
    floorsNum = 2               # Number of floors
    postNum = 7                 # Number of fence post on each side of floors center position
    floor_l = 10                # Floor length
    floor_t = 0.1               # Floor thickness
    floor_w = 2                 # Floor width
    texture_floor = 'textures/stone_floor.jpg'
    scale_floor = 10 # Texture scale

    # Add fence post, as a cylinder
    fence_r =  0.02         # Radius
    fence_h = 1             # Hight
    fence_d = 1             # Density
    texture = 'textures/white concrete.jpg'
    fence_corr = chrono.ChVectorD(0, fence_h/2, 0) # Correction for fence post postition

    for floor in range(floorsNum):
        # Add floors
        y_pos = floor*H + H                                 
        floor_pos_1 = chrono.ChVectorD(2.5-2, y_pos, 7)       # Add floors left side stair
        floor_pos_2 = chrono.ChVectorD(10.5, y_pos, -1)       # Add floors right side stair

        add_boxShape(system, floor_l-2, floor_t, floor_w, floor_pos_1, texture_floor, scale_floor)
        add_boxShape(system, floor_w, floor_t, floor_l, floor_pos_2, texture_floor, scale_floor)

        for post in range(postNum):
            # Add fence post to the rigth of the floors center position
            fence_pos_1 = chrono.ChVectorD(0+post, H, 7-floor_w) + fence_corr
            fence_pos_2 = chrono.ChVectorD(10.5-floor_w, y_pos, -4+post) + fence_corr # Right side stair

            add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_1, texture)
            add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_2, texture)

            if post > 0:
                # Add fence post to the left of the floors center position
                fence_pos_3 = chrono.ChVectorD(0-post, H, 7-floor_w) + fence_corr
                fence_pos_4 = chrono.ChVectorD(10.5-floor_w, y_pos, -4-post) + fence_corr # Right side stair

                add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_3, texture)
                add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_4, texture)
    
    # Add handle for each floor
    handle_r = 0.05         # Radius
    handle_l = 13           # Length
    handle_d = 1            # Density
    n_x = chrono.ChVectorD(1, 0, 0)     # Normalvector for handle
    n_z = chrono.ChVectorD(0, 0, 1)     # Normalvector for handle
    pos_rail_1 = chrono.ChVectorD(0, H+fence_h, 7-floor_w)          # Fence third floor left of stair
    pos_rail_2 = chrono.ChVectorD(10.5-floor_w, H+fence_h, -4)      # Fence third floor
    pos_rail_3 = chrono.ChVectorD(10.5-floor_w, 2*H+fence_h, -4)    # Fence fourth floor

    pos = [pos_rail_1, pos_rail_2, pos_rail_3]
    dirr = [n_z, n_x, n_x]
    
    for num in range(len(pos)):
        pos_rail = pos[num]
        n = dirr[num]
        
        body_handle = chrono.ChBodyEasyCylinder(handle_r, handle_l, handle_d) # Rail size
        body_handle.SetBodyFixed(True)
        body_handle.SetPos(pos_rail)
        
        qr = chrono.Q_from_AngAxis(np.pi/2, n.GetNormalized())    # Rotate the cylinder
        quaternion = qr * body_handle.GetRot()
        body_handle.SetRot(quaternion)

        # Collision shape
        body_handle.GetCollisionModel().ClearModel()
        body_handle.GetCollisionModel().AddCylinder(handle_r, handle_l, handle_d) # hemi sizes
        body_handle.GetCollisionModel().BuildModel()
        body_handle.SetCollide(True)

        # Body texture
        body_handle_texture = chrono.ChTexture()
        body_handle_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
        body_handle.GetAssets().push_back(body_handle_texture)

        system.Add(body_handle)

    # Add floor piece by the stir
    floor_x = 1
    floor_y = 0.1
    floor_z = 1
    scale_piece = 5 # Texture scale

    for piece in range(2):
        y_pos = piece*H + H
        floor_pos = chrono.ChVectorD(7.5, y_pos, 4) 
        
        add_boxShape(system, floor_x, floor_y, floor_z, floor_pos, texture_floor, scale_piece)

def MIT_walls(system, H):

    # Add main walls as a box 
    wall_thickness = 0.1
    wall_height = 2*H
    wall_length = 10
    texture_wall = 'textures/BHgang.jpg'
    texture_wall1 = 'skybox/sky_lf.jpg'
    scale = 5   # Texture scale
    
    pos_wall_1 = chrono.ChVectorD(12.5, 0, -1) + chrono.ChVectorD(0, wall_height/2, 0)
    pos_wall_2 = chrono.ChVectorD(-7.5, 0, -1) + chrono.ChVectorD(0, wall_height/2, 0)
    pos_wall_3 = chrono.ChVectorD(2.5, 0, 9) + chrono.ChVectorD(0, wall_height/2, 0)
    pos_wall_4 = chrono.ChVectorD(2.5, 0, -11) + chrono.ChVectorD(0, wall_height/2, 0)

    wall = [pos_wall_1, pos_wall_2, pos_wall_3, pos_wall_4]

    add_boxShape(system, wall_thickness, wall_height, wall_length, wall[0], texture_wall, scale)
    add_boxShape(system, wall_thickness, wall_height, wall_length, wall[1], texture_wall1, scale)
    add_boxShape(system, wall_length, wall_height, wall_thickness, wall[2], texture_wall, scale)
    add_boxShape(system, wall_length, wall_height, wall_thickness, wall[3], texture_wall1, scale)
    
    # Add top floor wall
    topWall_height = 2
    topWall_length = 7
    topWall_pos = chrono.ChVectorD(-0.5, 2*H+topWall_height, 5.1)
    add_boxShape(system, topWall_length, topWall_height, wall_thickness, topWall_pos, texture_wall, scale)

    # Add bottom floor wall
    bWall_height = 2 - 0.025            # -0.025 Correction of floor thickness
    bWall_length = 6
    bWall_pos = chrono.ChVectorD(-1.5, 0+bWall_height-0.025, 5.1)
    add_boxShape(system, bWall_length, bWall_height, wall_thickness, bWall_pos, texture_wall, scale)

    # Add top floor door wall
    topDoor_height = 2
    topDoor_length = 2
    topDoor_pos = chrono.ChVectorD(6.5, 2*H+topWall_height, 7)
    texture_door = 'textures/glass_door.jpg'
    scale = 5
    add_boxShape(system, wall_thickness, topDoor_height, topDoor_length, topDoor_pos, texture_door, scale)

def add_boxShape(system, size_x, size_y, size_z, pos, texture, scale):

    # Create a box
    body_box = chrono.ChBody()
    body_box.SetBodyFixed(True)
    body_box.SetPos(chrono.ChVectorD(pos))
    
    # Collision shape
    body_box.GetCollisionModel().ClearModel()
    body_box.GetCollisionModel().AddBox(size_x, size_y, size_z) # hemi sizes
    body_box.GetCollisionModel().BuildModel()
    body_box.SetCollide(True)
    
    # Visualization shape
    body_box_shape = chrono.ChBoxShape()
    body_box_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x, size_y, size_z)
    body_box_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_box.GetAssets().push_back(body_box_shape)
    
    body_box_texture = chrono.ChTexture()
    body_box_texture.SetTextureFilename(chrono.GetChronoDataFile(texture))
    body_box_texture.SetTextureScale(scale, scale)
    body_box.GetAssets().push_back(body_box_texture)
    
    system.Add(body_box)

def add_cylinderShape(system, radius, height, density, pos, texture):

    # Create a cylinder
    body_cylinder = chrono.ChBodyEasyCylinder(radius, height, density)
    body_cylinder.SetBodyFixed(True)
    body_cylinder.SetPos(chrono.ChVectorD(pos))

    # Collision shape
    body_cylinder.GetCollisionModel().ClearModel()
    body_cylinder.GetCollisionModel().AddCylinder(radius, height, density) # hemi sizes
    body_cylinder.GetCollisionModel().BuildModel()
    body_cylinder.SetCollide(True)

    # Body texture
    body_cylinder_texture = chrono.ChTexture()
    body_cylinder_texture.SetTextureFilename(chrono.GetChronoDataFile(texture))
    body_cylinder.GetAssets().push_back(body_cylinder_texture)

    system.Add(body_cylinder)

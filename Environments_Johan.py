import pychrono.core as chrono
import os
import numpy as np
import Shapes as shp

def Johan_Components(system):
    # Create the room: simple fixed rigid bodys with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    Height = 4              # Height between each floor
    center = chrono.ChVectorD(7, 0, 4)  # Center position for the stair
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
    texture = 'textures/white concrete.jpg' # Add texture
    pos_stair = center + chrono.ChVectorD(0, stair_h/2, 0)  # Correction for stair position

    # Add center cylinder of stair
    add_cylinderShape(system, stair_r, stair_h, stair_d, pos_stair, texture) 

    # Add steps to 3rd floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)    # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum) # Angle between each back step

        add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, center, stair_r, h, theta_f, theta_b)

    # Add steps to 4th floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)       # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum)   # Angle between each back step
        pos_topStair = center + chrono.ChVectorD(0, H, 0)

        add_stairStep(system, pos_topStair, stair_r, h, theta_f, theta_b, dh)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, pos_topStair, stair_r, h, theta_f, theta_b)

def add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh):

    # Add stair step
    width = 1.75    # Step width
    height = 0.2    # Step height
    
    df = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + df*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton front of step

    db = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + db*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton back of step                              
    
    step = shp.step(pos_f, df, pos_b, db, width, height)        # Create each step
        
    system.Add(step)

    # Add rail handle for stair
    handle_r = 0.05     # Radius
    handle_l = 0.705    # Length
    handle_d = 1        # Density
    texture_handle = 'textures/wood_floor.jpg'
    rail_r = 0.025      # Radius
    rail_l = 0.705      # Length
    rail_d = 1          # Density
    texture_rail = 'textures/white concrete.jpg'

    df.SetLength(width)
    db.SetLength(width)
    n = (df+db)/2   
        
    pos_handle = (pos_f+pos_b)/2 + (df+db)/2 + chrono.ChVectorD(0, 1.3, 0)
    pos_rail_1 = (pos_f+pos_b)/2 + (df+db)/2 + chrono.ChVectorD(0, 1, 0)    # Upper support rail
    pos_rail_2 = (pos_f+pos_b)/2 + (df+db)/2 + chrono.ChVectorD(0, 0.3, 0)  # Lower support rail

    dist = np.sqrt((df.x-db.x)**2 + (df.y-db.y)**2 + (df.z-db.z)**2)    # Calculate distance between df and db
    alpha = np.arctan((dist+0.1)/dh)
    
    add_spiralRail(system, handle_r, handle_l, handle_d, pos_handle, alpha, n, texture_handle)
    add_spiralRail(system, rail_r, rail_l, rail_d, pos_rail_1, alpha, n, texture_rail)
    add_spiralRail(system, rail_r, rail_l, rail_d, pos_rail_2, alpha, n, texture_rail)
    
def add_spiralRail(system, radius, length, density, pos, alpha, n, texture):
    
    # Add spiral cylinder 
    body_handle = chrono.ChBodyEasyCylinder(radius, length, density) # Rail size
    body_handle.SetBodyFixed(True)
    body_handle.SetPos(pos)
    
    qr = chrono.Q_from_AngAxis(alpha, n.GetNormalized())    # Rotate the cylinder
    quaternion = qr * body_handle.GetRot()
    body_handle.SetRot(quaternion)

    # Collision shape
    body_handle.GetCollisionModel().ClearModel()
    body_handle.GetCollisionModel().AddCylinder(0.95*radius, 0.95*length, density) # hemi sizes
    body_handle.GetCollisionModel().BuildModel()
    body_handle.SetCollide(True)

    # Body texture
    body_handle_texture = chrono.ChTexture()
    body_handle_texture.SetTextureFilename(chrono.GetChronoDataFile(texture))
    body_handle.GetAssets().push_back(body_handle_texture)

    system.Add(body_handle)

def add_stairPosts(system, center, stair_r, h, theta_f, theta_b):

    width = 1.75
    height = 0.2

    df = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + df*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton front of step

    db = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + db*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton back of step

    step = shp.step(pos_f, df, pos_b, db, width, height)        # Create each step

    system.Add(step)

    # Add rail pole for stair
    r_pole = 0.02   # Radius
    h_pole = 1.3    # Height
    d_pole = 1      # Density
    texture = 'textures/white concrete.jpg'
    df.SetLength(width)
    db.SetLength(width)
    pos_pole = (pos_f+pos_b)/2 + (df+db)/2 + chrono.ChVectorD(0, h_pole/2, 0)   # Position

    add_cylinderShape(system, r_pole, h_pole*0.95, d_pole, pos_pole, texture)

def MIT_floors(system, H):

    # Add floor, as a box
    floorsNum = 2               # Number of floors
    postNum = 7                 # How many fence post there is to each side of floors center position
    floor_l = 10                # Floor length
    floor_t = 0.1               # Floor thickness
    floor_w = 2                 # Floor width
    texture_floor = 'textures/stone_floor.jpg'

    # Add fence post, as a cylinder
    fence_r =  0.02        # Radius
    fence_h = 0.8         # Hight
    fence_d = 1           # Density
    texture = 'textures/white concrete.jpg'
    fence_corr = chrono.ChVectorD(0, fence_h/2, 0) # Correction for fence post postition

    for floor in range(floorsNum):
        # Add floors
        y_pos = floor*H + H     # Increase floor hight
        floor_pos_1 = chrono.ChVectorD(3, y_pos, 8)     # Add floors left side stair
        floor_pos_2 = chrono.ChVectorD(11, y_pos, -1)      # Add floors right side stair

        add_boxShape(system, floor_l, floor_t, floor_w, floor_pos_1, texture_floor)
        add_boxShape(system, floor_w, floor_t, floor_l, floor_pos_2, texture_floor)

        for post in range(postNum):
            # Add fence post to the rigth of the floors center position
            fence_pos_1 = chrono.ChVectorD(0.5+post, H, 8-floor_w) + fence_corr
            fence_pos_2 = chrono.ChVectorD(11-floor_w, y_pos, -2+post) + fence_corr# Right side stair

            add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_1, texture)
            add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_2, texture)

            if post > 0:
                # Add fence post to the left of the floors center position
                fence_pos_3 = chrono.ChVectorD(0.5-post, H, 8-floor_w) + fence_corr
                fence_pos_4 = chrono.ChVectorD(11-floor_w, y_pos, -2-post) + fence_corr# Right side stair

                add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_3, texture)
                add_cylinderShape(system, fence_r, fence_h, fence_d ,fence_pos_4, texture)
    
    # Add handle for each floor
    handle_r = 0.05     # Radius
    handle_l = 12.5       # Length
    handle_d = 1        # Density
    n_x = chrono.ChVectorD(1, 0, 0)     # Normalvector for handle
    n_z = chrono.ChVectorD(0, 0, 1)     # Normalvector for handle
    pos_rail_1 = chrono.ChVectorD(0.5, H+fence_h, 8-floor_w)      # Fence third floor
    pos_rail_2 = chrono.ChVectorD(11-floor_w, H+fence_h, -2)      # Fence third floor
    pos_rail_3 = chrono.ChVectorD(11-floor_w, 2*H+fence_h, -2)    # Fence fourth floor

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

    for piece in range(2):
        y_pos = piece*H + H
        floor_pos = chrono.ChVectorD(8, y_pos, 5) 
        
        add_boxShape(system, floor_x, floor_y, floor_z, floor_pos, texture_floor)

def MIT_walls(system, H):

    # Add main walls as a box 
    wall_thickness = 0.25
    wall_height = 2*H
    wall_length = 10
    # texture_mainWall = 'textures/BHgang.jpg'
    texture_wall = 'textures/BHgang.jpg'
    
    pos_wall_1 = chrono.ChVectorD(12.5, 0, -1) + chrono.ChVectorD(0, wall_height/2, 0)
    pos_wall_2 = chrono.ChVectorD(-7.5, 0, -1) + chrono.ChVectorD(0, wall_height/2, 0)
    pos_wall_3 = chrono.ChVectorD(2.5, 0, 9) + chrono.ChVectorD(0, wall_height/2, 0)
    pos_wall_4 = chrono.ChVectorD(2.5, 0, -11) + chrono.ChVectorD(0, wall_height/2, 0)

    wall = [pos_wall_1, pos_wall_2, pos_wall_3, pos_wall_4]

    add_boxShape(system, wall_thickness, wall_height, wall_length, wall[0], texture_wall)
    add_boxShape(system, wall_thickness, wall_height, wall_length, wall[1], texture_wall)
    add_boxShape(system, wall_length, wall_height, wall_thickness, wall[2], texture_wall)
    add_boxShape(system, wall_length, wall_height, wall_thickness, wall[3], texture_wall)
    
    # Add top floor wall
    topWall_height = 2
    topWall_length = 7
    topWall_pos = chrono.ChVectorD(0, 2*H+topWall_height, 6)
    add_boxShape(system, topWall_length, topWall_height, wall_thickness, topWall_pos, texture_wall)

    # Add bottom floor wall
    bWall_height = 2
    bWall_length = 6
    bWall_pos = chrono.ChVectorD(-1, 0+topWall_height, 6.25)
    add_boxShape(system, bWall_length, bWall_height, wall_thickness, bWall_pos, texture_wall)

def add_boxShape(system, size_x, size_y, size_z, box_pos, texture):

    # Create a box
    body_box = chrono.ChBody()
    body_box.SetBodyFixed(True)
    body_box.SetPos(chrono.ChVectorD(box_pos))
    
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
    body_box_texture.SetTextureScale(10, 10)
    body_box.GetAssets().push_back(body_box_texture)
    
    system.Add(body_box)

def add_cylinderShape(system, radius, height, density, pos, texture):

    # Create a cylinder
    body_fence = chrono.ChBodyEasyCylinder(radius, height, density)
    body_fence.SetBodyFixed(True)
    body_fence.SetPos(chrono.ChVectorD(pos))

    # Collision shape
    body_fence.GetCollisionModel().ClearModel()
    body_fence.GetCollisionModel().AddCylinder(radius/2, height/2, density/2) # hemi sizes
    body_fence.GetCollisionModel().BuildModel()
    body_fence.SetCollide(True)

    # Body texture
    body_fence_texture = chrono.ChTexture()
    body_fence_texture.SetTextureFilename(chrono.GetChronoDataFile(texture))
    body_fence.GetAssets().push_back(body_fence_texture)

    system.Add(body_fence)

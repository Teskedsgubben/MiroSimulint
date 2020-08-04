import pychrono.core as chrono
import os
import numpy as np
import Shapes as shp

def Johan_Components(system):
    # Create the room: simple fixed rigid bodys with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    center = chrono.ChVectorD(7, 0, 4)  # Center position for the stair
    Height = 4              # Height between each floor
    MIT_stairs(system, center, Height)  
    MIT_floors(system, Height)

def MIT_stairs(system, center, H):
        
    stair_r =  0.3       # Radius
    stair_h = 9          # Hight
    stair_d = 1          # Density
    stepNum = 15         # Number of steps
    dh = H/stepNum       # Heigth between each step
    rad = 1/360*2*np.pi  # Degrees to radians
    texture = 'textures/white concrete.jpg' # Add texture
    pos_stair = center + chrono.ChVectorD(0, stair_h/2, 0)  # Correction for stair position

    # Add center cylinder of stair
    MIT_add_cylinder(system, stair_r, stair_h, stair_d, pos_stair, texture) 

    # Add steps to 3rd floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)    # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum) # Angle between each back step

        MIT_stairsStep(system, center, stair_r, h, theta_f, theta_b, dh)

        # Add fence post for stair
        if step % 2 == 0:           
            MIT_stairsHandle(system, center, stair_r, h, theta_f, theta_b)

    # Add steps to 4th floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)       # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum)   # Angle between each back step
        pos_topStair = center + chrono.ChVectorD(0, H, 0)

        MIT_stairsStep(system, pos_topStair, stair_r, h, theta_f, theta_b, dh)

        # Add fence post for stair
        if step % 2 == 0:           
            MIT_stairsHandle(system, pos_topStair, stair_r, h, theta_f, theta_b)

def MIT_stairsStep(system, center, stair_r, h, theta_f, theta_b, dh):

    width = 1.75
    height = 0.2
    
    df = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + df*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton front of step

    db = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + db*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton back of step                              
    
    step = shp.step(pos_f, df, pos_b, db, width, height)        # Create each step
        
    system.Add(step)

    # Add rail handle for stair
    df.SetLength(width)
    db.SetLength(width)
    n = (df+db)/2
    
    pos_rail = (pos_f+pos_b)/2 + (df+db)/2 + chrono.ChVectorD(0, 1.3, 0)
    body_handle = chrono.ChBodyEasyCylinder(0.05, 0.705, 1) # Rail size
    body_handle.SetBodyFixed(True)
    body_handle.SetPos(pos_rail)

    dist = np.sqrt((df.x-db.x)**2 + (df.y-db.y)**2 + (df.z-db.z)**2)    # Calculate distance between df and db
    alpha = np.arctan((dist+0.1)/dh)
    
    qr = chrono.Q_from_AngAxis(alpha, n.GetNormalized())    # Rotate the cylinder
    quaternion = qr * body_handle.GetRot()
    body_handle.SetRot(quaternion)

    # Collision shape
    body_handle.GetCollisionModel().ClearModel()
    body_handle.GetCollisionModel().AddCylinder(0.05, 0.1, 1) # hemi sizes
    body_handle.GetCollisionModel().BuildModel()
    # body_handle.SetCollide(True)

    # Body texture
    body_handle_texture = chrono.ChTexture()
    body_handle_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
    body_handle.GetAssets().push_back(body_handle_texture)

    system.Add(body_handle)
    
def MIT_stairsHandle(system, center, stair_r, h, theta_f, theta_b):

    width = 1.75
    height = 0.2

    df = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + df*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton front of step

    db = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + db*stair_r + chrono.ChVectorD(0, h, 0)     # Start postiton back of step

    step = shp.step(pos_f, df, pos_b, db, width, height)        # Create each step

    system.Add(step)

    # Add rail pole for stair
    df.SetLength(width)
    db.SetLength(width)
    
    r_pole = 0.02   # Radius
    h_pole = 1.3    # Height
    d_pole = 1      # Density
    texture = 'textures/white concrete.jpg'     # Texture
    pos_pole = (pos_f+pos_b)/2 + (df+db)/2 + chrono.ChVectorD(0, h_pole/2, 0)   # Position

    MIT_add_cylinder(system, r_pole, h_pole*0.95, d_pole, pos_pole, texture)

def MIT_floors(system, H):

    # Add floor, as a box
    floorsNum = 2               # Number of floors
    postNum = 7                 # How many fence post there is to each side of floors center position
    size_floor_x = 20
    size_floor_y = 0.2
    size_floor_z = 4 

    # Add fence, as a cylinder
    fence_r =  0.05        # Radius
    fence_h = 0.8         # Hight
    fence_d = 1           # Density
    texture = 'textures/white concrete.jpg'
    fence_corr = chrono.ChVectorD(0, fence_h/2, 0) # Correction for fence post postition

    for floor in range(floorsNum):
        y_pos = floor*H + H     # Increase floor hight
        floor_pos_1 = chrono.ChVectorD(3, y_pos, 8)     # Add floors left side stair
        floor_pos_2 = chrono.ChVectorD(11, y_pos, -1)      # Add floors right side stair

        MIT_add_box(system, size_floor_x, size_floor_y, size_floor_z, floor_pos_1)
        MIT_add_box(system, size_floor_z, size_floor_y, size_floor_x, floor_pos_2)

        for post in range(postNum):
            # Add fence post to the rigth of the floors center position
            fence_pos_1 = chrono.ChVectorD(0.5+post, y_pos, 8-size_floor_z/2) + fence_corr
            fence_pos_2 = chrono.ChVectorD(11-size_floor_z/2, y_pos, 0+post) + fence_corr# Right side stair

            MIT_add_cylinder(system, fence_r, fence_h, fence_d ,fence_pos_1, texture)
            MIT_add_cylinder(system, fence_r, fence_h, fence_d ,fence_pos_2, texture)

            if post > 0:
                # Add fence post to the left of the floors center position
                fence_pos_3 = chrono.ChVectorD(0.5-post, y_pos, 8-size_floor_z/2) + fence_corr
                fence_pos_4 = chrono.ChVectorD(11-size_floor_z/2, y_pos, 0-post) + fence_corr# Right side stair

                MIT_add_cylinder(system, fence_r, fence_h, fence_d ,fence_pos_3, texture)
                MIT_add_cylinder(system, fence_r, fence_h, fence_d ,fence_pos_4, texture)

    # Add floor piece by the stir
    floor_x = 2
    floor_y = 0.2
    floor_z = 2

    for piece in range(2):
        y_pos = piece*H + H
        floor_pos = chrono.ChVectorD(8, y_pos, 5) 
        
        MIT_add_box(system, floor_x, floor_y, floor_z, floor_pos)

def MIT_add_box(system, size_x, size_y, size_z, floor_pos):

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
    body_floor_texture.SetTextureScale(10, 10)
    body_floor.GetAssets().push_back(body_floor_texture)
    
    system.Add(body_floor)

def MIT_add_cylinder(system, radius, height, density, pos, texture):

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

import pychrono.core as chrono
import numpy as np

from src import Shapes as shp

def Johan_Components(system, SPEEDMODE = False):
    # Create the room: simple fixed rigid bodys with a collision shape
    # and a visualization shape
    Height = 3.32                                   # Height between each floor
    if SPEEDMODE == False:
        center = chrono.ChVectorD(6.5, 0, 3)        # Center position for the stair
        MIT_stair(system, center, Height)           # Add a spiral stair
    MIT_floors(system, Height, SPEEDMODE)           # Add floors
    MIT_walls(system, Height)                       # Add walls

def MIT_stair(system, center, H):
        
    stair_r =  0.3          # Radius
    stair_h = 2*H+0.8       # Hight
    stair_d = 1             # Density
    stepNum = 21            # Number of steps
    dh = (H-0.1)/stepNum    # Heigth between each step
    rad = 1/360*2*np.pi     # Degrees to radians
    texture = 'textures/white concrete.jpg' 
    pos_stair = center + chrono.ChVectorD(0, stair_h/2, 0)  # Correction for stair position

    # Add center cylinder of stair
    add_cylinderShape(system, stair_r, stair_h, stair_d, pos_stair, texture, [10,10]) 
    # Add fake stair to base floor
    add_cylinderShape(system, stair_r+1.7, 0.001, stair_d, center, 'textures/black.jpg', [1,1])

    # Add steps to 3rd floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)    # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum) # Angle between each back step

        add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh, step, stepNum, True)
        add_stairStep(system, center, stair_r, 0, theta_f, theta_b, 0, step, stepNum, False)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, center, stair_r, h, theta_f, theta_b)
            add_stairPosts(system, center, stair_r, 0, theta_f, theta_b)

    # Add steps to 4th floor
    for step in range(stepNum):
        h = step*dh                     
        theta_f = rad*(90 + 270*step/stepNum)       # Angle between each front step
        theta_b = rad*(90 + 270*(step+1)/stepNum)   # Angle between each back step
        pos = center + chrono.ChVectorD(0, H, 0)

        add_stairStep(system, pos, stair_r, h, theta_f, theta_b, dh, step, stepNum, True)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, pos, stair_r, h, theta_f, theta_b)

def add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh, i, stepNum, steps):

    # Add stair step
    width = 1.53    # Step width
    height = 0.1    # Step height
    
    # Create upper half of stair step
    dir_f = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))       # Direction front
    pos_f = center + dir_f*stair_r + chrono.ChVectorD(0, h+3/4*height, 0) # Start postiton front of step

    dir_b = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))       # Direction back
    pos_b = center + dir_b*stair_r + chrono.ChVectorD(0, h+3/4*height, 0) # Start postiton back of step 

    if steps == True:
        step_t = shp.step(pos_f, dir_f, pos_b, dir_b, width, 1/4*height, [0.05,0.03,0.03])
        system.Add(step_t)

    # Create lower half of stair step
    dir_f = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f))   # Direction front
    pos_f = center + dir_f*stair_r + chrono.ChVectorD(0, h, 0)      # Start postiton front of step

    dir_b = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))   # Direction back
    pos_b = center + dir_b*stair_r + chrono.ChVectorD(0, h, 0)      # Start postiton back of step
    
    if steps == True:
        step = shp.step(pos_f, dir_f, pos_b, dir_b, width, 3/4*height, [1, 1, 1])
        system.Add(step)

    # Add stair handle
    add_stairHandle(system, width, dir_f, pos_f, dir_b, pos_b, dh, i, stepNum)

def add_stairHandle(system, width, dir_f, pos_f, dir_b, pos_b, dh, i, stepNum):
    # Add spiral rail for stair
    handle_r = 0.0175     # Radius
    handle_l = 0.445    # Length
    handle_d = 1        # Density
    texture_handle = 'textures/wood_floor.jpg'
    rail_r = 0.025      # Radius
    rail_l = 0.45      # Length
    rail_d = 1          # Density
    texture_rail = 'textures/white concrete.jpg'

    dir_f.SetLength(width)
    dir_b.SetLength(width)
    n = (dir_f+dir_b)/2   
        
    pos_handle = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, 1.3, 0)  # Handle rail
    pos_rail_1 = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, 1, 0)    # Upper support rail
    pos_rail_2 = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + chrono.ChVectorD(0, 0.3, 0)  # Lower support rail

    dist = np.sqrt((dir_f.x-dir_b.x)**2 + (dir_f.y-dir_b.y)**2 + (dir_f.z-dir_b.z)**2)    # Calculate distance between dir_f and dir_b
    alpha = np.arctan((dist+0.07)/dh)
    
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

    width = 1.53

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

def MIT_floors(system, H, SPEEDMODE):

    # Add floor, as a box
    floorsNum = 3               # Number of floors
    postNum = 19                 # Number of fence post on each side of floors center position
    floor_l = 12                # Floor length
    floor_t = 0.08               # Floor thickness
    floor_w = 1.58                # Floor width towards NA
    floor_w_2 = 1.95        # towards technology house
    texture_floor = 'textures/stone_floor.jpg'
    texture_roof = 'textures/white concrete.jpg'
    scale_floor = [10,20] # Texture scale
    scale_roof = [80,10]
    handle_l = 13.5    
    
    for floor in range(floorsNum):
        # Add floors
        y_pos = floor*H - floor_t                              
        floor_pos_1 = chrono.ChVectorD(-3.5, y_pos, 6.58)       # Add floors towards NA
        floor_pos_2 = chrono.ChVectorD(10.45, y_pos, -4-0.42)    # Add floors towards technology house

        add_boxShape(system, floor_l, floor_t, floor_w, floor_pos_1, texture_floor, [20,10])
        add_boxShape(system, floor_w_2, floor_t, floor_l+0.58, floor_pos_2, texture_floor, [10,20])

        if floor > 0 and SPEEDMODE == False:
            add_fence(system, H, postNum, floor_w, floor_w_2, floor, floor_t, handle_l)
    
    for roof in range(floorsNum):
        # Add roof 
        y_pos = roof*H - 3*floor_t                              
        roof_pos_1 = chrono.ChVectorD(-3.5, y_pos, 6.58)          # Add roof towards NA
        roof_pos_2 = chrono.ChVectorD(10.45, y_pos, -4-0.42)       # Add roof towards technology house

        add_boxShape(system, floor_l, floor_t, floor_w, roof_pos_1, texture_roof, scale_roof)
        add_boxShape(system, floor_w_2, floor_t, floor_l+0.58, roof_pos_2, texture_roof, scale_roof)

    # Add floor piece by the stair
    floor_x = 1.03
    floor_z = 1.03

    for piece in range(floorsNum):
        y_pos = piece*H - floor_t*0.999
        floor_pos = chrono.ChVectorD(7.5, y_pos+0.002, 4) 
        
        add_boxShape(system, floor_x, floor_t, floor_z, floor_pos, texture_floor, [4,3])
    
    for piece in range(floorsNum):
        if piece > 0:
            y_pos = piece*H - 3*floor_t
            floor_pos = chrono.ChVectorD(7.5, y_pos+0.002, 4) 
            
            add_boxShape(system, floor_x, floor_t, floor_z, floor_pos, texture_roof, scale_roof)

    # Add walkway towards umu library
    length = 10
    width = 2
    for i in range(2):
        y = i*H + H - floor_t
        pos = chrono.ChVectorD(16.5, y, 10.16)

        add_boxShape(system, length, floor_t, width, pos, texture_floor, scale_floor)
    
    for i in range(2):
        y = i*H + H - 3*floor_t
        pos = chrono.ChVectorD(16.5, y, 10.16)

        add_boxShape(system, length, floor_t, width, pos, texture_roof, scale_roof)

    # Add MIT entrence floor
    pos = chrono.ChVectorD(7.25, 0-floor_t, 10.16)
    add_boxShape(system, 5.25, floor_t, 2, pos, texture_floor, scale_floor)

    # Add MIT top floor roof over entrence
    pos = chrono.ChVectorD(9.5, 0+3*H+floor_t, 10.16)
    add_boxShape(system, 3, floor_t, 2, pos, texture_roof, scale_roof)

    # Add MIT roof over entrence
    pos = chrono.ChVectorD(4.25, 0+H-2*floor_t, 10.16)
    add_boxShape(system, 2.25, 2*floor_t, 2, pos, texture_roof, scale_roof)

    # Add horizontal beam along floors
    beam_length = 6.9
    for floor in range(floorsNum):
        beam_corr_2 = floor_w_2+0.99*floor_t/2      # Technology
        beam_corr = floor_w+0.99*floor_t/2      # Na
        if floor > 0:
            y_pos = floor*H - 2*floor_t                             
            floor_pos_1 = chrono.ChVectorD(0, y_pos, 6.58-beam_corr)       # Add beam left side stair
            floor_pos_2 = chrono.ChVectorD(10.45-beam_corr_2, y_pos, -4)   # Add beam right side stair

            add_boxShape(system, beam_length, 2*floor_t, floor_t/2, floor_pos_1, 'textures/white concrete.jpg')
            add_boxShape(system, floor_t/2, 2*floor_t, beam_length, floor_pos_2, 'textures/white concrete.jpg')

def MIT_walls(system, H):

    # Add main walls as a box 
    wall_t = 0.1
    wall_h = 3/2*H
    wall_l = 8
    texture_wall = 'textures/yellow_brick.jpg'
    office_wall = 'textures/MITwall_dark.jpg'
    scale = [10,10]   # Texture scale
    
    pos_1 = chrono.ChVectorD(12.5+wall_t, 0, -1) + chrono.ChVectorD(0, wall_h, 0)
    pos_2 = chrono.ChVectorD(-7.5-wall_t, 0, -3) + chrono.ChVectorD(0, wall_h, 0)
    pos_3_3 = chrono.ChVectorD(-4.5, 0+3/2*H, 8.16+wall_t)
    pos_3_4 = chrono.ChVectorD(-4.5-wall_t, 5/2*H, 8.16+wall_t)
    pos_4 = chrono.ChVectorD(0.5, 0, -11-wall_t) + chrono.ChVectorD(0, wall_h, 0)

    add_boxShape(system, wall_t, wall_h, 10, pos_1, texture_wall, [10,10]) # Positive x direction
    add_boxShape(system, wall_t, wall_h, wall_l, pos_2, office_wall, [4,3]) # Negative x direction
    add_boxShape(system, 11, H/2, wall_t, pos_3_3, texture_wall, [10,10]) # Positive z direction
    add_boxShape(system, 11-wall_t, H/2, wall_t, pos_3_4, texture_wall, [10,10]) # Positive z direction
    add_boxShape(system, wall_l, wall_h, wall_t, pos_4, office_wall, [-4,-3])    # Negative z direction
    
    # Add support colums as a box
    beam_h = 3/2*H
    beam_w = 0.08
    beam_pos_1 = chrono.ChVectorD(4.5, 0+2/3*beam_h, 5)     # Close left of stair
    beam_pos_2 = chrono.ChVectorD(-2.5, 0+beam_h, 5)        # Left of stair
    beam_pos_3 = chrono.ChVectorD(8.5, 0+beam_h, 1)         # Close right of stair
    beam_pos_4 = chrono.ChVectorD(8.5, 0+beam_h, -7)        # Right of stair
    beam_pos_5 = chrono.ChVectorD(8.5, 0+beam_h, 5)         # Middle beam
    beam_pos_6 = chrono.ChVectorD(-7.5-wall_t, 0+beam_h, 5) # Far left bream
    beam_pos_7 = chrono.ChVectorD(8.5, 0+beam_h, -11-wall_t) # Far right beam

    add_boxShape(system, beam_w, 2/3*beam_h, beam_w, beam_pos_1, 'textures/white concrete.jpg', scale)
    add_boxShape(system, beam_w, 2/6*beam_h, beam_w, beam_pos_2, 'textures/white concrete.jpg', scale)
    add_boxShape(system, beam_w, beam_h, beam_w, beam_pos_3, 'textures/white concrete.jpg', scale)
    add_boxShape(system, beam_w, beam_h, beam_w, beam_pos_4, 'textures/white concrete.jpg', scale)
    add_boxShape(system, beam_w, beam_h, beam_w, beam_pos_5, 'textures/white concrete.jpg', scale)
    add_boxShape(system, beam_w, 1/3*beam_h, beam_w, beam_pos_6, 'textures/white concrete.jpg', scale)
    add_boxShape(system, beam_w, beam_h, beam_w, beam_pos_7, 'textures/white concrete.jpg', scale)

    # Add wall, 4th floor towards MIT place
    topWall_pos = chrono.ChVectorD(-0.5-wall_t, 5/2*H, 5.1)
    add_boxShape(system, 7-wall_t, H/2, wall_t, topWall_pos, office_wall, [2,1])

    # Add wall, 2nd floor towards MIT place
    bWall_height = H/2-wall_t
    pos = chrono.ChVectorD(-2.5-3*wall_t, 0+bWall_height, 5+wall_t)
    add_boxShape(system, 5-3*wall_t, bWall_height, wall_t, pos, 'textures/wwp.png', scale)

    # Add wall, 4th floor flower pot (Negative x direction)
    pos = chrono.ChVectorD(6.5-wall_t, 5/2*H, 6.88+wall_t)
    add_boxShape(system, wall_t, H/2, 1.88+wall_t, pos, 'textures/white concrete.jpg', [5,5])

    # Add wall, 2nd floor towards NA (positive z direction)
    pos = chrono.ChVectorD(-6.75-wall_t, 0+H/2, 8.16+wall_t)
    add_boxShape(system, 8.75-wall_t, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add wall, 3nd floor (negative x direction) MIT info screen
    pos = chrono.ChVectorD(6.5-wall_t, 0+3/2*H , 10.16+wall_t)
    add_boxShape(system, wall_t, H/2, 2-wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add wall, 4nd floor (negative x direction) data cooridor
    pos = chrono.ChVectorD(6.5-wall_t, 0+5/2*H , 10.46+wall_t)
    add_boxShape(system, wall_t, H/2, 1.7-wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add wall, 3rd floor NA corridor end (negative x direction)
    pos = chrono.ChVectorD(-15.5-wall_t, 0+3/2*H , 7)
    add_boxShape(system, wall_t, H/2, 2, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add entrence wall (positive x direction)
    pos = chrono.ChVectorD(12.5+wall_t, 0+H/2-0.1, 10.16)
    add_boxShape(system, wall_t, H/2-0.1, 2, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add 2nd entrence wall (negative x direction)
    pos = chrono.ChVectorD(2-wall_t, 0+H/2-0.1, 7+wall_t)
    add_boxShape(system, wall_t, H/2-0.1, 2-wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add 1st entrence wall (negative x direction)
    pos = chrono.ChVectorD(2-wall_t, 0+H/2-0.1, 10.16)
    add_boxShape(system, wall_t, H/2-0.1, 2, pos, 'textures/white concrete.jpg', [5,5])

    # Add top floor wall (positive x direction)
    pos = chrono.ChVectorD(12.5+wall_t, 0+5/2*H, 11)
    add_boxShape(system, wall_t, H/2, 2, pos, 'textures/yellow_brick.jpg', [2,2])

    # Add wall towards mitum (negative x direction)
    pos = chrono.ChVectorD(8.5-wall_t, 0+3/2*H, -14-wall_t)
    add_boxShape(system, wall_t, 3/2*H, 3-wall_t, pos, 'textures/yellow_brick.jpg', [10,7])

    # Add wall towards mitum (positive x direction)
    pos = chrono.ChVectorD(12.5+wall_t, 0+3/2*H, -14)
    add_boxShape(system, wall_t, 3/2*H, 3, pos, 'textures/yellow_brick.jpg', [10,7])

    # Add wall, 3rd floor towards NA (negative z direction)
    pos = chrono.ChVectorD(-11.5-wall_t, 0+3/2*H, 5-wall_t)
    add_boxShape(system, 4-wall_t, 3/2*H, wall_t, pos, 'textures/yellow_brick.jpg', [10,7])

    # Add wall, 3rd floor towards MIT fountain
    pos = chrono.ChVectorD(11.5, 3/2*H, 12.16+wall_t)
    add_boxShape(system, 5, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add wall, 3rd floor wall, rigth hand side towards UMU library (negative z direction)
    pos = chrono.ChVectorD(14.5+2*wall_t, 3/2*H, 9-wall_t)
    add_boxShape(system, 2, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [3,3])

    # Add wall, 4th floor wall towards MIT fountain
    pos = chrono.ChVectorD(9.5, 5/2*H, 12.16+wall_t)
    add_boxShape(system, 3, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add elevator shaft
    for floor in range(3):
        y_pos = H*floor + H/2
        pos = chrono.ChVectorD(10.5, y_pos, 12.16)
        add_boxShape(system, 3.34, H/2, wall_t, pos, 'textures/elevator.png', [4,3])

    # Add end wall, towards mitum
    texture = ['textures/mit_2nd.jpg', 'textures/mit_3rd.jpg', 'textures/mit_4th.jpg']
    for floor in range(3):
        y_pos = H*floor + H/2
        pos = chrono.ChVectorD(10.5, y_pos, -17)
        add_boxShape(system, 2, H/2, wall_t, pos, texture[floor], [-4,-3])

def add_boxShape(system, size_x, size_y, size_z, pos, texture, scale = [5,5]):

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
    body_box_texture.SetTextureScale(scale[0], scale[1])
    body_box.GetAssets().push_back(body_box_texture)
    
    system.Add(body_box)

def add_cylinderShape(system, radius, height, density, pos, texture, scale = [5,5]):

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
    body_cylinder_texture.SetTextureScale(scale[0], scale[1])
    body_cylinder.GetAssets().push_back(body_cylinder_texture)

    system.Add(body_cylinder)

def add_fence(system, H, postNum, floor_w, floor_w_2, floor, floor_t, handle_l):

    # Add fence post, as a cylinder
    fence_r =  0.02         # Radius
    fence_h = 1.04          # Hight
    fence_d = 1             # Density
    texture = 'textures/white concrete.jpg'
    fence_corr = chrono.ChVectorD(0, fence_h/2, 0) # Correction for fence post postition

    # Add handle for each floor
    handle_r = 0.0175         # Radius
    handle_d = 1            # Density
    n_x = chrono.ChVectorD(1, 0, 0)     # Normalvector in x direction
    n_z = chrono.ChVectorD(0, 0, 1)     # Normalvector in z direction
    # Handle
    pos_rail_1 = chrono.ChVectorD(-0.75, H+fence_h*0.99, 6.58-floor_w)         # Fence 3rd floor left of stair
    pos_rail_2 = chrono.ChVectorD(10.45-floor_w_2, H+fence_h*0.99, -4.4)       # Fence 3rd floor
    pos_rail_3 = chrono.ChVectorD(10.45-floor_w_2, 2*H+fence_h*0.99, -4.4)     # Fence 4th floor
    pos_rail_4 = chrono.ChVectorD(6.5, 2*H+fence_h*0.99, 4.2)               # Fence by the stair 4th floor
    # Rail
    pos_rail_5 = chrono.ChVectorD(-0.75, H+3/4*fence_h, 6.58-floor_w)         # Fence 3rd floor left of stair
    pos_rail_6 = chrono.ChVectorD(10.45-floor_w_2, H+3/4*fence_h, -4.4)       # Fence 3rd floor
    pos_rail_7 = chrono.ChVectorD(10.45-floor_w_2, 2*H+3/4*fence_h, -4.4)     # Fence 4th floor
    pos_rail_8 = chrono.ChVectorD(6.5, 2*H+3/4*fence_h, 4.2)               # Fence by the stair 4th floor

    pos_h = [pos_rail_1, pos_rail_2, pos_rail_3, pos_rail_4]
    pos_r = [pos_rail_5, pos_rail_6, pos_rail_7, pos_rail_8]
    dirr = [n_z, n_x, n_x, n_x]
    handle_length = [handle_l, handle_l, handle_l, 2]
    dl = (handle_l)/postNum     # Delta lenght between each post
    
    # Handle rail
    for num in range(len(pos_h)):
        pos_rail = pos_h[num]
        n = dirr[num]
        length = handle_length[num]
            
        body = chrono.ChBodyEasyCylinder(handle_r, length, handle_d) # Cylinder size
        body.SetBodyFixed(True)
        body.SetPos(pos_rail)
            
        qr = chrono.Q_from_AngAxis(np.pi/2, n.GetNormalized())    # Rotate cylinder
        quaternion = qr * body.GetRot()
        body.SetRot(quaternion)

        # Collision shape
        body.GetCollisionModel().ClearModel()
        body.GetCollisionModel().AddCylinder(handle_r, handle_l, handle_d) # hemi sizes
        body.GetCollisionModel().BuildModel()
        body.SetCollide(True)

        # Body texture
        body_texture = chrono.ChTexture()
        body_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
        body.GetAssets().push_back(body_texture)

        system.Add(body)
    # Support rail
    for num in range(len(pos_r)):
        pos_rail = pos_r[num]
        n = dirr[num]
        length = handle_length[num]
            
        body = chrono.ChBodyEasyCylinder(fence_r, length, handle_d) # Cylinder size
        body.SetBodyFixed(True)
        body.SetPos(pos_rail)
            
        qr = chrono.Q_from_AngAxis(np.pi/2, n.GetNormalized())    # Rotate cylinder
        quaternion = qr * body.GetRot()
        body.SetRot(quaternion)

        # Collision shape
        body.GetCollisionModel().ClearModel()
        body.GetCollisionModel().AddCylinder(handle_r, handle_l, handle_d) # hemi sizes
        body.GetCollisionModel().BuildModel()
        body.SetCollide(True)

        # Body texture
        body_texture = chrono.ChTexture()
        body_texture.SetTextureFilename(chrono.GetChronoDataFile(texture))
        body.GetAssets().push_back(body_texture)

        system.Add(body)

    for post in range(postNum):
        y_pos = floor*H - floor_t
        pos_l = chrono.ChVectorD((-0.7-handle_l/2)+post*dl, H-floor_t, 6.58-floor_w) + fence_corr  # Left side stair  
        pos_r = chrono.ChVectorD(10.45-floor_w_2, y_pos, (-4.4-handle_l/2)+post*dl) + fence_corr # Right side stair

        add_cylinderShape(system, fence_r, fence_h, fence_d , pos_r, texture)
        add_cylinderShape(system, fence_r, fence_h, fence_d , pos_l, texture)

    for post in range(3):
        pos = chrono.ChVectorD(6.5, 2*H-floor_t, 3.5+post*dl) + fence_corr

        add_cylinderShape(system, fence_r, fence_h, fence_d , pos, texture)
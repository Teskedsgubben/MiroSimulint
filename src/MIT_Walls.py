from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

def build(system, SPEEDMODE = False):
    # Create the room: simple fixed rigid bodys with a collision shape
    # and a visualization shape
    Height = 3.32                                   # Height between each floor
    center = np.array([6.5, 0, 3])                  # Center position for the stair
    MIT_stair(system, center, Height, SPEEDMODE)    # Add a spiral stair
    MIT_floors(system, Height, SPEEDMODE)           # Add floors
    MIT_walls(system, Height)                       # Add walls

def MIT_stair(system, center, H, SPEEDMODE):
    stair_r =  0.3          # Radius
    stair_h = 2*H+1         # Hight
    stair_d = 1             # Density
    stepNum = 21            # Number of steps
    dh = (H-0.1)/stepNum    # Heigth between each step
    rad = 1/360*2*np.pi     # Degrees to radians
    texture = 'textures/white concrete.jpg' 
    pos_stair = center + np.array([0,stair_h/2, 0]) #chrono.ChVectorD(0, stair_h/2, 0)  # Correction for stair position
    pos_disk = center + np.array([0, stair_h+0.025, 0])#chrono.ChVectorD(0, stair_h+0.025, 0)
    
    # Add center cylinder of stair
    MiroAPI.add_cylinderShape(system, stair_r, stair_h, stair_d, pos_stair, texture, [10,10])

    # If SPEEDMODE is activated, stop here
    if SPEEDMODE:
        return
    
    # Top disk
    MiroAPI.add_cylinderShape(system, stair_r+0.01, 0.05, 1, pos_disk, 'textures/MIT_stone_floor.jpg', [1/8,1/8]) 
    # Add fake stair to base floor
    MiroAPI.add_cylinderShape(system, stair_r+1.7, 0.001, stair_d, center, 'textures/black.jpg', [1,1])

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
        pos = center + np.array([0,H,0])

        add_stairStep(system, pos, stair_r, h, theta_f, theta_b, dh, step, stepNum, True)

        # Add fence post for stair
        if step % 2 == 0:           
            add_stairPosts(system, pos, stair_r, h, theta_f, theta_b)

def add_stairStep(system, center, stair_r, h, theta_f, theta_b, dh, i, stepNum, steps):

    # Add stair step
    width = 1.53    # Step width
    height = 0.1    # Step height
    
    # Create upper half of stair step
    dir_f = np.array([np.cos(theta_f),0,np.sin(theta_f)])
    pos_f = center + dir_f*stair_r + np.array([0, h+3/4*height, 0])

    dir_b = np.array([np.cos(theta_b),0,np.sin(theta_b)])
    pos_b = center + dir_b*stair_r + np.array([0, h+3/4*height, 0])

    if steps == True:
        step_t = MiroAPI.stepShape(pos_f, dir_f, pos_b, dir_b, width, 1/4*height, [0.05,0.03,0.03])
        system.Add(step_t)

    # Create lower half of stair step
    dir_f = np.array([np.cos(theta_f), 0, np.sin(theta_f)])   # Direction front
    pos_f = center + dir_f*stair_r + np.array([0, h, 0])     # Start postiton front of step

    dir_b = np.array([np.cos(theta_b), 0, np.sin(theta_b)])   # Direction back
    pos_b = center + dir_b*stair_r + np.array([0, h, 0])      # Start postiton back of step

    if steps == True:
        step = MiroAPI.stepShape(pos_f, dir_f, pos_b, dir_b, width, 3/4*height, [1, 1, 1])
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

    dir_f = width*dir_f/np.linalg.norm(dir_f)
    dir_b = width*dir_b/np.linalg.norm(dir_b)
    n = (dir_f+dir_b)/2   

    pos_handle = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + np.array([0, 1.3, 0])  # Handle rail
    pos_rail_1 = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + np.array([0, 1, 0])    # Upper support rail
    pos_rail_2 = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + np.array([0, 0.3, 0])  # Lower support rail

    dist = np.sqrt((dir_f[0]-dir_b[0])**2 + (dir_f[1]-dir_b[1])**2 + (dir_f[2]-dir_b[2])**2)    # Calculate distance between dir_f and dir_b
    alpha = np.pi/2
    if dh > 0:
        alpha = np.arctan((dist+0.07)/dh)
    
    MiroAPI.add_cylinderShape(system, handle_r, handle_l, handle_d, pos_handle, texture_handle, rotAngle=alpha, rotAxis=n,rotDegrees=False )
   
    if 0 < i and i < stepNum-1:
        MiroAPI.add_cylinderShape(system, rail_r, rail_l, rail_d, pos_rail_1, texture_rail, rotAngle=alpha, rotAxis=n,rotDegrees=False )
        MiroAPI.add_cylinderShape(system, rail_r, rail_l, rail_d, pos_rail_2, texture_rail, rotAngle=alpha, rotAxis=n,rotDegrees=False )

def add_stairPosts(system, center, stair_r, h, theta_f, theta_b):

    width = 1.53

    dir_f = np.array([np.cos(theta_f), 0, np.sin(theta_f)])   # Direction front of step
    pos_f = center + dir_f*stair_r + np.array([0, h, 0]) 

    dir_b = np.array([np.cos(theta_b), 0, np.sin(theta_b)])   # Direction back of step
    pos_b = center + dir_b*stair_r + np.array([0, h, 0]) 

    # Add rail pole for stair
    post_r = 0.02   # Radius
    post_h = 1.3    # Height
    post_d = 1      # Density
    texture = 'textures/white concrete.jpg'
    dir_f = width*dir_f/np.linalg.norm(dir_f)
    dir_b = width*dir_b/np.linalg.norm(dir_b)
    pos_pole = (pos_f+pos_b)/2 + (dir_f+dir_b)/2 + np.array([0, post_h/2, 0])   # Position

    MiroAPI.add_cylinderShape(system, post_r, post_h, post_d, pos_pole, texture, rotDegrees=False)

def MIT_floors(system, H, SPEEDMODE):

    # Add floor, as a box
    floorsNum = 3               # Number of floors
    postNum = 19                 # Number of fence post on each side of floors center position
    floor_l = 12                # Floor length
    floor_t = 0.08               # Floor thickness
    floor_w = 1.58                # Floor width towards NA
    floor_w_2 = 1.95 +2.11       # towards technology house
    texture_floor = ['textures/MIT_stone_floor.jpg', 'textures/MIT_story_floor.jpg', 'textures/MIT_story_floor.jpg']
    texture_roof = 'textures/MIT_inner_roof.jpg'
    scale_roof = [80,10]
    handle_l = 13.5    
    
    for floor in range(floorsNum):
        # Add floors
        y_pos = floor*H - floor_t
        floor_pos_1 = np.array([-3.5, y_pos, 6.58])       # Add floors towards NA
        floor_pos_2 = np.array([10.45+2.11, y_pos, -4-0.42])    # Add floors towards technology house
        floor_pos_3 = np.array([-10.2, y_pos, -7])      # Add floor in NTK cooriodor
        floor_pos_4 = np.array([1.5, y_pos, -13.45])      # Add floor in NTK cooriodor (-z direction)

        MiroAPI.add_boxShapeHemi(system, floor_l, floor_t, floor_w, floor_pos_1, texture_floor[floor], [50,3.6])
        MiroAPI.add_boxShapeHemi(system, floor_w_2, floor_t, floor_l+0.58, floor_pos_2, texture_floor[floor], [18,28])
        MiroAPI.add_boxShapeHemi(system, 0.85, floor_t, floor_l, floor_pos_3, texture_floor[floor], [50,3.6])
        MiroAPI.add_boxShapeHemi(system, 7, floor_t, 0.85, floor_pos_4, texture_floor[floor], [18,28])

        if floor > 0 and SPEEDMODE == False:
            add_fence(system, H, postNum, floor_w, floor_w_2, floor, floor_t, handle_l)
    
    for roof in range(floorsNum):
        # Add roof 
        y_pos = roof*H - 3*floor_t #+0.025
        roof_pos_1 = np.array([-3.5, y_pos, 6.58])          # Add roof towards NA
        roof_pos_2 = np.array([10.45+2.11, y_pos, -4-0.42]) # Add roof towards technology house
        roof_pos_3 = np.array([-10.2, y_pos, -7])      # Add roof in NTK cooriodor (-x direction)
        roof_pos_4 = np.array([1.5, y_pos, -13.45])      # Add roof in NTK cooriodor (-z direction)

        MiroAPI.add_boxShapeHemi(system, floor_l, floor_t, floor_w, roof_pos_1, texture_roof, [100, 10])
        MiroAPI.add_boxShapeHemi(system, floor_w_2, floor_t, floor_l+0.58, roof_pos_2, texture_roof, [35,80])
        MiroAPI.add_boxShapeHemi(system, 0.85, floor_t, floor_l, roof_pos_3, texture_roof, [35,80])
        MiroAPI.add_boxShapeHemi(system, 7, floor_t, 0.85, roof_pos_4, texture_roof, [100,10])

    # Office floors
    for floor in range(floorsNum):
        # Add floors
        y_pos = floor*H - floor_t
        floor_pos_3 = np.array([-7.425, y_pos, -7])      # Add roof in NTK cooriodor (-x direction)
        floor_pos_4 = np.array([1.5, y_pos, -10.8])      # Add roof in NTK cooriodor (-z direction)
        MiroAPI.add_boxShapeHemi(system, 1.925, floor_t, floor_l, floor_pos_3, 'textures/BHgang.jpg', [35,80])
        MiroAPI.add_boxShapeHemi(system, 7, floor_t, 1.8, floor_pos_4, 'textures/BHgang.jpg', [100,10])

    for roof in range(floorsNum):
        # Add roof
        y_pos = roof*H - 3*floor_t
        roof_pos_3 = np.array([-7.425, y_pos, -7])      # Add roof in NTK cooriodor (-x direction)
        roof_pos_4 = np.array([1.5, y_pos, -10.8])      # Add roof in NTK cooriodor (-z direction)
        MiroAPI.add_boxShapeHemi(system, 1.925, floor_t, floor_l, roof_pos_3, texture_roof, [35,80])
        MiroAPI.add_boxShapeHemi(system, 7, floor_t, 1.8, roof_pos_4, texture_roof, [100,10])

    # Add floor piece by the stair
    floor_x = 1.03
    floor_z = 1.03

    for piece in range(floorsNum):
        y_pos = piece*H - floor_t*0.999
        floor_pos = np.array([7.5, y_pos+0.002, 4]) 
        
        MiroAPI.add_boxShapeHemi(system, floor_x, floor_t, floor_z, floor_pos, texture_floor[0], [4,2])
    
    for piece in range(floorsNum):
        if piece > 0:
            y_pos = piece*H - 3*floor_t
            floor_pos = np.array([7.5, y_pos+0.002, 4]) 
            
            MiroAPI.add_boxShapeHemi(system, floor_x, floor_t, floor_z, floor_pos, texture_roof, [12,9])

    # Add walkway towards umu library
    length = 10.5
    width = 2
    for i in range(2):
        y = i*H + H - floor_t
        pos = np.array([10, y, 10.16])

        MiroAPI.add_boxShapeHemi(system, length, floor_t, width, pos, texture_floor[1], [48.9,6])
    
    for i in range(2):
        y = i*H + H - 3*floor_t
        pos = np.array([10, y, 10.16])

        MiroAPI.add_boxShapeHemi(system, length, floor_t, width, pos, texture_roof, scale_roof)

    # Add MIT entrence floor
    pos = np.array([6.2, 0-floor_t, 10.16])
    MiroAPI.add_boxShapeHemi(system, 6.5, floor_t, 2, pos, texture_floor[0], [30,6])

    # Add horizontal beam along floors
    beam_length = 5.87
    for floor in range(floorsNum):
        beam_corr_2 = floor_w_2+0.99*floor_t/2      # Technology
        beam_corr = floor_w+0.99*floor_t/2      # Na
        if floor > 0:
            y_pos = floor*H - 2*floor_t                             
            floor_pos_1 = np.array([0.63, y_pos, 6.58-beam_corr])       # Towards NA
            floor_pos_2 = np.array([10.45+2.11-beam_corr_2, y_pos, -2.9])   # Towards technology

            MiroAPI.add_boxShapeHemi(system, beam_length, 2*floor_t, floor_t/2, floor_pos_1, 'textures/white concrete.jpg')
            MiroAPI.add_boxShapeHemi(system, floor_t/2, 2*floor_t, beam_length, floor_pos_2, 'textures/white concrete.jpg')

def MIT_walls(system, H):

    # Add main walls as a box 
    wall_t = 0.1
    wall_h = 3/2*H
    texture_wall = 'textures/yellow_brick.jpg'
    scale = [10,10]   # Texture scale

    pos_3_3 = np.array([-4.5, 0+3/2*H, 8.16+wall_t])
    pos_3_4 = np.array([-4.5-wall_t, 5/2*H, 8.16+wall_t])

    MiroAPI.add_boxShapeHemi(system, 11, H/2, wall_t, pos_3_3, texture_wall, [10,10]) # Positive z direction
    MiroAPI.add_boxShapeHemi(system, 11-wall_t, H/2, wall_t, pos_3_4, texture_wall, [10,10]) # Positive z direction
    
    # Add support colums as a box
    beam_h = 3/2*H
    beam_w = 0.08
    beam_pos_1 = np.array([4, 0+beam_h, 5])     # Close left of stair
    beam_pos_2 = np.array([-0.8, 0+4/3*beam_h, 5])        # Left of stair
    beam_pos_3 = np.array([8.5, 0+beam_h, 0.5])         # Close right of stair
    beam_pos_4 = np.array([8.5, 0+beam_h, -4.3])        # Right of stair
    beam_pos_5 = np.array([8.5, 0+beam_h, 5])         # Middle beam

    MiroAPI.add_boxShapeHemi(system, beam_w, beam_h, beam_w, beam_pos_1, 'textures/white concrete.jpg', scale)
    MiroAPI.add_boxShapeHemi(system, beam_w, 2/3*beam_h, beam_w, beam_pos_2, 'textures/white concrete.jpg', scale)
    MiroAPI.add_boxShapeHemi(system, beam_w, beam_h, beam_w, beam_pos_3, 'textures/white concrete.jpg', scale)
    MiroAPI.add_boxShapeHemi(system, beam_w, beam_h, beam_w, beam_pos_4, 'textures/white concrete.jpg', scale)
    MiroAPI.add_boxShapeHemi(system, beam_w, beam_h, beam_w, beam_pos_5, 'textures/white concrete.jpg', scale)

    # Beams along wall
    for beam in range(5):
        x = 12.75 + beam*0.46
        z = 8.16+0.05+wall_t - beam*4.47
        beam_pos = np.array([x, 0+beam_h, z])
        MiroAPI.add_boxShapeHemi(system, beam_w, beam_h, beam_w, beam_pos, 'textures/white concrete.jpg', scale)

    #-------------2nd floor---------------

    # Add wall, 2nd floor towards MIT place
    bWall_height = H/2-wall_t
    pos = np.array([-1.82, 0+bWall_height, 5+wall_t])
    MiroAPI.add_boxShapeHemi(system, 3.48, bWall_height, wall_t, pos, 'textures/storage_wall.jpg', [12,15])

    # Add wall, 2nd floor towards NA (positive z direction)
    pos = np.array([-7, H/2, 8.16+wall_t])
    MiroAPI.add_boxShapeHemi(system, 8.75-wall_t, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add entrence wall (positive x direction)
    pos = np.array([12.7+wall_t, 0+H/2-0.1, 10.18])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2-0.1, 1.9, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add entrence wall (negative x direction)
    pos = np.array([-0.4, 0+H/2-0.16, 9.86])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2-0.16, 1.5, pos, 'textures/door_cs.jpg', [4,3],Collide=False)

    # Add entrence corridor (negative x direction)
    pos = np.array([0.65, 0+H/2-0.1, 11.41])
    MiroAPI.add_boxShapeHemi(system, 1, H/2-0.1, wall_t, pos, 'textures/white concrete.jpg', [5,5])

    # Add 2nd entrence wall (negative x direction)
    pos = np.array([1.6, 0+H/2-0.1, 6.5+wall_t+0.01+0.05])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2-0.1, 1.5+wall_t+0.05, pos, 'textures/yellow_brick.jpg', [5,5])

    #-------------3rd floor---------------

    # Add wall, 3rd floor (negative x direction) MIT info screen
    pos = np.array([6.5-wall_t, 0+3/2*H-0.16, 10.16+wall_t])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2-0.16, 2-wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add wall, 3rd floor towards NA 1 (negative z direction)
    pos = np.array([-7.6, 0+3/2*H, 5.65])
    MiroAPI.add_boxShapeHemi(system, 1.75, H/2, wall_t, pos, 'textures/white concrete.jpg', [10,7])

    # Add wall, 3rd floor towards NA 2 (negative z direction)
    pos = np.array([-11.3, 0+3/2*H, 5.65])
    MiroAPI.add_boxShapeHemi(system, 0.25, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [1,1], False)

    # Add wall, 3rd floor corridor towards NTK (negative x direction)
    for wall in range(2):
        x = -11.05 + wall*(1.71+wall_t)
        pos = np.array([x, 0+3/2*H, 5.25])
        MiroAPI.add_boxShapeHemi(system, wall_t, H/2, 0.4, pos, 'textures/yellow_brick.jpg', [1,1], False)

    # Add wall, 3rd floor NTK door (negative z direction)
    # pos = np.array([-10.2, 0+3/2*H, 5])
    # MiroAPI.add_boxShapeHemi(system, 0.85, H/2, wall_t, pos, 'textures/door_ntk.jpg', [-4,-3], False)

    # Add wall, 3rd floor NA corridor end (negative x direction)
    pos = np.array([-11.55, 3/2*H-0.16 , 6.95])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2-0.16, 1.25, pos, 'textures/mit_3rd_na2.jpg', [4,3])

    # Add wall, 3rd floor towards MIT fountain
    pos = np.array([11.65, 3/2*H, 12.16+wall_t])
    MiroAPI.add_boxShapeHemi(system, 5.15, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [5,5])

    # Add wall, 3rd floor wall, left hand side towards UMU library (negative z direction)
    pos = np.array([18.3, 3/2*H-wall_t, 12.16+wall_t])
    MiroAPI.add_boxShapeHemi(system, 1.5, H/2-wall_t, wall_t, pos, 'textures/white concrete.jpg', [3,3])

    # Add wall, 3rd floor UMU library end (negative x direction)
    pos = np.array([19.9, 3/2*H-0.16 , 10.56])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2-0.16, 1.6, pos, 'textures/mit_3rd_sam.jpg', [-4,-3])

    #-------------4th floor---------------  

    # Add wall, 4th floor flower pot (Negative x direction)
    pos = np.array([6.5-wall_t+0.01, 5/2*H, 7.08+wall_t+0.01])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2, 2.08+wall_t, pos, 'textures/white concrete.jpg', [5,5])

    # Add wall, 4th floor data cooridor (negative x direction) 
    pos = np.array([5.5-wall_t, 0+5/2*H , 10.66+wall_t])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2, 1.5-wall_t, pos, 'textures/door_cs.jpg', [4,3], Collide=False)

    # Add 4th floor wall (positive x direction)
    pos = np.array([12.7+wall_t, 0+5/2*H, 10.18])
    MiroAPI.add_boxShapeHemi(system, wall_t, H/2, 1.9, pos, 'textures/yellow_brick.jpg', [2,2])

    # Add wall, 4th floor towards NA (negative z direction)
    pos = np.array([-9.3-wall_t, 0+5/2*H, 5-wall_t])
    MiroAPI.add_boxShapeHemi(system, 4-wall_t, H/2, wall_t, pos, 'textures/yellow_brick.jpg', [10,7], False)

    # Add wall, 4th floor wall towards MIT fountain
    pos = np.array([9, 5/2*H, 12.16+wall_t])
    MiroAPI.add_boxShapeHemi(system, 3.5, H/2, wall_t, pos, 'textures/white concrete.jpg', [5,5])

    #----------------Other----------------

    # Add white wall extension, technology
    pos = np.array([9.9, 3/2*H, -8.8-wall_t])
    MiroAPI.add_boxShapeHemi(system, 1.4, 3/2*H, wall_t, pos, 'textures/white concrete.jpg', [5,5])

    # Add wall towards technology building  (negative x direction)
    pos = np.array([8.5-wall_t+2.8, 0+3/2*H, -11.8-wall_t+1.1])
    MiroAPI.add_boxShapeHemi(system, wall_t, 3/2*H, 1.9-wall_t, pos, 'textures/white concrete.jpg', [10,10])

    # Add office cooridor wall (negative x direction)
    pos = np.array([-11.05, 0+3/2*H, -7])
    MiroAPI.add_boxShapeHemi(system, wall_t, 3/2*H, 12, pos, 'textures/white concrete.jpg', [10,10])

    # Add office wall (negative x direction)
    pos = np.array([-9.35, 0+3/2*H, -1.9])
    MiroAPI.add_boxShapeHemi(system, wall_t, 3/2*H, 6.9, pos, 'textures/white concrete.jpg', [10,10])

    # Add office wall (negative z direction)
    pos = np.array([1.5, 0+3/2*H, -12.6])
    MiroAPI.add_boxShapeHemi(system, 7, 3/2*H, wall_t, pos, 'textures/white concrete.jpg', [10,10])

    # Add office cooridor wall (negative z direction)
    pos = np.array([1.5, 0+3/2*H, -14.3])
    MiroAPI.add_boxShapeHemi(system, 7, 3/2*H, wall_t, pos, 'textures/white concrete.jpg', [10,10])

    # Add elevator shaft
    for floor in range(3):
        y_pos = H*floor + H/2
        pos = np.array([10.7, y_pos, 12.1])
        MiroAPI.add_boxShapeHemi(system, 2.034, H/2, wall_t, pos, 'textures/elevator.png', [4,3])

    # Add end wall, towards technology
    texture = ['textures/mit_4th.jpg', 'textures/mit_4th.jpg', 'textures/mit_4th.jpg']
    for floor in range(3):
        y_pos = H*floor + H/2
        pos = np.array([10.5+2.8-0.23, y_pos, -17+2.2+2.2])
        MiroAPI.add_boxShapeHemi(system, 1.77, H/2, wall_t, pos, texture[floor], [-4,-3], Collide=False)

    #Add oblique walls
    
    n = np.array([0,1,0])         # Normal vector for rotation
    alpha = -np.arctan(211/1380-0.05)   # Rotation angle for positive x wall

    #Add oblique wall towards umu libary
    pos_1 = np.array([16.3, 3/2*H-wall_t, 0.34+8.16+wall_t])
    dim_1 = np.array([wall_t, H/2, 3.6])
    ang_1 = np.pi*(0.5-0.03)
    sca_1 = [10,10]

    #Add oblique wall towards NA
    pos_2 = np.array([-5.6-wall_t, 3/2*H, 5.3])
    dim_2 = np.array([wall_t, H/2, 0.545])
    ang_2 = -(np.pi/4)

    #Main wall in positive x direction
    pos_3 = np.array([13.775+wall_t, 0, -2.2]) + np.array([0, wall_h, 0])
    ang_3 = alpha
    dim_3 = np.array([wall_t, wall_h, 10.58])

    pos_ob = [pos_1, pos_2, pos_3]
    dim = [dim_1, dim_2, dim_3]
    ang = [ang_1, ang_2, ang_3]
    textures = [texture_wall, 'textures/white concrete.jpg', texture_wall]
    scale = [sca_1, sca_1, sca_1]
    for i in range(len(pos_ob)):
        # Create a box
        MiroAPI.add_boxShapeHemi(system, dim[i][0], dim[i][1], dim[i][2], pos_ob[i], rotY=ang[i], rotDegrees=False, texture=textures[i], scale = scale[i])

def add_fence(system, H, postNum, floor_w, floor_w_2, floor, floor_t, handle_l):

    # Add fence post, as a cylinder
    fence_r =  0.02         # Radius
    fence_h = 1.04          # Hight
    fence_d = 1             # Density
    texture = 'textures/white concrete.jpg'
    fence_corr = np.array([0, fence_h/2, 0]) # Correction for fence post postition

    # Add handle for each floor
    handle_r = 0.0175         # Radius
    # handle_d = 1            # Density
    n_x = np.array([1, 0, 0])     # Normalvector in x direction
    n_z = np.array([0, 0, 1])     # Normalvector in z direction
    # Handle
    pos_rail_1 = np.array([-0.75, H+fence_h*0.925, 6.58-floor_w])         # Fence 3rd floor left of stair
    pos_rail_2 = np.array([10.45+2.11-floor_w_2, H+fence_h*0.925, -4.4])       # Fence 3rd floor
    pos_rail_3 = np.array([10.45+2.11-floor_w_2, 2*H+fence_h*0.925, -4.4])     # Fence 4th floor
    pos_rail_4 = np.array([6.5, 2*H+fence_h*0.925, 4.2])                  # Fence by the stair 4th floor
    # Rail
    pos_rail_5 = np.array([-0.75, H+3/4*fence_h, 6.58-floor_w])           # Fence 3rd floor left of stair
    pos_rail_6 = np.array([10.45+2.11-floor_w_2, H+3/4*fence_h, -4.4])         # Fence 3rd floor
    pos_rail_7 = np.array([10.45+2.11-floor_w_2, 2*H+3/4*fence_h, -4.4])       # Fence 4th floor
    pos_rail_8 = np.array([6.5, 2*H+3/4*fence_h, 4.2])                    # Fence by the stair 4th floor

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
        
        MiroAPI.add_cylinderShape(system, handle_r, length, 1, pos_rail, 'textures/wood_floor.jpg', rotAngle=np.pi/2,rotAxis=n,rotDegrees=False)

    # Support rail
    for num in range(len(pos_r)):
        pos_rail = pos_r[num]
        n = dirr[num]
        length = handle_length[num]

        MiroAPI.add_cylinderShape(system, fence_r, length, 1, pos_rail, 'textures/white concrete.jpg', rotAngle=np.pi/2,rotAxis=n,rotDegrees=False)

    for post in range(postNum):
        y_pos = floor*H - floor_t
        pos_l = np.array([(-0.7-handle_l/2)+post*dl, H-floor_t, 6.58-floor_w]) + fence_corr  # Left side stair  
        pos_r = np.array([10.45+2.11-floor_w_2, y_pos, (-4.4-handle_l/2)+post*dl]) + fence_corr # Right side stair

        MiroAPI.add_cylinderShape(system, fence_r, fence_h, fence_d , pos_r, texture)
        MiroAPI.add_cylinderShape(system, fence_r, fence_h, fence_d , pos_l, texture)

    for post in range(3):
        pos = np.array([6.5, 2*H-floor_t, 3.5+post*dl]) + fence_corr

        MiroAPI.add_cylinderShape(system, fence_r, fence_h, fence_d , pos, texture)

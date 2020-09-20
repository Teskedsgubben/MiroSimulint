import pychrono.core as chrono
import numpy as np
import random

from src import Shapes as shp

def Franz_Components(system, SPEEDMODE = False):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    stage(system)
    screen(system)
    back_stage(system)
    if not SPEEDMODE:
        second_floor(system)
        third_floor(system)
        fourth_floor(system)



def second_floor(system):
    start_table_pos = chrono.ChVectorD(-3.8, 0, -7.6)  # The position for the table in x and z direction
    num_table_z = 2     # Tabels along the z axis 
    num_table_x = 3     # Tabels along the x axis
    #The table size and position in y direction.                              
    size_table_x = 1.2
    size_table_y = 0.1
    size_table_z = 1.2
    size_leg_h = 0.8
    size_leg_r = 0.03
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2) 
    for table_i in range(num_table_z):
        table_pos = start_table_pos + chrono.ChVectorD((random.random() - 0.4)/2, 0, 3*table_i + 6.5)
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(4):
            length_rand = length - random.random()/5
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i)
    
    for table_i in range(num_table_x):
        table_pos = start_table_pos + chrono.ChVectorD(3*table_i + 5.5, 0, random.random()/2)
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(4):
            length_rand = length - random.random()/5
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i)


def third_floor(system):
    start_table_pos = chrono.ChVectorD(9.05,3.32,5.55)
    num_table_x = 2     # Tabels in the x direction
    num_table_z = 2 
    #The table size and position in y direction.                              
    size_table_x = 1
    size_table_y = 0.1
    size_table_z = 1
    size_leg_h = 0.8
    size_leg_r = 0.03
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2)
    # The tables in the x dircetion on thirdfloor
    for table_i in range(num_table_x):
        table_pos = start_table_pos + chrono.ChVectorD(-4*table_i -7, 0, 0)
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(0,4,2):
            length_rand = length - random.random()/5
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i)  
    # the tables in z direction on thirdfloor
    for table_i in range(num_table_z):
        table_pos = start_table_pos + chrono.ChVectorD(0, 0, -4*table_i - 7)
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(1,4,2):
            length_rand = length - random.random()/5 #makes the chairs look more natural because they wont be perfect inline
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i)  

def fourth_floor(system):
    table_pos = chrono.ChVectorD(9.15,6.64,-5.8)
    size_table_x = 1
    size_table_y = 0.1
    size_table_z = 1
    size_leg_h = 0.8
    size_leg_r = 0.03
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2)
    MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
    for chair_i in range(1,4,2):
        length_rand = length - random.random()/5 #makes the chairs look more natural because they wont be perfect inline
        theta = chair_i*0.5*np.pi
        n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
        pos_chair = table_pos + n
        MIT_chair(system, pos_chair,chair_i)  

def MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z,size_leg_h, size_leg_r):    
    size_table = np.array([size_table_x, size_table_y, size_table_z, size_leg_h])
    tabletop(system, table_pos, size_table)
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2) - 2*size_leg_r
    for i in range(4):
        theta = i*0.5*np.pi + np.pi/4
        n = chrono.ChVectorD(length*np.cos(theta), size_leg_h/2, length*np.sin(theta))
        leg_pos = table_pos + n
        table_leg(system,leg_pos, size_leg_r, size_leg_h)



def tabletop(system, table_pos, size_table):

    body_table = chrono.ChBody()
    body_table.SetBodyFixed(True)
    body_table.SetPos(table_pos + chrono.ChVectorD(0,size_table[3],0))
    
    # Collision shape
    body_table.GetCollisionModel().ClearModel()
    body_table.GetCollisionModel().AddBox(size_table[0]/2, size_table[1]/2, size_table[2]/2) # hemi sizes
    body_table.GetCollisionModel().BuildModel()
    body_table.SetCollide(True)
    
    # Visualization shape
    body_table_shape = chrono.ChBoxShape()
    body_table_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_table[0]/2, size_table[1]/2, size_table[2]/2)
    body_table_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_table.GetAssets().push_back(body_table_shape)
    
    body_table_texture = chrono.ChTexture()
    if(size_table[0] < 0.6):
        tex = 'textures/MITstol.jpg'
    else:
        tex = 'textures/MITbord.jpg'
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile(tex))
    body_table_texture.SetTextureScale(4, 3)
    body_table.GetAssets().push_back(body_table_texture)
    
    system.Add(body_table)
    

def table_leg(system,leg_pos, size_leg_r, size_leg_h):

    # creating the cylinder leg
    size_leg_d = 1   
    body_table_leg = chrono.ChBodyEasyCylinder(size_leg_r, size_leg_h, size_leg_d)
    body_table_leg.SetBodyFixed(True)
    body_table_leg.SetPos(leg_pos)
    # Collision shape
    body_table_leg.GetCollisionModel().ClearModel()
    body_table_leg.GetCollisionModel().AddCylinder(size_leg_r, size_leg_r, size_leg_h/2) # hemi sizes
    body_table_leg.GetCollisionModel().BuildModel()
    body_table_leg.SetCollide(True)
    
    # Visualization shape
    body_table_leg_texture = chrono.ChTexture()
    body_table_leg_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/brushsteel.png'))
    body_table_leg_texture.SetTextureScale(1, 1)
    body_table_leg.GetAssets().push_back(body_table_leg_texture)
    
    system.Add(body_table_leg)


def MIT_chair(system, pos_chair,rotation):
    #dimensions of the chair
    size_chair_x = 0.5
    size_chair_y = 0.1
    size_chair_z = 0.5
    size_chair_leg_h = 0.5
    size_leg_r = 0.02 
    size_back_cylinder_r = 0.015 # the back of the chair
    size_back_cylinder_h = 0.5
    size_back_x = size_chair_x/7
    size_back_y = 0.2
    size_back_z = size_chair_z + 0.05 
    MIT_table(system, pos_chair, size_chair_x, size_chair_y, size_chair_z, size_chair_leg_h, size_leg_r) # making the bottom of the chair
    
    if rotation == 0:
        pos_back  = pos_chair + chrono.ChVectorD(-size_chair_x/2.3, size_back_cylinder_h + size_chair_leg_h,0)
    elif rotation == 1:
        pos_back  = pos_chair + chrono.ChVectorD(0, size_back_cylinder_h + size_chair_leg_h,size_chair_z/2.3)
        temp = size_back_x
        size_back_x = size_back_z
        size_back_z = temp
    elif rotation == 2:
        pos_back  = pos_chair + chrono.ChVectorD(size_chair_x/2.3,size_back_cylinder_h + size_chair_leg_h,0)
    else:
        pos_back  = pos_chair + chrono.ChVectorD(0, size_back_cylinder_h + size_chair_leg_h,-size_chair_z/2.3)
        temp = size_back_x
        size_back_x = size_back_z
        size_back_z = temp 
   
    chair_back(system, pos_back, size_back_x,size_back_y, size_back_z)
    length_0 = np.sqrt((size_chair_x/2)**2 + (size_chair_z/2)**2) - 2*size_back_cylinder_r
    theta_0 = rotation*0.5*np.pi - np.pi/4
    
    for i in range(6):
        theta = theta_0 + i*np.pi/10
        length = length_0 - (i*(5-i)*(1-1/np.sqrt(2))*length_0)/6.25 
        n = chrono.ChVectorD(- length*np.cos(theta), size_back_cylinder_h/2 + size_chair_leg_h, length*np.sin(theta))
        pos_back = pos_chair + n
        table_leg(system,pos_back, size_back_cylinder_r, size_back_cylinder_h)

def chair_back(system, pos_back, size_back_x,size_back_y, size_back_z):

    chair_back = chrono.ChBody()
    chair_back.SetBodyFixed(True)
    chair_back.SetPos(pos_back)
    
    # Collision shape
    chair_back.GetCollisionModel().ClearModel()
    chair_back.GetCollisionModel().AddBox(size_back_x/2, size_back_y/2, size_back_z/2) # hemi sizes
    chair_back.GetCollisionModel().BuildModel()
    chair_back.SetCollide(True)
    
    # Visualization shape
    chair_back_shape = chrono.ChBoxShape()
    chair_back_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_back_x/2, size_back_y/2, size_back_z/2)
    chair_back_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    chair_back.GetAssets().push_back(chair_back_shape)
    
    chair_back_texture = chrono.ChTexture()
    chair_back_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITstol.jpg'))
    chair_back.GetAssets().push_back(chair_back_texture)
    
    system.Add(chair_back)

#coner position (-7.5,0,-11)
def stage(system): 
    theta_f = 0 
    theta_b = np.pi/2
    pos_f = chrono.ChVectorD(-4.3, 0, -8.8)
    dir_f = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f)) 
    pos_b = chrono.ChVectorD(-5.3, 0, -7.8)
    dir_b = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))
    step = shp.step(pos_f, dir_f, pos_b, dir_b, 3, 0.3, [0.1,0.1,0.1])
    system.Add(step)


def screen(system):
    corner_pos = chrono.ChVectorD(-5.3,3.55,-8.8)
    size_length = 4
    size_width = 0.01
    size_height = size_length/(4/3)
    
    alpha = np.pi/10
    delta_tilt = chrono.ChVectorD(np.sin(alpha)/np.sqrt(2), np.cos(alpha), np.sin(alpha)/np.sqrt(2))*size_height/2
    screen_pos = corner_pos + chrono.ChVectorD(1/np.sqrt(8),0, 1/np.sqrt(8))*size_length + delta_tilt
    pro_screen = chrono.ChBody()
    pro_screen.SetBodyFixed(True)
    pro_screen.SetPos(screen_pos)

    # Collision shape
    pro_screen.GetCollisionModel().ClearModel()
    pro_screen.GetCollisionModel().AddBox(size_length/2, size_height/2, size_width/2) # hemi sizes
    pro_screen.GetCollisionModel().BuildModel()
    pro_screen.SetCollide(True)
    
    # Visualization shape
    pro_screen_shape = chrono.ChBoxShape()
    pro_screen_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_length/2, size_height/2, size_width/2)
    pro_screen_shape.SetColor(chrono.ChColor(255,255,255))
    pro_screen.GetAssets().push_back(pro_screen_shape)
    
    pro_screen_texture = chrono.ChTexture()
    pro_screen_texture.SetTextureFilename(chrono.GetChronoDataFile('GroupLogo.png'))
    pro_screen_texture.SetTextureScale(-4, -3)
    pro_screen.GetAssets().push_back(pro_screen_texture)

    rot_x = chrono.ChVectorD(1,0,0)
    rot_y = chrono.ChVectorD(0,1,0)
    alpha = np.pi/10
    beta = np.pi/4
    qr_x = chrono.Q_from_AngAxis(alpha, rot_x.GetNormalized())    # Rotate the screen
    qr_y = chrono.Q_from_AngAxis(beta, rot_y.GetNormalized())
    quaternion = qr_y* qr_x * pro_screen.GetRot()
    pro_screen.SetRot(quaternion)

    system.Add(pro_screen)

    # Top cylinder
    r = 0.08
    roller = chrono.ChBodyEasyCylinder(r, 4.15, 1000)
    roller.SetBodyFixed(True)
    roller.SetCollide(False)
    roller.SetPos(screen_pos + delta_tilt*((1.9*r+size_height)/size_height))
    qr = chrono.Q_from_AngAxis(np.pi/2, chrono.ChVectorD(1,0,1).GetNormalized())
    roller.SetRot(qr * roller.GetRot())

    system.Add(roller)

    # Hanging bars
    bar_h = 0.05
    dx = chrono.ChVectorD(0.25, 0, 0)  
    dz = chrono.ChVectorD(0, 0, 0.25)  

    barN = chrono.ChBodyEasyBox(bar_h, bar_h, 1.2, 1000)
    barN.SetBodyFixed(True)
    barN.SetCollide(False)
    roller_mid = screen_pos + delta_tilt*((3.9*r+size_height)/size_height) + chrono.ChVectorD(0,bar_h/2,0)
    offset = chrono.ChVectorD(1,0,-1)
    offset.SetLength(1.8)
    barN.SetPos(roller_mid + offset - dz)

    system.Add(barN)

    barS = barN.Clone()
    barS.SetRot(chrono.Q_from_AngAxis(np.pi/2, chrono.ChVectorD(0,1,0)) * barS.GetRot())
    barS.SetPos(roller_mid - offset - dx)

    system.Add(barS)

def back_stage(system):
    coner_pos = chrono.ChVectorD(-5.3,1.55,-8.8) # Real coner -5.3,1.25,-8.8
    length = 1.8
    in_screen_pos = coner_pos + chrono.ChVectorD(1/np.sqrt(2),0, 1/np.sqrt(2))*length
    in_screen = chrono.ChBody()
    in_screen.SetBodyFixed(True)
    in_screen.SetPos(in_screen_pos)

    size_len = 2.5
    size_width = 0.05
    size_height = 2.5
    # Collision shape
    in_screen.GetCollisionModel().ClearModel()
    in_screen.GetCollisionModel().AddBox((size_len)/2, (size_height)/2, size_width/2) # hemi sizes
    in_screen.GetCollisionModel().BuildModel()
    in_screen.SetCollide(True)
    
    # Visualization shape
    in_screen_shape = chrono.ChBoxShape()
    in_screen_shape.GetBoxGeometry().Size = chrono.ChVectorD((size_len)/2, (size_height)/2, size_width/2)
    in_screen_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    in_screen.GetAssets().push_back(in_screen_shape)
    system.Add(in_screen)
    in_screen_texture = chrono.ChTexture()
    in_screen_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/tf-logo.jpg'))
    in_screen_texture.SetTextureScale(-4, -3)
    in_screen.GetAssets().push_back(in_screen_texture)

    
    rot_y = chrono.ChVectorD(0,1,0)
    alpha = np.pi/4
    qr_y = chrono.Q_from_AngAxis(alpha, rot_y.GetNormalized())
    quaternion = qr_y * in_screen.GetRot() #rotates the inner screen
    in_screen.SetRot(quaternion)
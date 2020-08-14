import pychrono.core as chrono
import os
import numpy as np
import random
def Franz_Components(system):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    second_floor(system)
    third_floor(system)


def second_floor(system):
    start_table_pos = chrono.ChVectorD(10, 0, -9.8)  # The position for the table in x and z direction
    num_table_1 = 5     # Tabels along the z axis 
    num_table_2 = 6     # Tabels along the x axis
    #The table size and position in y direction.                              
    size_table_x = 1.2
    size_table_y = 0.1
    size_table_z = 1.2
    size_leg_h = 0.8
    size_leg_r = 0.03
    level_pos = [0, 4, 8] # the of the floor in the y direction.
    level = 0   #what floor? 0 = second floor and so on.
    start_table_pos.y = level_pos[level] + size_leg_h #makes sure the legs of the tale touches the ground
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2) 

    for table_i in range(num_table_1):
        table_pos = start_table_pos + chrono.ChVectorD((random.random() - 0.7)/2, 0, 3)*table_i
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(4):
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length*np.cos(theta), 0, length*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i, level)
    
    for table_i in range(1,num_table_2):
        table_pos = start_table_pos + chrono.ChVectorD(-3, 0, random.random()/2)*table_i
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(4):
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length*np.cos(theta), 0, length*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i, level)

# 3. 4. 8
def third_floor(system):
    start_table_pos = chrono.ChVectorD(9.55,4,6.55)
    num_table_x = 4     # Tabels in the x direction 
    #The table size and position in y direction.                              
    size_table_x = 1
    size_table_y = 0.1
    size_table_z = 1
    size_leg_h = 0.8
    size_leg_r = 0.03
    level_pos = [0, 4, 8] # the y coordinate of the floors.
    level = 1   #what floor? 0 = second floor and so on.
    start_table_pos.y = level_pos[level] + size_leg_h #makes sure the legs of the tale touches the ground
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2)
    # The tables in the x dircetion on thirdfloor
    for table_i in range(num_table_x):
        table_pos = start_table_pos + chrono.ChVectorD(-3, 0, 0)*(table_i + 2)
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(0,4,2):
            length_rand = length - random.random()/2
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i, level)  
    # the tables in z direction on thirdfloor
    for table_i in range(num_table_x):
        table_pos = start_table_pos + chrono.ChVectorD(0, 0, -3)*(table_i + 2)
        MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(1,4,2):
            length_rand = length - random.random()/2 #makes the chairs look more natural because they wont be perfect inline
            theta = chair_i*0.5*np.pi
            n = chrono.ChVectorD(-length_rand*np.cos(theta), 0, length_rand*np.sin(theta))
            pos_chair = table_pos + n
            MIT_chair(system, pos_chair,chair_i, level)  



def MIT_table(system, table_pos, size_table_x, size_table_y, size_table_z,size_leg_h, size_leg_r):    
    size_table = np.array([size_table_x, size_table_y, size_table_z])
    tabletop(system, table_pos, size_table)
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2) - 2*size_leg_r
    for i in range(4):
        theta = i*0.5*np.pi + np.pi/4
        n = chrono.ChVectorD(length*np.cos(theta), -size_leg_h/2, length*np.sin(theta))
        leg_pos = table_pos + n
        table_leg(system,leg_pos, size_leg_r, size_leg_h)



def tabletop(system, table_pos, size_table):

    body_table = chrono.ChBody()
    body_table.SetBodyFixed(True)
    body_table.SetPos(table_pos)
    
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
    body_table_leg.GetCollisionModel().AddCylinder(size_leg_r, size_leg_h, size_leg_d) # hemi sizes
    body_table_leg.GetCollisionModel().BuildModel()
    body_table_leg.SetCollide(True)
    
    # Visualization shape
    body_table_leg_texture = chrono.ChTexture()
    body_table_leg_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/brushsteel.jpg'))
    body_table_leg.GetAssets().push_back(body_table_leg_texture)
    
    system.Add(body_table_leg)


def MIT_chair(system, pos_chair,rotation, level):
    #dimensions of the chair
    size_chair_x = 0.5
    size_chair_y = 0.1
    size_chair_z = 0.5
    size_chair_leg_h = 0.5
    size_leg_r = 0.02 
    size_back_cylinder_r = 0.015 # the back of the chair
    size_back_cylinder_h = 0.5
    level_pos = [0, 4, 8] # the of the floor in the y direction.
    pos_chair.y = level_pos[level] + size_chair_leg_h #makes sure the chair stands on second floor
    size_back_x = size_chair_x/7
    size_back_y = 0.2
    size_back_z = size_chair_z + 0.05 
    MIT_table(system, pos_chair, size_chair_x, size_chair_y, size_chair_z, size_chair_leg_h, size_leg_r) # making the bottom of the chair
    
    if rotation == 0:
        pos_back  = pos_chair + chrono.ChVectorD(-size_chair_x/2.3, size_back_cylinder_h,0)
    elif rotation == 1:
        pos_back  = pos_chair + chrono.ChVectorD(0, size_back_cylinder_h,size_chair_z/2.3)
        temp = size_back_x
        size_back_x = size_back_z
        size_back_z = temp
    elif rotation == 2:
        pos_back  = pos_chair + chrono.ChVectorD(size_chair_x/2.3, size_back_cylinder_h,0)
    else:
        pos_back  = pos_chair + chrono.ChVectorD(0, size_back_cylinder_h,-size_chair_z/2.3)
        temp = size_back_x
        size_back_x = size_back_z
        size_back_z = temp


    
    chair_back(system, pos_back, size_back_x,size_back_y, size_back_z)

    length_0 = np.sqrt((size_chair_x/2)**2 + (size_chair_z/2)**2) - 2*size_back_cylinder_r
    theta_0 = rotation*0.5*np.pi - np.pi/4
    
    for i in range(6):
        theta = theta_0 + i*np.pi/10
        length = length_0 - (i*(5-i)*(1-1/np.sqrt(2))*length_0)/6.25 
        n = chrono.ChVectorD(- length*np.cos(theta), size_back_cylinder_h/2, length*np.sin(theta))
        pos_back = pos_chair + n
        table_leg(system,pos_back, size_back_cylinder_r, size_back_cylinder_h)
    
    
  #  for i in range(6):
   #     pos_back = pos_chair + chrono.ChVectorD(-size_chair_x/2 + 0.01,size_back_cylinder_h/2 , -size_chair_z/2.2 + i*size_chair_z/5.5)
    #    table_leg(system,pos_back, size_back_cylinder_r, size_back_cylinder_h)


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
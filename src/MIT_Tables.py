from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np
import random

def build(ChSystem, SPEEDMODE = False):
    if not SPEEDMODE:
        second_floor(ChSystem)
        third_floor(ChSystem)
        fourth_floor(ChSystem)

def second_floor(MiroSystem):
    start_table_pos = np.array([-3.8, 0, -7.6])  # The position for the table in x and z direction
    num_table_z = 0     # Tabels along the z axis 
    num_table_x = 3     # Tabels along the x axis
    #The table size and position in y direction.                              
    size_table_x = 1.2
    size_table_y = 0.1
    size_table_z = 1.2
    size_leg_h = 0.8
    size_leg_r = 0.03
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2) 
    for table_i in range(num_table_z):
        table_pos = start_table_pos + np.array([(random.random() - 0.4)/2, 0, 3*table_i + 6.5])
        MIT_table(MiroSystem, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(4):
            length_rand = length - random.random()/5
            theta = chair_i*0.5*np.pi
            n = np.array([-length_rand*np.cos(theta), 0, length_rand*np.sin(theta)])
            pos_chair = table_pos + n
            MIT_chair(MiroSystem, pos_chair,chair_i)
    
    for table_i in range(num_table_x):
        table_pos = start_table_pos + np.array([3*table_i + 5.5, 0, random.random()/2])
        MIT_table(MiroSystem, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(4):
            length_rand = length - random.random()/5
            theta = chair_i*0.5*np.pi
            n = np.array([-length_rand*np.cos(theta), 0, length_rand*np.sin(theta)])
            pos_chair = table_pos + n
            MIT_chair(MiroSystem, pos_chair,chair_i)


def third_floor(MiroSystem):
    start_table_pos = np.array([9.05,3.32,5.55])
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
        table_pos = start_table_pos + np.array([-4*table_i -7, 0, 0])
        MIT_table(MiroSystem, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(0,4,2):
            length_rand = length - random.random()/5
            theta = chair_i*0.5*np.pi
            n = np.array([-length_rand*np.cos(theta), 0, length_rand*np.sin(theta)])
            pos_chair = table_pos + n
            MIT_chair(MiroSystem, pos_chair,chair_i)  
    # the tables in z direction on thirdfloor
    for table_i in range(num_table_z):
        table_pos = start_table_pos + np.array([0, 0, -4*table_i - 7])
        MIT_table(MiroSystem, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(1,4,2):
            length_rand = length - random.random()/5 #makes the chairs look more natural because they wont be perfect inline
            theta = chair_i*0.5*np.pi
            n = np.array([-length_rand*np.cos(theta), 0, length_rand*np.sin(theta)])
            pos_chair = table_pos + n
            MIT_chair(MiroSystem, pos_chair,chair_i)  

def fourth_floor(MiroSystem):
    for table_pos in [np.array([9.15,6.64,-5.8]), np.array([10.15,6.64,-5.8]), np.array([9.2,6.64,1.7])]:
        size_table_x = 1
        size_table_y = 0.1
        size_table_z = 1
        size_leg_h = 0.8
        size_leg_r = 0.03
        length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2)
        MIT_table(MiroSystem, table_pos, size_table_x, size_table_y, size_table_z, size_leg_h, size_leg_r)   # The table
        for chair_i in range(1,4,2):
            length_rand = length - random.random()/5 #makes the chairs look more natural because they wont be perfect inline
            theta = chair_i*0.5*np.pi
            n = np.array([-length_rand*np.cos(theta), 0, length_rand*np.sin(theta)])
            pos_chair = table_pos + n
            MIT_chair(MiroSystem, pos_chair,chair_i)  

def MIT_table(MiroSystem, table_pos, size_table_x, size_table_y, size_table_z,size_leg_h, size_leg_r):    
    size_table = np.array([size_table_x, size_table_y, size_table_z, size_leg_h])
    tabletop(MiroSystem, table_pos, size_table)
    length = np.sqrt((size_table_x/2)**2 + (size_table_z/2)**2) - 2*size_leg_r
    for i in range(4):
        theta = i*0.5*np.pi + np.pi/4
        n = np.array([length*np.cos(theta), size_leg_h/2, length*np.sin(theta)])
        leg_pos = table_pos + n
        table_leg(MiroSystem,leg_pos, size_leg_r, size_leg_h)



def tabletop(MiroSystem, table_pos, size_table):
    if(size_table[0] < 0.6):
        tex = 'textures/MITstol.jpg'
    else:
        tex = 'textures/MITbord.jpg'

    MiroAPI.add_boxShape(MiroSystem, size_table[0], size_table[1], size_table[2], table_pos + np.array([0,size_table[3],0]), tex)
    

def table_leg(MiroSystem, leg_pos, size_leg_r, size_leg_h):
    # creating the cylinder leg
    MiroAPI.add_cylinderShape(MiroSystem, size_leg_r, size_leg_h, 1200, leg_pos, texture='brushsteel.png')

def MIT_chair(MiroSystem, pos_chair,rotation):
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
    MIT_table(MiroSystem, pos_chair, size_chair_x, size_chair_y, size_chair_z, size_chair_leg_h, size_leg_r) # making the bottom of the chair
    
    if rotation == 0:
        pos_back  = pos_chair + np.array([-size_chair_x/2.3, size_back_cylinder_h + size_chair_leg_h,0])
    elif rotation == 1:
        pos_back  = pos_chair + np.array([0, size_back_cylinder_h + size_chair_leg_h,size_chair_z/2.3])
        temp = size_back_x
        size_back_x = size_back_z
        size_back_z = temp
    elif rotation == 2:
        pos_back  = pos_chair + np.array([size_chair_x/2.3,size_back_cylinder_h + size_chair_leg_h,0])
    else:
        pos_back  = pos_chair + np.array([0, size_back_cylinder_h + size_chair_leg_h,-size_chair_z/2.3])
        temp = size_back_x
        size_back_x = size_back_z
        size_back_z = temp 
   
    chair_back(MiroSystem, pos_back, size_back_x,size_back_y, size_back_z)
    length_0 = np.sqrt((size_chair_x/2)**2 + (size_chair_z/2)**2) - 2*size_back_cylinder_r
    theta_0 = rotation*0.5*np.pi - np.pi/4
    
    for i in range(6):
        theta = theta_0 + i*np.pi/10
        length = length_0 - (i*(5-i)*(1-1/np.sqrt(2))*length_0)/6.25 
        n = np.array([- length*np.cos(theta), size_back_cylinder_h/2 + size_chair_leg_h, length*np.sin(theta)])
        pos_back = pos_chair + n
        table_leg(MiroSystem,pos_back, size_back_cylinder_r, size_back_cylinder_h)

def chair_back(MiroSystem, pos_back, size_back_x,size_back_y, size_back_z):
    MiroAPI.add_boxShape(MiroSystem, size_back_x, size_back_y, size_back_z, pos_back, 'MITstol.jpg')

import pychrono.core as chrono
import os
import numpy as np
def Franz_Components(system):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    start_table_pos = chrono.ChVectorD(8, -0.3, -5)  # The position for the table
    num_table = 7
    for table in range(num_table):
        table_pos = start_table_pos + chrono.ChVectorD(0, 0, 1.5)*table
        MIT_table(system, table_pos)               # The table

def MIT_table(system, table_pos):    
    size_table_x = 0.7
    size_table_y = 0.1
    size_table_z = 0.7
    size_table = np.array([size_table_x, size_table_y, size_table_z])
    tabletop(system, table_pos, size_table)
    size_leg_r = 0.05
    size_leg_h = 0.7
    length = np.sqrt((size_table_x/2)**2 + (size_table_y/2)**2)
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
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/BHgang.jpg'))
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
    body_table_leg.SetCollide(False)
    
    # Visualization shape
    
    #body_table_leg_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    #body_table_leg.GetAssets().push_back(body_table_leg_shape)
    
    body_table_leg_texture = chrono.ChTexture()
    body_table_leg_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/BHgang.jpg'))
    body_table_leg.GetAssets().push_back(body_table_leg_texture)
    
    system.Add(body_table_leg)

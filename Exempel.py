import numpy as np

def Johan_Components(system):
    center = chrono.ChVectorD(1.2, 0, 0 )
    MIT_trappa(system, center)


def MIT_trappa(system, center):
    #cylinder här, radie = r
    r = 1
    for i in range(5):
        h = i*dh
        theta = i*2*pi*(1/20)
        MIT_trappsteg(system, center, r, h, theta)
    #räcke


def MIT_trappsteg(system, center, r, h, theta):
    # Create the table, as a box
    
    size_table_x = 1
    size_table_y = 0.2
    size_table_z = 1
    
    body_table = chrono.ChBody()
    body_table.SetBodyFixed(True)
    n = chrono.ChVectorD(np.cos(theta), 0, np.sin(theta))
    start = center + 2*r*n
    body_table.SetPos(start)
    
    # Collision shape
    body_table.GetCollisionModel().ClearModel()
    body_table.GetCollisionModel().AddBox(size_table_x/2, size_table_y/2, size_table_z/2) # hemi sizes
    body_table.GetCollisionModel().BuildModel()
    body_table.SetCollide(True)
    
    # Visualization shape
    body_table_shape = chrono.ChBoxShape()
    body_table_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_table_x/2, size_table_y/2, size_table_z/2)
    body_table_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_table.GetAssets().push_back(body_table_shape)
    
    body_table_texture = chrono.ChTexture()
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/tf-logo.jpg'))
    body_table.GetAssets().push_back(body_table_texture)
    
    system.Add(body_table)
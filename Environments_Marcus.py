import pychrono.core as chrono
import os

def Marcus_Components(system):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")
    
    # Create the shaking table, as a box
    
    size_table_x = 1
    size_table_y = 0.2
    size_table_z = 1
    
    body_table = chrono.ChBody()
    body_table.SetBodyFixed(True)
    body_table.SetPos(chrono.ChVectorD(-1.2, -2*size_table_y, 0 ))
    
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
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/bhgang.jpg'))
    body_table.GetAssets().push_back(body_table_texture)
    
    system.Add(body_table)
    
   
import pychrono.core as chrono
import numpy as np


def add_boxShapex2(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale = [4,3], hitbox = True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotDegrees=True, Fixed=True):
    add_boxShape(MiroSystem, 2*size_x, 2*size_y, 2*size_z, pos, texture, scale, hitbox, rotX, rotY, rotZ, rotOrder, rotDegrees, Fixed)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale = [4,3], hitbox = True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotDegrees=True, Fixed=True):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''

    ChPos = chrono.ChVectorD(pos[0], pos[1], pos[2])

    # Create a box
    body_box = chrono.ChBody()
    body_box.SetBodyFixed(Fixed)
    body_box.SetPos(ChPos)

    # Collision shape
    body_box.GetCollisionModel().ClearModel()
    body_box.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # hemi sizes
    body_box.GetCollisionModel().BuildModel()
    body_box.SetCollide(hitbox)
    
    # Visualization shape
    if(hitbox):
        body_box_shape = chrono.ChBoxShape()
        body_box_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
        body_box_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
        body_box.GetAssets().push_back(body_box_shape)
    
    body_box_texture = chrono.ChTexture()
    body_box_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
    body_box_texture.SetTextureScale(scale[0], scale[1])
    body_box.GetAssets().push_back(body_box_texture)
    
    MiroSystem.Add(body_box)
import pychrono.core as chrono
import numpy as np

def ChVecify(vec):
    if type(vec) == type([]):
        ChVec = chrono.ChVectorD(vec[0], vec[1], vec[2])
    elif type(vec) == type(np.array([])):
        ChVec = chrono.ChVectorD(vec[0], vec[1], vec[2])
    else:
        ChVec = chrono.ChVectorD(vec)
    return ChVec


def add_boxShapeHemi(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotDegrees=True):
    add_boxShape(MiroSystem, 2*size_x, 2*size_y, 2*size_z, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotDegrees)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale = [4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotDegrees=True):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    
    # Convert rotation to radians
    if(rotDegrees):
        rotX = np.deg2rad(rotX)
        rotY = np.deg2rad(rotY)
        rotZ = np.deg2rad(rotZ)

    # Filter 'textures/' out of the texture name, it's added later
    if len(texture) > len('textures/'):
        if texture[0:len('textures/')] == 'textures/':
            texture = texture[len('textures/'):]

    # Create a box
    body_box = chrono.ChBody()
    body_box.SetBodyFixed(Fixed)
    body_box.SetPos(ChPos)

    # Collision shape
    body_box.GetCollisionModel().ClearModel()
    body_box.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # hemi sizes
    body_box.GetCollisionModel().BuildModel()
    body_box.SetCollide(Collide)
    
    # Visualization shape
    if(Collide):
        body_box_shape = chrono.ChBoxShape()
        body_box_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
        body_box_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
        body_box.GetAssets().push_back(body_box_shape)
    
    body_box_texture = chrono.ChTexture()
    body_box_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
    body_box_texture.SetTextureScale(scale[0], scale[1])
    body_box.GetAssets().push_back(body_box_texture)
    
    MiroSystem.Add(body_box)

def add_cylinderShape(system, radius, height, density, pos, texture='test.jpg', scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotDegrees=True):
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    
    # Convert rotation to radians
    if(rotDegrees):
        rotX = np.deg2rad(rotX)
        rotY = np.deg2rad(rotY)
        rotZ = np.deg2rad(rotZ)

    # Filter 'textures/' out of the texture name, it's added later
    if len(texture) > len('textures/'):
        if texture[0:len('textures/')] == 'textures/':
            texture = texture[len('textures/'):]
    
    # Create a cylinder
    body_cylinder = chrono.ChBodyEasyCylinder(radius, height, density)
    body_cylinder.SetBodyFixed(Fixed)
    body_cylinder.SetPos(ChPos)

    # Collision shape
    body_cylinder.GetCollisionModel().ClearModel()
    body_cylinder.GetCollisionModel().AddCylinder(radius, radius, height/2) # hemi sizes
    body_cylinder.GetCollisionModel().BuildModel()
    body_cylinder.SetCollide(Collide)

    # Body texture
    body_cylinder_texture = chrono.ChTexture()
    body_cylinder_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
    body_cylinder_texture.SetTextureScale(scale[0], scale[1])
    body_cylinder.GetAssets().push_back(body_cylinder_texture)

    system.Add(body_cylinder)
import pychrono.core as chrono
import numpy as np

def ChVecify(vec):
    if type(vec) == type([]):
        ChVec = chrono.ChVectorD(float(vec[0]), float(vec[1]), float(vec[2]))
    elif type(vec) == type(np.array([])):
        ChVec = chrono.ChVectorD(float(vec[0]), float(vec[1]), float(vec[2]))
    else:
        ChVec = chrono.ChVectorD(vec)
    return ChVec

def rotateBody(body, rotX, rotY, rotZ, rotOrder, rotAngle, ChRotAxis, rotDegrees=True):
    if(rotDegrees):
        rotX = np.deg2rad(rotX)
        rotY = np.deg2rad(rotY)
        rotZ = np.deg2rad(rotZ)
        rotAngle = np.deg2rad(rotAngle)
    
    if rotAngle:
        q = chrono.ChQuaternionD()
        q.Q_from_AngAxis(rotAngle, ChRotAxis.GetNormalized())
        body.SetRot(q*body.GetRot())

    for dim in rotOrder:
        angle = (dim == 'x')*rotX + (dim == 'y')*rotY + (dim == 'z')*rotZ
        if angle:
            axis = chrono.ChVectorD((dim == 'x')*1, (dim == 'y')*1, (dim == 'z')*1)
            q = chrono.ChQuaternionD()
            q.Q_from_AngAxis(angle, axis)
            body.SetRot(q*body.GetRot())


def add_boxShapeHemi(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    add_boxShape(MiroSystem, 2*size_x, 2*size_y, 2*size_z, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    ChRotAxis = ChVecify(rotAxis)
    
    # Filter 'textures/' out of the texture name, it's added later
    if len(texture) > len('textures/'):
        if texture[0:len('textures/')] == 'textures/':
            texture = texture[len('textures/'):]

    # Create a box
    body_box = chrono.ChBody()
    body_box.SetBodyFixed(Fixed)
    body_box.SetPos(ChPos)

    rotateBody(body_box, rotX, rotY, rotZ, rotOrder, rotAngle, ChRotAxis, rotDegrees)

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
    
    print('textures/'+texture)
    body_box_texture = chrono.ChTexture()
    body_box_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
    body_box_texture.SetTextureScale(scale[0], scale[1])
    body_box.GetAssets().push_back(body_box_texture)
    
    MiroSystem.Add(body_box)

def add_cylinderShape(system, radius, height, density, pos, texture='test.jpg', scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    ChRotAxis = ChVecify(rotAxis)

    # Filter 'textures/' out of the texture name, it's added later
    if len(texture) > len('textures/'):
        if texture[0:len('textures/')] == 'textures/':
            texture = texture[len('textures/'):]
    
    # Create a cylinder
    body_cylinder = chrono.ChBodyEasyCylinder(radius, height, density)
    body_cylinder.SetBodyFixed(Fixed)
    body_cylinder.SetPos(ChPos)

    rotateBody(body_cylinder, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

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

################# TRAPPSTEG ###############
# position_front:  chrono.ChVectorD, the position of the inner lower front corner
# direction_front: chrono.ChVectorD, normal direction to staircase center that aligns with front of the step
# position_back:   chrono.ChVectorD, the position of the inner lower front corner
# direction_back:  chrono.ChVectorD, normal direction that aligns with back of the step
# width:  double, Width of the step as seen when walking in the staircase
# height: double, Thickness of the step
def stepShape(position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    position_front = ChVecify(position_front)
    direction_front = ChVecify(direction_front)
    position_back = ChVecify(position_back)
    direction_back = ChVecify(direction_back)
  
    direction_front.SetLength(width)
    direction_back.SetLength(width)

    # Notation: I = Inner/O = Outer, U = Upper/L = Lower, F = Front/B = Back
    # Ex: Step_ILF is the Inner Lower Front corner of the step
    Step_ILF = position_front
    Step_IUF = position_front + chrono.ChVectorD(0, height, 0)
    Step_ILB = position_back
    Step_IUB = position_back  + chrono.ChVectorD(0, height, 0)

    Step_OLF = position_front + direction_front
    Step_OUF = position_front + direction_front + chrono.ChVectorD(0, height, 0)
    Step_OLB = position_back  + direction_back  
    Step_OUB = position_back  + direction_back + chrono.ChVectorD(0, height, 0)

    Step_mesh = chrono.ChTriangleMeshConnected()

    # inner side
    Step_mesh.addTriangle(Step_ILF, Step_ILB, Step_IUF)
    Step_mesh.addTriangle(Step_IUB, Step_IUF, Step_ILB)

    # outer side
    Step_mesh.addTriangle(Step_OLF, Step_OUB, Step_OLB)
    Step_mesh.addTriangle(Step_OLF, Step_OUF, Step_OUB)

    # top side
    Step_mesh.addTriangle(Step_IUF, Step_OUB, Step_OUF)
    Step_mesh.addTriangle(Step_IUF, Step_IUB, Step_OUB)

    # bottom side
    Step_mesh.addTriangle(Step_ILF, Step_OLF, Step_OLB)
    Step_mesh.addTriangle(Step_ILF, Step_OLB, Step_ILB)

    # back side
    Step_mesh.addTriangle(Step_ILB, Step_OLB, Step_IUB)
    Step_mesh.addTriangle(Step_OUB, Step_IUB, Step_OLB)

    # front side
    Step_mesh.addTriangle(Step_ILF, Step_IUF, Step_OLF)
    Step_mesh.addTriangle(Step_OUF, Step_OLF, Step_IUF)

    Step_mesh.RepairDuplicateVertexes()

    Step = chrono.ChBody()
    Step.SetBodyFixed(True)

    Step_shape = chrono.ChTriangleMeshShape()
    Step_shape.SetMesh(Step_mesh)
    Step_shape.SetColor(chrono.ChColor(clr[0], clr[1], clr[2]))


    Step.GetCollisionModel().ClearModel()	
    Step.GetCollisionModel().AddTriangleMesh(Step_mesh, True, False)
    Step.GetCollisionModel().BuildModel()
    Step.SetCollide(True)
        
    # Step_texture = chrono.ChTexture()
    # Step_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/red_dot.png'))
    # Step_texture.SetTextureScale(10, 10)
    # Step.GetAssets().push_back(Step_texture)
        

    Step.GetAssets().push_back(Step_shape)

    return Step
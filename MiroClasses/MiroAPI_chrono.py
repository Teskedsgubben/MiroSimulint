import sys
try:
    import pychrono.core as chrono
    import pychrono.irrlicht as chronoirr
except:
    import sys
    sys.exit('PyChrono could not be imported. Check that the correct Pyhton interpreter is selected and that the MiroSim conda environment is activated. View guidelines for details.')
import numpy as np
import os
import time

API = 'PyChrono'

def ChVecify(vec):
    if type(vec) == type([]):
        ChVec = chrono.ChVectorD(float(vec[0]), float(vec[1]), float(vec[2]))
    elif type(vec) == type(np.array([])):
        ChVec = chrono.ChVectorD(float(vec[0]), float(vec[1]), float(vec[2]))
    else:
        ChVec = chrono.ChVectorD(vec)
    return ChVec

def rotateVector(vec, rotAngle=0, rotAxis=[0,1,0], rotDegrees=True):
    if(rotDegrees):
        rotAngle = np.deg2rad(rotAngle)
    ChRotAxis = ChVecify(rotAxis).GetNormalized()
    q = chrono.ChQuaternionD()
    q.Q_from_AngAxis(rotAngle, ChRotAxis)
    rotvec = q.Rotate(ChVecify(vec))
    rotvec = [rotvec.x, rotvec.y, rotvec.z]
    return np.array(rotvec)
    

def rotateBody(body, rotX=0, rotY=0, rotZ=0, rotOrder=['x', 'y', 'z'], rotAngle=0, rotAxis=[0,1,0], rotDegrees=True):
    ChRotAxis = ChVecify(rotAxis)
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


# First function to be called
def PreSetup(args, SetupFunction):
    chrono.SetChronoDataPath(os.getcwd() + "/")
    SetupFunction()

# System setup
def SetupSystem():
    ChSystem = chrono.ChSystemNSC()
    ChSimulation = chronoirr.ChIrrApp(ChSystem, 'MiroSimulation', chronoirr.dimension2du(1720, 920))
    # Set the default outward/inward shape margins for collision detection,
    # this is epecially important for very large or very small objects.
    chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.0000001)
    chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.0001)
    
    # Maybe you want to change some settings for the solver. For example you
    # might want to use SetSolverMaxIterations to set the number of iterations
    # per timestep, etc.
    
    #MiroSystem.ChSystem.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
    ChSystem.SetSolverMaxIterations(70)
    return [ChSystem, ChSimulation]

# Shapes
def add_boxShapeHemi(MiroSystem, hemi_size_x, hemi_size_y, hemi_size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5]):
    add_boxShape(MiroSystem, 2*hemi_size_x, 2*hemi_size_y, 2*hemi_size_z, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5]):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    ChRotAxis = ChVecify(rotAxis)
    
    # Create a box
    body_box = chrono.ChBody()
    body_box.SetBodyFixed(Fixed)
    body_box.SetPos(ChPos)

    if not mass:
        mass = density * size_x * size_y * size_z

    inertia_brick_xx = (size_y**2 + size_z**2)*mass/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass/3
    
    body_box.SetMass(mass)
    body_box.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))     

    # Collision shape
    body_box.GetCollisionModel().ClearModel()
    body_box.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # hemi sizes
    body_box.GetCollisionModel().BuildModel()
    body_box.SetCollide(Collide)
    
    # Visualization shape
    body_box_shape = chrono.ChBoxShape()
    body_box_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    body_box_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_box.GetAssets().push_back(body_box_shape)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        body_box_texture = chrono.ChTexture()
        body_box_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
        body_box_texture.SetTextureScale(scale[0], scale[1])
        body_box.GetAssets().push_back(body_box_texture)
    
    rotateBody(body_box, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)
    
    if MiroSystem:
        ChSystem = MiroSystem.Get_APIsystem()[0]
        ChSystem.Add(body_box)
    
    return body_box

def add_cylinderShape(MiroSystem, radius, height, density, pos, texture='test.jpg', scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    ChRotAxis = ChVecify(rotAxis)

    # Create a cylinder
    body_cylinder = chrono.ChBodyEasyCylinder(radius, height, density)
    body_cylinder.SetBodyFixed(Fixed)
    body_cylinder.SetPos(ChPos)

    rotateBody(body_cylinder, rotX, rotY, rotZ, rotOrder, rotAngle, ChRotAxis, rotDegrees)

    # Collision shape
    if(Collide):
        body_cylinder.GetCollisionModel().ClearModel()
        body_cylinder.GetCollisionModel().AddCylinder(radius, radius, height/2) # hemi sizes
        body_cylinder.GetCollisionModel().BuildModel()
    body_cylinder.SetCollide(Collide) 

    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        body_cylinder_texture = chrono.ChTexture()
        body_cylinder_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
        body_cylinder_texture.SetTextureScale(scale[0], scale[1])
        body_cylinder.GetAssets().push_back(body_cylinder_texture)
    
    if MiroSystem:
        ChSystem = MiroSystem.Get_APIsystem()[0]
        ChSystem.Add(body_cylinder)

    return body_cylinder

def add_sphereShape(MiroSystem, radius, pos, texture='test.jpg', density=1000, scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    ChRotAxis = ChVecify(rotAxis)

    # Create a cylinder
    body_ball = chrono.ChBodyEasySphere(radius, density)
    body_ball.SetBodyFixed(Fixed)
    body_ball.SetPos(ChPos)

    rotateBody(body_ball, rotX, rotY, rotZ, rotOrder, rotAngle, ChRotAxis, rotDegrees)

    # Collision shape
    if(Collide):
        body_ball.GetCollisionModel().ClearModel()
        body_ball.GetCollisionModel().AddSphere(radius) # hemi sizes
        body_ball.GetCollisionModel().BuildModel()
    body_ball.SetCollide(Collide) 

    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        body_texture = chrono.ChTexture()
        body_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
        body_texture.SetTextureScale(scale[0], scale[1])
        body_ball.GetAssets().push_back(body_texture)
    
    if MiroSystem:
        ChSystem = MiroSystem.Get_APIsystem()[0]
        ChSystem.Add(body_ball)

    return body_ball

def add_ellisoidShape(MiroSystem, radius_x, radius_y, radius_z, pos, texture='test.jpg', density=1000, scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    # Convert position to chrono vector, supports using chvector as input as well
    ChPos = ChVecify(pos)
    ChRotAxis = ChVecify(rotAxis)

    # Create a cylinder
    body_ball = chrono.ChBodyEasyEllipsoid(chrono.ChVectorD(radius_x, radius_y, radius_z), density)
    body_ball.SetBodyFixed(Fixed)
    body_ball.SetPos(ChPos)

    rotateBody(body_ball, rotX, rotY, rotZ, rotOrder, rotAngle, ChRotAxis, rotDegrees)

    # Collision shape
    if(Collide):
        body_ball.GetCollisionModel().ClearModel()
        body_ball.GetCollisionModel().AddEllipsoid(radius_x, radius_y, radius_z) # hemi sizes
        body_ball.GetCollisionModel().BuildModel()
    body_ball.SetCollide(Collide) 

    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        body_texture = chrono.ChTexture()
        body_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+texture))
        body_texture.SetTextureScale(scale[0], scale[1])
        body_ball.GetAssets().push_back(body_texture)
    
    if MiroSystem:
        ChSystem = MiroSystem.Get_APIsystem()[0]
        ChSystem.Add(body_ball)

    return body_ball

def add_stepShape(MiroSystem, position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    Step = stepShape(position_front, direction_front, position_back, direction_back, width, height, clr)
    if MiroSystem:
        ChSystem = MiroSystem.Get_APIsystem()[0]
        ChSystem.Add(Step)
    return Step

def stepShape(position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    ################# TRAPPSTEG ###############
    # position_front:  chrono.ChVectorD, the position of the inner lower front corner
    # direction_front: chrono.ChVectorD, normal direction to staircase center that aligns with front of the step
    # position_back:   chrono.ChVectorD, the position of the inner lower front corner
    # direction_back:  chrono.ChVectorD, normal direction that aligns with back of the step
    # width:  double, Width of the step as seen when walking in the staircase
    # height: double, Thickness of the stepposition_front = ChVecify(position_front)
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

# Import from file
def LoadFromObj(filename, density=1000, color=[1,0.1,0.1]):
    body = chrono.ChBodyEasyMesh(filename, density, True, True)
    body.AddAsset(chrono.ChColorAsset(chrono.ChColor(color[0], color[1], color[2])))
    return body

# Rigid body operations
def GetMass(body):
    return body.GetMass()

def GetBodyPosition(body):
    ChPos = body.GetPos()
    npPos = np.array([ChPos.x, ChPos.y, ChPos.z])
    return npPos

def GetBodyVelocity(body):
    ChVel = body.GetPos_dt()
    npVel = np.array([ChVel.x, ChVel.y, ChVel.z])
    return npVel
    
def GetBodyAcceleration(body):
    ChAcc = body.GetPos_dtdt()
    npAcc = np.array([ChAcc.x, ChAcc.y, ChAcc.z])
    return npAcc

def MoveBodyBy(body, delta_pos):
    ChPos = ChVecify(delta_pos)
    body.Move(ChPos)

def MoveBodyTo(body, position):
    ChPos = ChVecify(position) - body.GetPos()
    body.Move(ChPos)

def SetBodyFixed(body, Fixed=True):
    body.SetBodyFixed(Fixed)

def SetBodyVelocity(body, velocity):
    vel = ChVecify(velocity)
    body.SetPos_dt(vel)

def SetCollisionModel_Box(body, dimensions, mass, offset):
    dr = ChVecify(offset)
    dim = ChVecify(dimensions)
    inertia_brick_xx = (dim.y**2 + dim.z**2)*mass/3
    inertia_brick_yy = (dim.x**2 + dim.z**2)*mass/3
    inertia_brick_zz = (dim.x**2 + dim.y**2)*mass/3
    body.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))   
    body.GetCollisionModel().ClearModel()
    body.GetCollisionModel().AddBox(dim.x/2, dim.y/2, dim.z/2, dr)
    body.GetCollisionModel().BuildModel()

def SetCollisionModel_Ellipsoid(body, dimensions, mass, offset):
    dr = ChVecify(offset)
    dim = ChVecify(dimensions)   
    inertia_brick_xx = (dim.y**2 + dim.z**2)*mass/5
    inertia_brick_yy = (dim.x**2 + dim.z**2)*mass/5
    inertia_brick_zz = (dim.x**2 + dim.y**2)*mass/5
    body.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))   
    body.GetCollisionModel().ClearModel()
    body.GetCollisionModel().AddEllipsoid(dim.x/2, dim.y/2, dim.z/2, dr)
    body.GetCollisionModel().BuildModel()

def AddBodyForce(body, force, direction, new=True, isRelative=True):
    if new:
        direction = ChVecify(direction).GetNormalized()
        F = chrono.ChForce()
        F.SetF_x(chrono.ChFunction_Const(direction.x * force))
        F.SetF_y(chrono.ChFunction_Const(direction.y * force))
        F.SetF_z(chrono.ChFunction_Const(direction.z * force))
        body.AddForce(F)
        return F
    return False

def RemoveBodyForce(body, force_pointer):
    body.RemoveForce(force_pointer)

def ChangeBodyTexture(body, texture_file, scale=[1,1]):
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile(texture_file))
    texture.SetTextureScale(scale[0], scale[1])
    body.AddAsset(texture)

# Links
def LinkBodies_Hinge(body1, body2, link_position, link_direction):
    linkdir = ChVecify(link_direction)
    linkpos = ChVecify(link_position)
    # Get the quaternion that represents the rotation of the global z-axis to the link direction
    z_ax = chrono.ChVectorD(0,0,1)
    q = chrono.ChQuaternionD(1 + z_ax.Dot(linkdir), z_ax.Cross(linkdir))
    q.Normalize()
    
    # Create a new ChFrame coordinate system at the link position and with the global_z-to-linkdir rotation
    mframe = chrono.ChFrameD(linkpos, q)

    # Create a revolute link between the components at the coordinate system
    mlink = chrono.ChLinkRevolute()
    mlink.Initialize(body1, body2, mframe)

    return mlink

def LinkBodies_Spring(body1, pos1, body2, pos2, length, KS, KD, visible=False, spring_radius = 0.005, spring_turns = 40):
    pos1 = ChVecify(pos1)
    pos2 = ChVecify(pos2)
    mlink = chrono.ChLinkTSDA()
    mlink.Initialize(body1, body2, False, pos1, pos2)

    mlink.SetSpringCoefficient(KS)
    mlink.SetDampingCoefficient(KD)
    mlink.SetRestLength(length)
    
    if visible:
        mlink.AddAsset(chrono.ChPointPointSpring(spring_radius, 15*spring_turns, spring_turns))

    return mlink



# Simulation stuff
def ChIrrVecify(vec):
    if type(vec) == type([]):
        ChIrrVec = chronoirr.vector3df(float(vec[0]), float(vec[1]), float(vec[2]))
    elif type(vec) == type(np.array([])):
        ChIrrVec = chronoirr.vector3df(float(vec[0]), float(vec[1]), float(vec[2]))
    else:
        ChIrrVec = chronoirr.vector3df(vec)
    return ChIrrVec

def SetCamera(system_list, camera_position, look_at_point, up_direction=[0,1,0]):
    position = ChIrrVecify(camera_position)
    looker = ChIrrVecify(look_at_point)
    simulation = system_list[1]
    simulation.AddTypicalCamera(position, looker)

def Set_Lights(ChSimulation, Sources, ambients = True):
    for light in Sources:
        add_light = True
        if light[6] and not ambients: # if light is Ambient but ambients are off
            add_light = False
        if add_light:
            pos = chronoirr.vector3df(light[0][0], light[0][1], light[0][2])
            if light[7]:
                aim = chronoirr.vector3df(light[1][0], light[1][1], light[1][2])
                ChSimulation.AddLightWithShadow(pos, aim, light[2], light[3], light[4], light[5])
            else:
                ChSimulation.AddLight(pos, light[2])

def AddObjectByAPI(system_list, Object):
    system_list[0].Add(Object)

# Running the simulation
def RunSimulation(MiroSystem):
    ChSimulation = MiroSystem.system_list[1]
    ChSimulation.SetVideoframeSave(MiroSystem.record)
    ChSimulation.AddTypicalSky()
    MiroSystem.Set_Camera()
    Set_Lights(ChSimulation, MiroSystem.Environment.Get_Lightsources(), True)

                # ==IMPORTANT!== Use this function for adding a ChIrrNodeAsset to all items
                # in the system. These ChIrrNodeAsset assets are 'proxies' to the Irrlicht meshes.
                # If you need a finer control on which item really needs a visualization proxy in
                # Irrlicht, just use application.AssetBind(myitem); on a per-item basis.

    ChSimulation.AssetBindAll()

                # ==IMPORTANT!== Use this function for 'converting' into Irrlicht meshes the assets
                # that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!

    ChSimulation.AssetUpdateAll()

                # If you want to show shadows because you used "AddLightWithShadow()'
                # you must remember this:
    ChSimulation.AddShadowAll() 
    # ---------------------------------------------------------------------
    #
    #  Run the simulation
    #

    dt = 1/MiroSystem.fps # per frame
    substeps = MiroSystem.subframes

    ChSimulation.SetTimestep(dt/substeps)
    ChSimulation.SetTryRealtime(True)
    ChSimulation.SetVideoframeSaveInterval(MiroSystem.framesave_interval)

    if MiroSystem.start_paused:
        ChSimulation.SetPaused(True)
        paused = True
    else:
        paused = False

    for sensor_ID, sensor in MiroSystem.sensors.items():
        sensor.Initialize(sensor_ID+'.txt', MiroSystem)

    ChSimulation.GetDevice().run()
    ChSimulation.BeginScene()
    ChSimulation.DrawAll()
    ChSimulation.DoStep()
    ChSimulation.EndScene()

    if MiroSystem.print:
        MiroSystem.PrintModuleInfo()

    start = time.time()

    while(ChSimulation.GetDevice().run() and start + MiroSystem.delay > time.time()):
        ChSimulation.BeginScene()
        ChSimulation.DrawAll()
        for _ in range(0,substeps):
            ChSimulation.DoStep()
        ChSimulation.EndScene()

        if MiroSystem.follow and not ChSimulation.GetPaused():
            MiroSystem.Set_Camera()

    MiroSystem.Release_MiroModules()

    if MiroSystem.pre_pause:
        print('\n--- Press SPACE to release! ---')
        ChSimulation.SetPaused(True)
        paused = True
        if MiroSystem.notifier:
            MiroSystem.Environment.Get_Notifier().Set_Ready()

    while(ChSimulation.GetDevice().run()):
        # for _, link in MiroSystem.links.items():
        #     if abs(link.Get_react_force().Length()) > 30000:
        #         link.SetBroken(True)

        ChSimulation.BeginScene()
        ChSimulation.DrawAll()
        for _ in range(0,substeps):
            ChSimulation.DoStep()
            if not paused:
                for _, sensor in MiroSystem.sensors.items():
                    sensor.LogData()
        ChSimulation.EndScene()

        if (MiroSystem.follow or MiroSystem.cycle) and not paused:
            MiroSystem.Set_Camera()

        if MiroSystem.notifier and not paused and ChSimulation.GetPaused():
            paused = True
            MiroSystem.Environment.Get_Notifier().Set_Ready()
        if MiroSystem.notifier and paused and not ChSimulation.GetPaused():
            paused = False
            MiroSystem.Environment.Get_Notifier().Set_Idle()

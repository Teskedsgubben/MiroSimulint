import sys
try:
    import agx
except:
    sys.exit("Could not import AGX. Make sure the system is setup script is run, i.e. \"C:\Program Files\Algoryx\AGX-2.29.2.0\setup_env.bat\" in the terminal. Also check that you are using the correct Pyhton Interpreter.")

import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxModel
import agxRender

import time as TIME
import math
import numpy as np

API = 'AGX'

# agx is defined in another coordinate system
def xyzTransform(vec):
    return [vec[0], vec[2], vec[1]]

def agxVecify(vec, transform = True):
    if transform:
        vec = xyzTransform(vec)
    if type(vec) == type([]):
        agxVec = agx.Vec3(float(vec[0]), float(vec[1]), float(vec[2]))
    elif type(vec) == type(np.array([])):
        agxVec = agx.Vec3(float(vec[0]), float(vec[1]), float(vec[2]))
    else:
        agxVec = agx.Vec3(vec)
    return agxVec

def rotateVector(vec, rotAngle=0, rotAxis=[0,1,0], rotDegrees=True, transform=True):
    vec = agxVecify(vec, transform)
    if(rotDegrees):
        rotAngle = np.deg2rad(rotAngle)
    agxRotAxis = agxVecify(rotAxis)
    agxRotAxis.normalize()
    q = agx.Quat(rotAngle, agxRotAxis)
    rotvec = q*vec
    rotvec = [rotvec.x(), rotvec.y(), rotvec.z()]
    if transform:
        rotvec = xyzTransform(rotvec)
    return np.array(rotvec)

def rotateBody(body, rotX=0, rotY=0, rotZ=0, rotOrder=[], rotAngle=0, rotAxis=[0,1,0], rotDegrees=True):
    agxRotAxis = agxVecify(rotAxis)
    agxRotAxis.normalize()
    if(rotDegrees):
        rotX = np.deg2rad(rotX)
        rotY = np.deg2rad(rotY)
        rotZ = np.deg2rad(rotZ)
        rotAngle = np.deg2rad(rotAngle)
    
    if rotAngle:
        q = agx.Quat(rotAngle, agxRotAxis)
        body.setRotation(q*body.getRotation())

    for dim in rotOrder:
        angle = (dim == 'x')*rotX + (dim == 'y')*rotY + (dim == 'z')*rotZ
        if angle:
            axis = agx.Vec3((dim == 'x')*1, (dim == 'y')*1, (dim == 'z')*1)
            q = agx.Quat(angle, axis)
            body.setRotation(q*body.getRotation())

# System setup
def SetupSystem(args, startFunction):
    if agxPython.getContext() == None:
        init = agx.AutoInit()

    ## Create an application with graphics etc.
    app = agxOSG.ExampleApplication()

    ## Create a command line parser. sys.executable will point to python executable
    ## in this case, because getArgumentName(0) needs to match the C argv[0] which
    ## is the name of the program running
    argParser = agxIO.ArgumentParser([sys.executable] + args)
    app.addScene(argParser.getArgumentName(1), "startSimulation", ord('1'), True)

    ## Call the init method of ExampleApplication
    ## It will setup the viewer, windows etc.
    if app.init(argParser):
        app.run()
    else:
        print("An error occurred while initializing ExampleApplication.")


# Functions for adding shapes to the MiroSystem
def add_boxShapeHemi(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    add_boxShape(MiroSystem, 2*size_x, 2*size_y, 2*size_z, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxPos = agxVecify(pos)
    agxRotAxis = agxVecify(rotAxis)
       
    # Create a box
    body_box = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(size_x, size_y, size_z)))
    if Fixed:
        body_box.setMotionControl(1)
    body_box.setPosition(agxPos)

    rotateBody(body_box, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

    # Collision shape
    # if(Collide):
    
    # Visualization shape
    cylinder_shape = agxOSG.createVisual(body_box, agxRoot)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        agxOSG.setTexture(cylinder_shape, texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0]/4, scale[1]/3)
    else:
        color = agxRender.Color.Red()
        agxOSG.setDiffuseColor(cylinder_shape, color)
    
    agxSim.add(body_box)
    return body_box

def add_cylinderShape(MiroSystem, radius, height, density, pos, texture='test.jpg', scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxPos = agxVecify(pos)
    agxRotAxis = agxVecify(rotAxis)
       
    # Create a box
    body_cylinder = agx.RigidBody( agxCollide.Geometry( agxCollide.Cylinder(radius, height)))
    if Fixed:
        body_cylinder.setMotionControl(1)
    body_cylinder.setPosition(agxPos)

    rotateBody(body_cylinder, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

    # Collision shape
    # if(Collide):
    
    # Visualization shape
    box_shape = agxOSG.createVisual(body_cylinder, agxRoot)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        agxOSG.setTexture(box_shape, texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
    else:
        color = agxRender.Color.Red()
        agxOSG.setDiffuseColor(box_shape, color)
    
    agxSim.add(body_cylinder)
    return body_cylinder

def add_sphereShape(MiroSystem, radius, density, pos, texture='test.jpg', scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxPos = agxVecify(pos)
    agxRotAxis = agxVecify(rotAxis)
       
    # Create a box
    body_ball = agx.RigidBody( agxCollide.Geometry( agxCollide.Sphere(radius)))
    if Fixed:
        body_ball.setMotionControl(1)
    body_ball.setPosition(agxPos)

    rotateBody(body_ball, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

    # Collision shape
    # if(Collide):
    
    # Visualization shape
    ball_shape = agxOSG.createVisual(body_ball, agxRoot)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        agxOSG.setTexture(ball_shape, texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
    else:
        color = agxRender.Color.Red()
        agxOSG.setDiffuseColor(ball_shape, color)
    
    agxSim.add(body_ball)
    return body_ball

def add_ellisoidShape(MiroSystem, radius_x, radius_y, radius_z, pos, texture='test.jpg', density=1000, scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True):
    return

def add_stepShape(MiroSystem, position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    return

def stepShape(position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    return

# Import from file
def LoadFromObj(filename, density=1000, color=[1,0.1,0.1]):
    return

# Rigid body operations
def GetMass(body):
    body.getMassProperties().getMass()

def GetBodyPosition(body):
    agxPos = body.getPosition()
    npPos = np.array([agxPos.x(), agxPos.y(), agxPos.z()])
    return npPos

def GetBodyVelocity(body):
    agxVel = body.getPosition()
    npVel = np.array([agxVel.x(), agxVel.y(), agxVel.z()])
    return npVel
    
def GetBodyAcceleration(body):
    agxAcc = body.getPosition()
    npAcc = np.array([agxAcc.x(), agxAcc.y(), agxAcc.z()])
    return npAcc

def MoveBodyBy(body, delta_pos):
    agxPos = body.getPosition()
    body.setPosition(agxPos + agxVecify(delta_pos))

def MoveBodyTo(body, position):
    body.setPosition(agxVecify(position))

def SetBodyFixed(body, Fixed=True):
    if Fixed:
        body.setMotionControl(agx.RigidBody.KINEMATICS)
    else:
        body.setMotionControl(agx.RigidBody.DYNAMICS)

def SetBodyVelocity(body, velocity):
    agxVel = agxVecify(velocity)
    body.setVelocity(agxVel)

def SetCollisionModel_Box(body, dimensions, mass, offset):
    return

def SetCollisionModel_Ellipsoid(body, dimensions, mass, offset):
    return

def AddBodyForce(body, force, direction, new=True, isRelative=True):
    return

def RemoveBodyForce(body, force_pointer):
    return

def ChangeBodyTexture(body, texture_file, scale=[1,1]):
    return

# Links
def LinkBodies_Hinge(body1, body2, link_position, link_direction):
    hf = agx.HingeFrame()
    hf.setAxis(agxVecify(link_direction))
    hf.setCenter(agxVecify(link_position))
    link = agx.Hinge(hf, body1, body2)
    return link

def LinkBodies_Spring(body1, pos1, body2, pos2, length, KS, KD):
    spr1 = agx.Frame()
    spr1.setTranslate(agxVecify(pos1))
    spr2 = agx.Frame()
    spr2.setTranslate(agxVecify(pos2))
    spring = agx.DistanceJoint(body1, spr1, body2, spr2)
    spring.setElasticity(KS)
    spring.setDamping(KD)
    return spring

# Simulation stuff
def SetCamera(system_list, camera_position, look_at_point, up_direction=[0,1,0]):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()

    cameraData                   = app.getCameraData()
    cameraData.eye               = agxVecify(camera_position)
    cameraData.center            = agxVecify(look_at_point)
    cameraData.up                = agxVecify(up_direction)
    cameraData.nearClippingPlane = 0.1
    cameraData.farClippingPlane  = 5000
    app.applyCameraData( cameraData )
    return

def Set_Lights(ChSimulation, Sources, ambients = True):
    return

def AddObjectByAPI(system_list, Object):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()

    sim.add(Object)
    return

# Running the simulation
def RunSimulation(MiroSystem):
    return
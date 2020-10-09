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
import os
from MiroClasses import BackupColors

API = 'AGX'
TEXTURES_ON = False
important_textures = [
    'MITfloor.pngBLOCK',
    'tf-logo.jpgBLOCK',
]

# agx is defined in another coordinate system
def xyzTransform(vec, sizes = False, reverse = False):
    newvec = [-vec[0], -vec[2], vec[1]]
    if reverse:
        newvec = [-vec[0], vec[2], -vec[1]]
    return newvec

def scaleLimit(scale):
    max_scale = [1, 1]
    for i in range(len(scale)):
        if scale[i] < max_scale[i]:
            max_scale[i] = scale[i]
    return max_scale

def backupColor(texture, color):
    if texture in BackupColors.backups.keys():
        return BackupColors.backups[texture]
    return color

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
    q = agx.Quat(-rotAngle, agxRotAxis)
    rotvec = q*vec
    rotvec = [rotvec.x(), rotvec.y(), rotvec.z()]
    if transform:
        rotvec = xyzTransform(rotvec, reverse=True)
    return np.array(rotvec)

def rotateBody(body, rotX=0, rotY=0, rotZ=0, rotOrder=['x', 'y', 'z'], rotAngle=0, rotAxis=[0,1,0], rotDegrees=True):
    agxRotAxis = agxVecify(rotAxis)
    agxRotAxis.normalize()
    if(rotDegrees):
        rotX = np.deg2rad(rotX)
        rotY = np.deg2rad(rotY)
        rotZ = np.deg2rad(rotZ)
        rotAngle = np.deg2rad(rotAngle)
    
    if rotAngle:
        q = agx.Quat(-rotAngle, agxRotAxis)
        body.setRotation(body.getRotation()*q)

    for dim in rotOrder:
        angle = (dim == 'x')*-rotX + (dim == 'y')*-rotY + (dim == 'z')*-rotZ
        if angle:
            axis = agxVecify([(dim == 'x')*1, (dim == 'y')*1, (dim == 'z')*1])
            q = agx.Quat(angle, axis)
            body.setRotation(body.getRotation()*q)

def rotateBodyExp(body, rotX=0, rotY=0, rotZ=0, rotOrder=['x', 'y', 'z'], rotAngle=0, rotAxis=[0,1,0], rotDegrees=True):
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

    agx_ex = agxVecify([1,0,0])
    agx_ey = agxVecify([0,1,0])
    agx_ez = agxVecify([0,0,1])

    for dim in rotOrder:
        angle = (dim == 'x')*rotX - (dim == 'y')*rotY - (dim == 'z')*rotZ
        if angle:
            axis = (dim == 'x')*agx_ex + (dim == 'y')*agx_ey + (dim == 'z')*agx_ez
            q = agx.Quat(angle, axis)
            body.setRotation(body.getRotation()*q)

def PreSetup(args, SetupFunction):
    if agxPython.getContext():
        return
    
    init = agx.AutoInit()
    ## Create an application with graphics etc.
    app = agxOSG.ExampleApplication()

    ## Create a command line parser. sys.executable will point to python executable
    ## in this case, because getArgumentName(0) needs to match the C argv[0] which
    ## is the name of the program running
    argParser = agxIO.ArgumentParser([sys.executable] + args)

    app.addScene(argParser.getArgumentName(1), "RunSimulation", ord('1'), True)

    ## Call the init method of ExampleApplication
    ## It will setup the viewer, windows etc.
    if app.init(argParser):
        app.run()
    else:
        print("An error occurred while initializing ExampleApplication.")


# System setup
def SetupSystem():
    if agxPython.getContext():
        sim = agxPython.getContext().environment.getSimulation()
        app = agxPython.getContext().environment.getApplication()
        root = agxPython.getContext().environment.getSceneRoot()
        return [sim, app, root]
    return []

# Functions for adding shapes to the MiroSystem
def add_boxShapeHemi(MiroSystem, hemi_size_x, hemi_size_y, hemi_size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5]):
    add_boxShape(MiroSystem, 2*hemi_size_x, 2*hemi_size_y, 2*hemi_size_z, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees, mass, density, dynamic, color)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5]):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxPos = agxVecify(pos)
    agxRotAxis = agxVecify(rotAxis)
    [size_x, size_y, size_z] = xyzTransform([size_x, size_y, size_z], True)
    scale = [scale[0]/4, scale[1]/3]
       
    # Create a box
    body_geo = agxCollide.Geometry( agxCollide.Box(size_x/2, size_y/2, size_z/2))
    body_box = agx.RigidBody(body_geo)
    if Fixed:
        body_box.setMotionControl(1)
    body_box.setPosition(agxPos)

    rotateBody(body_box, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

    # Collision shape
    # if(Collide):
    
    # Visualization shape
    body_shape = agxOSG.createVisual(body_box, agxRoot)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        if TEXTURES_ON or texture in important_textures:
                # diffuseColor = agxRender.Color(1.0, 1.0, 1.0, 1)
                # ambientColor = agxRender.Color(1, 1, 1, 1)
                # specularColor = agxRender.Color(1, 1, 1, 1)
                # agxOSG.setDiffuseColor(body_shape, diffuseColor )
                # agxOSG.setAmbientColor(body_shape, ambientColor )
                # agxOSG.setSpecularColor(body_shape, specularColor )
                # agxOSG.setShininess(body_shape, 120  )
                # agxOSG.setAlpha(body_shape, 1.0 )
                # agxOSG.setTexture(body_geo, agxRoot, 'textures/'+texture)
            agxOSG.setTexture(body_shape, 'textures/'+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
        else:
            color = backupColor(texture, color)
            if len(color) == 4:
                color = agxRender.Color(color[0], color[1], color[2], color[3])
            else:
                color = agxRender.Color(color[0], color[1], color[2])
            
            agxOSG.setDiffuseColor(body_shape, color)
            
    else:
        color = agxRender.Color(color[0], color[1], color[2])
        agxOSG.setDiffuseColor(body_shape, color)
    
    agxSim.add(body_box)
    return body_box

def add_cylinderShape(MiroSystem, radius, height, density, pos, texture='test.jpg', scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxPos = agxVecify(pos)
    agxRotAxis = agxVecify(rotAxis)
    scale = scaleLimit(scale)
       
    # Create a box
    body_cylinder = agx.RigidBody( agxCollide.Geometry( agxCollide.Cylinder(radius, height)))
    if Fixed:
        body_cylinder.setMotionControl(1)
    body_cylinder.setPosition(agxPos)

    rotateBody(body_cylinder, rotX=90)
    rotateBody(body_cylinder, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

    # Collision shape
    # if(Collide):
    
    # Visualization shape
    body_shape = agxOSG.createVisual(body_cylinder, agxRoot)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        if TEXTURES_ON:
            agxOSG.setTexture(body_shape, 'textures/'+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
        else:
            color = backupColor(texture, color)
            color = agxRender.Color(color[0], color[1], color[2])
            agxOSG.setDiffuseColor(body_shape, color)
    else:
        color = agxRender.Color(color[0], color[1], color[2])
        agxOSG.setDiffuseColor(body_shape, color)
    
    agxSim.add(body_cylinder)
    return body_cylinder

def add_sphereShape(MiroSystem, radius, pos, texture='test.jpg', density=1000, scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    '''system, size_x, size_y, size_z, pos, texture, scale = [5,5], hitbox = True/False'''
    # Convert position to chrono vector, supports using chvector as input as well
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxPos = agxVecify(pos)
    agxRotAxis = agxVecify(rotAxis)
    scale = scaleLimit(scale)
       
    # Create a box
    body_ball = agx.RigidBody( agxCollide.Geometry( agxCollide.Sphere(radius)))
    if Fixed:
        body_ball.setMotionControl(1)
    body_ball.setPosition(agxPos)

    rotateBody(body_ball, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees)

    # Collision shape
    # if(Collide):
    
    # Visualization shape
    body_shape = agxOSG.createVisual(body_ball, agxRoot)
    
    # Body texture
    if texture:
        # Filter 'textures/' out of the texture name, it's added later
        if len(texture) > len('textures/'):
            if texture[0:len('textures/')] == 'textures/':
                texture = texture[len('textures/'):]
        if TEXTURES_ON:
            agxOSG.setTexture(body_shape, 'textures/'+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
        else:
            color = backupColor(texture, color)
            color = agxRender.Color(color[0], color[1], color[2])
            agxOSG.setDiffuseColor(body_shape, color)
    else:
        color = agxRender.Color(color[0], color[1], color[2])
        agxOSG.setDiffuseColor(body_shape, color)
    
    agxSim.add(body_ball)
    return body_ball

def add_ellisoidShape(MiroSystem, radius_x, radius_y, radius_z, pos, texture='test.jpg', density=1000, scale=[1,1], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    return

def add_stepShape(MiroSystem, position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    # posf = agxVecify(position_front)
    # dirf = agxVecify(direction_front)
    # posb = agxVecify(position_back)
    # dirb = agxVecify(direction_back)
    posf = np.array(position_front)
    dirf = np.array(direction_front)
    posb = np.array(position_back)
    dirb = np.array(direction_back)

    posf_out = posf + dirf*width
    posb_out = posb + dirb*width
    dir_mid = (dirf + dirb) /np.linalg.norm(dirf + dirb)
    # dir_mid.normalize()

    # size_x = ((posf-posb).length() + (posf_out-posb_out).length())/2
    size_x = (np.linalg.norm(posf-posb)+ 5*np.linalg.norm(posf_out-posb_out))/6
    size_y = height
    size_z = width

    pos = (posf+posb + posf_out+posb_out)/4
    pos[1] = pos[1] + height/2

    z = np.array([0,0,1])
    theta = np.dot(z, dir_mid)
    if (np.abs(theta) < 1):
        sign = np.cross(z, dir_mid)
        sign = sign[1]
        if sign != 0:
            sign = sign/np.abs(sign)
        else:
            sign = 1
        theta = sign*np.arccos(theta)
    else:
        theta = 0
    

    return add_boxShape(MiroSystem, size_x, size_y, size_z, pos, rotY=theta, rotDegrees=False, texture=False, color=clr)


def stepShape(position_front, direction_front, position_back, direction_back, width, height, clr = [0.5,0.5,0.5]):
    return add_stepShape(False, position_front, direction_front, position_back, direction_back, width, height, clr)


# Import from file
def LoadFromObj(filename, density=1000, color=[1,0.1,0.1]):
    return add_boxShape(False, 0.1, 0.1, 0.1, [0,0,0], color=color)

# Rigid body operations
def GetMass(body):
    return body.getMassProperties().getMass()

def GetBodyPosition(body):
    agxVec = body.getPosition()
    npVec = np.array(xyzTransform([agxVec.x(), agxVec.y(), agxVec.z()], reverse=True))
    return npVec

def GetBodyVelocity(body):
    agxVec = body.getVelocity()
    npVec = np.array(xyzTransform([agxVec.x(), agxVec.y(), agxVec.z()], reverse=True))
    return npVec
    
def GetBodyAcceleration(body):
    agxVec = body.getAcceleration()
    npVec = np.array(xyzTransform([agxVec.x(), agxVec.y(), agxVec.z()], reverse=True))
    return npVec

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

def LinkBodies_Spring(body1, pos1, body2, pos2, length, KS, KD, visible=False, spring_radius=0.05, spring_turns=50):
    if(visible):
        print('Drawing springs is currently only supported in the chrono API')
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
    [sim, app, root] = MiroSystem.Get_APIsystem()
    MiroSystem.Set_Camera()
    sim.add(ModuleReleaser(MiroSystem))
    return

class ModuleReleaser(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, MiroSystem):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.system = MiroSystem

    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_Home:
            print('Releasing Modules!')
            self.system.Release_MiroModules()
        else:
            return False
        return True
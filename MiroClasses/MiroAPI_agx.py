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
import collections

import time as TIME
import math
import numpy as np
import os
from MiroClasses import BackupColors

API = 'AGX'

TEXTURES_ON = True
TEXTURE_PATH ='textures_lowres/'
TEXTURE_EXEPTIONS = {
    'MITfloor.png': False,
    'tf-logo.jpg': True,
    'MIT_story_floor.jpg': False,
    'MIT_stone_floor.jpg': True,
    'MIT_inner_roof.jpg': False,
}

important_textures = []
for texture, include in TEXTURE_EXEPTIONS.items():
    if include:
        important_textures.append(texture)

####### UTILITY FUNCTIONS #######
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

####### SIMULATION SETUP #######
# Preparatory setup
def PreSetup(args, SetupFunction):
    if agxPython.getContext():
        return
    
    init = agx.AutoInit()
    ## Create an application with graphics etc.
    app = agxOSG.ExampleApplication()
    dec = app.getSceneDecorator()
    dec.setBackgroundColor(agx.Vec3(1,1,1))
    dec.setLogoFile('textures/TF-loader.png')
    dec.setLogoLocation(agxOSG.SceneDecorator.FREE)
    width = 0.25
    dec.setLogoPosition(0.5-width/2, 0.3)
    dec.setMaximumLogoDimension(width, 1.0)

    ## Create a command line parser. sys.executable will point to python executable
    ## in this case, because getArgumentName(0) needs to match the C argv[0] which
    ## is the name of the program running
    argParser = agxIO.ArgumentParser([sys.executable] + args)
    app.addScene(argParser.getArgumentName(1), "buildScene", ord('1'), True)

    ## Call the init method of ExampleApplication
    ## It will setup the viewer, windows etc.
    if app.init(argParser):
        app.run()
    else:
        print("An error occurred while initializing ExampleApplication.")

# MiroSystem setup call
def SetupSystem():
    if agxPython.getContext():
        sim = agxPython.getContext().environment.getSimulation()
        app = agxPython.getContext().environment.getApplication()
        root = agxPython.getContext().environment.getSceneRoot()

        # Run on maximum threads, pasted from ice_floe example
        agx.setNumThreads(0)
        n = agx.getNumThreads()*0.5-1
        agx.setNumThreads(int(n))

        
        dec = app.getSceneDecorator()
        dec.setEnableLogo(False)
        
        skybox = agxOSG.SkyBox('Campus','skybox/sky_','.jpg')
        root.addChild(skybox)
        return [sim, app, root]
    return []

# Final function call in the simulation
def RunSimulation(MiroSystem):
    [sim, app, root] = MiroSystem.Get_APIsystem()
    MiroSystem.Set_Camera()
    sim.add(SimStepper(MiroSystem))
    sim.add(ModuleReleaser(MiroSystem))
    return

####### SIMPLE SHAPE SHORTHANDS #######
# Functions for adding shapes to the MiroSystem
def add_boxShapeHemi(MiroSystem, hemi_size_x, hemi_size_y, hemi_size_z, pos, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5]):
    add_boxShape(MiroSystem, 2*hemi_size_x, 2*hemi_size_y, 2*hemi_size_z, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees, mass, density, dynamic, color)

def add_boxShape(MiroSystem, size_x, size_y, size_z, pos, texture=False, scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5], friction=False):
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
    if friction:
        high_friction_tires = agx.Material('Tires', 0.05, friction)
        body_geo.setMaterial(high_friction_tires)
    
    body_geo.setEnableCollisions(Collide)
    body_box = agx.RigidBody(body_geo)
    if mass:
        body_box.getMassProperties().setMass(mass)
    else:
        body_box.getMassProperties().setMass(size_x*size_y*size_z*density)
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
            if TEXTURE_PATH == 'textures_lowres/' and texture=='yellow_brick.jpg':
                scale[0] = 11*scale[0]
                scale[1] = 8*scale[1]
            agxOSG.setTexture(body_shape, TEXTURE_PATH+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
        else:
            color = backupColor(texture, color)
            texture = False       
    if not texture:
        agxColor = agxRender.Color(color[0], color[1], color[2])
        agxOSG.setDiffuseColor(body_shape, agxColor)
        if len(color) > 3:
                agxOSG.setAlpha(body_shape, color[3])
    
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
       
    # Create a cylinder
    body_geo = agxCollide.Geometry(agxCollide.Cylinder(radius, height))
    body_geo.setEnableCollisions(Collide)
    body_cylinder = agx.RigidBody(body_geo)
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
            agxOSG.setTexture(body_shape, TEXTURE_PATH+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], -scale[1])
        else:
            color = backupColor(texture, color)
            texture = False       
    if not texture:
        agxColor = agxRender.Color(color[0], color[1], color[2])
        agxOSG.setDiffuseColor(body_shape, agxColor)
        if len(color) > 3:
                agxOSG.setAlpha(body_shape, color[3])
    
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
    body_geo = agxCollide.Geometry(agxCollide.Sphere(radius))
    body_geo.setEnableCollisions(Collide)
    body_ball = agx.RigidBody(body_geo)
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
            agxOSG.setTexture(body_shape, TEXTURE_PATH+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
        else:
            color = backupColor(texture, color)
            texture = False       
    if not texture:
        agxColor = agxRender.Color(color[0], color[1], color[2])
        agxOSG.setDiffuseColor(body_shape, agxColor)
        if len(color) > 3:
                agxOSG.setAlpha(body_shape, color[3])
    
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

####### RIGID BODY OPERATIONS #######
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
    # # Filter 'textures/' out of the texture name, it's added later
    # if len(texture_file) > len('textures/'):
    #     if texture_file[0:len('textures/')] == 'textures/':
    #         texture_file = texture_file[len('textures/'):]
    # if TEXTURES_ON:
    #     agxOSG.setTexture(body, TEXTURE_PATH+texture_file, True, agxOSG.DIFFUSE_TEXTURE, scale[0], -scale[1])
    # else:
    #     color = backupColor(texture_file, color) 
    return

####### LINKS AND CONSTRAINTS #######
# Links
def LinkBodies_Hinge(body1, body2, link_position, link_direction, MiroSystem=False):
    hf = agx.HingeFrame()
    hf.setAxis(agxVecify(link_direction))
    hf.setCenter(agxVecify(link_position))
    link = agx.Hinge(hf, body1, body2)
    if MiroSystem:
        MiroSystem.Add(link)
    return link

def LinkBodies_Spring(body1, pos1, body2, pos2, length, KS, KD, visible=False, spring_radius=0.05, spring_turns=50):
    spr1 = agx.Frame()
    spr1.setTranslate(agxVecify(pos1))
    spr2 = agx.Frame()
    spr2.setTranslate(agxVecify(pos2))
    spring = agx.DistanceJoint(body1, spr1, body2, spr2)
    spring.setElasticity(KS)
    spring.setDamping(KD)
    return spring

####### SCENE CONFIGURATION #######
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

class SimStepper(agxSDK.StepEventListener):
    def __init__(self, MiroSystem):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.system = MiroSystem

    def preCollide(self, time):
        return

    def pre(self, time):
        self.system.Set_Camera()
        return

    def post(self, time):
        return


def addGround(MiroSystem, size_x, size_y, size_z, pos, heightmap, texture='test.jpg', scale=[4,3], Collide=True, Fixed=True, rotX=0, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, mass=False, density=1000, dynamic=False, color=[0.5, 0.5, 0.5]):

    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    # Create the ground
    ground_material = agx.Material("Ground")

    # Create the height field from a heightmap
    hf = agxCollide.HeightField.createFromFile("textures/"+heightmap, size_x, size_z, 0, size_y)

    ground_geometry = agxCollide.Geometry(hf)
    ground = agx.RigidBody(ground_geometry)
    ground.setPosition(agxVecify(pos))
    ground.setMotionControl(agx.RigidBody.STATIC)
    node = agxOSG.createVisual( ground, agxRoot )
    agxOSG.setShininess(node, 5)

    # Add a visual texture.
    agxOSG.setTexture(node, "textures/"+texture, True, agxOSG.DIFFUSE_TEXTURE, 100, 100)
    agxSim.add(ground)


def create_water_visual(geo, root):
    node = agxOSG.createVisual(geo, root)

    diffuse_color = agxRender.Color(0.0, 0.75, 1.0, 1)
    ambient_color = agxRender.Color(1, 1, 1, 1)
    specular_color = agxRender.Color(1, 1, 1, 1)
    agxOSG.setDiffuseColor(node, diffuse_color)
    agxOSG.setAmbientColor(node, ambient_color)
    agxOSG.setSpecularColor(node, specular_color)
    agxOSG.setShininess(node, 120)
    agxOSG.setAlpha(node, 0.5)
    return node

def createPond(sim, root):
    water_material = agx.Material("waterMaterial")
    water_material.getBulkMaterial().setDensity(1025)
    
    water = agxCollide.Geometry(agxCollide.Box(30, 50, 5))
    water.setMaterial(water_material)
    water.setPosition(agxVec([10,-8,45]))
    sim.add(water)
    
    controller = agxModel.WindAndWaterController()
    controller.addWater(water)
    create_water_visual(water, root)
    sim.add(controller)


class UserController(agxSDK.GuiEventListener):
    def __init__(self, Module):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.module = Module
    
    def keyboard(self, key, alt, x, y, keydown):
        if self.module.controller:
            self.module.UseController(keydown, key, alt)
            return True
        else: 
            print('No controller added to Module!')
            return False

def AddController(Module):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()
    
    controller = UserController(Module)

    sim.add(controller)

<<<<<<< HEAD
<<<<<<< HEAD

def MiniCam(MiroSystem):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    sim.add(SideViewer(MiroSystem, sim, app))


class SideViewer(agxSDK.StepEventListener):
    def __init__(self, MiroSystem, sim, app):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.system = MiroSystem
        self.app = app
        self.theta = 0
        self.dec = self.app.getSceneDecorator()
        self.dec.setEnableLogo(True)
        self.dec.setLogoLocation(agxOSG.SceneDecorator.FREE)
        width = 0.45
        self.dec.setLogoPosition(0.01, 0.01)
        self.dec.setMaximumLogoDimension(width, 3.0)
        addSecondCam(sim, app)
        

    def preCollide(self, time):
        return

    def pre(self, time):
        self.dec.setLogoFile('Second_cam.png')
        return

    def post(self, time):
        return



def addSecondCam(sim, app):
    size_color = (256, 256, 4)
    size_depth = (256, 256, 1)
    fovy = 64
    near_plane = 0.1
    far_plane = 30.0


    rti_color = agxOSG.RenderToImage(size_color[0], size_color[1])
    app.addRenderTarget(rti_color)


    rti_color.setViewMatrixAsLookAt(agx.Vec3(0,0,10), agx.Vec3(0,0,0), agx.Vec3(0,1,0))
    rti_color.setProjectionMatrixAsPerspective(fovy, size_color[1]/size_color[0], near_plane, far_plane)
    # Do not want near and far plane to move
    # rti_color.setComputeNearFarMode(agxOSG.RenderTarget.DO_NOT_COMPUTE_NEAR_FAR)

    # Create stepEventListener that extracts the image after every simulation time step
    show_images = ShowImages(rti_color, size_color)
    sim.add(show_images)


class ShowImages(agxSDK.StepEventListener):
    def __init__(self, rti_color, size_color):
        super().__init__()

        self.rti_color = rti_color
        self.size_color = size_color

    def post(self, t):

        eye = agxVecify([0,8,0])

        pos = agxVecify([0,0,0])
        
        self.rti_color.setViewMatrixAsLookAt(eye, pos, agx.Vec3(0,1,0))

        filename_color = "Second_cam.png"
        self.rti_color.saveImage(filename_color)
=======
=======
>>>>>>> 50a596603c5cb72315eaf7eea1edf8b8959f5b1b
class LidarSensor1D(agxSDK.StepEventListener):
    '''
    A 1D lidar simulated using agxCollide::Line and collision detection.
    '''
    def __init__(self,
                 sim: agxSDK.Simulation,
                 root,
                 size, 
                 world_position: agx.Vec3,
                 world_direction: agx.Vec3,
                 num_side_rays: int,
                 rad_range_side: float,
                 max_length: float,
                 rb_origin: agx.RigidBody = None,
                 draw_lines: bool = False):
        '''
        Creates the lidar sensor. The Lidar sensor is placed at the given world_position and
        directed towards the specified world_direction. It always has at least one ray in the world direction.

        :param sim: Simulation that the Lines and Listeners are added to
        :param world_position: World position of the lidar
        :param world_direction: World direction of the lidar
        :param num_side_rays: Number of rays created on either side of the middle ray. Can be 0.
        :param rad_range_side: The range within the side rays are created.
        :param max_length: The maximum length of the lidar rays
        :param rb_origin: Rigidbody to lock the lidar body to. Will lock to world if None
        :param draw_lines: debug rendering of the rays
        '''
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE + agxSDK.StepEventListener.POST_STEP)
#CHECK WHEELCONTROLLER REMOTE I PLAYGROUND
        geom = agxCollide.Geometry(agxCollide.Box(size[0], size[1], size[2]))
        geom.setName("lidar_geom")
        geom.setSensor(True)
        self.lidar_body = agx.RigidBody(geom)
        self.lidar_body.setMotionControl(agx.RigidBody.DYNAMICS)

        self.lidar_body.setRotation(agx.Quat(agx.Vec3().X_AXIS(), world_direction))
        self.lidar_body.setPosition(world_position)
 

        # if rb_origin is not None:
        #     self._relative_transform = lidar_body.getTransform() * rb_origin.getTransform().inverse()

        rays_dict = collections.OrderedDict()

        delta = 0
        start = 0
        if num_side_rays > 0:
            delta = rad_range_side/num_side_rays
            start = -rad_range_side

        for i in range(2*num_side_rays + 1):
            angle = start + i * delta
            x = max_length*math.cos(angle)
            y = max_length*math.sin(angle)
            ray = agxCollide.Geometry(agxCollide.Line(agx.Vec3(0), agx.Vec3(x, y, 0)))
            ray.setSensor(True)
            ray.setEnableSerialization(False)
            ray.addGroup("LidarGeom")
            ray.setName("Ray")
            ray.setEnableCollisions(geom, False)
            self.lidar_body.add(ray)
            rays_dict[ray.getUuid()] = [ray, max_length]

        self.cel = LidarContactSensor(self.lidar_body, rays_dict, max_length)
        sim.add(self.cel)
        sim.add(self.lidar_body)

       # self._lidar_body = lidar_body
        self._rb_origin = rb_origin
        self._rays_dict = rays_dict
        self._max_length = max_length
        self._draw_lines = draw_lines

        render_manager = sim.getRenderManager()
        if render_manager and self._draw_lines:
            render_manager.disableFlags(agxRender.RENDER_GEOMETRIES)

    def preCollide(self, t):
        if self._draw_lines:
            pos = self.lidar_body.getPosition()
            for k, v in self._rays_dict.items():
                color = v[1] / self._max_length
                ray = v[0].getShapes()[0].asLine()
                f = v[0].getFrame()
                d = f.transformPointToWorld(ray.getSecondPoint()) - pos
                agxRender.RenderSingleton.instance().add(pos, pos + v[1] * d.normal(), 0.025, agx.Vec4f(1-color**0.4, color**0.4, 0, 1))

        # clear rays
        for k in self._rays_dict.keys():
            self._rays_dict[k][1] = self._max_length

#       if self._relative_transform:
#            self._lidar_body.setTransform(self._relative_transform * self._rb_origin.getTransform())

    def get_distances(self):
        d = []
        for k, v in self._rays_dict.items():
            d.append(v[1])
        return d
    
    def getBody(self):
        return self.lidar_body

    def post(self, t):
        print(self.get_distances())

class LidarContactSensor(agxSDK.ContactEventListener):
    def __init__(self, lidar_body, rays_dict, max_length):
        super().__init__(agxSDK.ContactEventListener.IMPACT+agxSDK.ContactEventListener.CONTACT)

        self.setFilter(agxSDK.RigidBodyFilter(lidar_body))
        self.lidar_body = lidar_body
        self.rays_dict = rays_dict
        self.max_length = max_length

    def contact(self, t, gc):
        return self.handle(t, gc)

    def impact(self, t, gc):
        return self.handle(t, gc)

    def handle(self, t, gc):
        g0 = gc.geometry(0)
        g1 = gc.geometry(1)

        point = None
        g = None
        if g0.getUuid() in self.rays_dict:
            point = gc.points()[0].getPoint()
            g = g0
        elif g1.getUuid() in self.rays_dict:
            point = gc.points()[0].getPoint()
            g = g1
        else:
            # Something is in contact with lidar_geom
            return agxSDK.ContactEventListener.REMOVE_CONTACT_IMMEDIATELY
        distance = (self.lidar_body.getPosition() - point).length()

        if distance < self.rays_dict[g.getUuid()][1]:
            self.rays_dict[g.getUuid()][1] = distance

        return agxSDK.ContactEventListener.REMOVE_CONTACT_IMMEDIATELY
# def AddSensorLidar():


<<<<<<< HEAD
>>>>>>> 50a596603c5cb72315eaf7eea1edf8b8959f5b1b
=======
>>>>>>> 50a596603c5cb72315eaf7eea1edf8b8959f5b1b

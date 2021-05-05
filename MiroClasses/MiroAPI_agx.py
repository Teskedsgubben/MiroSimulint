import sys
try:
    import agx
except:
    sys.exit(
    "Could not import AGX. Make sure the system setup script is run, and check that you are using the correct Pyhton Interpreter.\n" \
    "\nRun the startup script by (may need changing to your agx version):\n"\
    "  Windows: \"C:\Program Files\Algoryx\AgX-2.30.0.0\setup_env.bat\"\n"\
    "  Mac OS : source /opt/Algoryx/AgX-2.30.0.0/setup_env.bash"
    )

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
TEXTURE_PATH ='textures/'
TEXTURE_EXEPTIONS = {
    'MITfloor.png': False,
    'tf-logo.jpg': True,
    'MIT_story_floor.jpg': False,
    'MIT_stone_floor.jpg': True,
    'MIT_inner_roof.jpg': False,
}
LOADED_TEXTURES = {}

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
    return np.array(newvec)

def IsInArea(Area, agxBody):
    pos = agxBody.getPosition()
    pos = [pos.x(), pos.y(), pos.z()]
    pos = xyzTransform(pos, reverse=True)
    x = pos[0]
    z = pos[2]
    x_max = max(Area[0])
    x_min = min(Area[0])
    z_max = max(Area[1])
    z_min = min(Area[1])

    inArea = True
    if(x < x_min or x > x_max):
        inArea = False
    if(z < z_min or z > z_max):
        inArea = False
    return inArea


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
    body_geo.setName("body")
    if friction:
        high_friction_tires = agx.Material('Tires', 0.05, friction)
        body_geo.setMaterial(high_friction_tires)
    
    body_geo.setEnableCollisions(Collide)
    body_box = agx.RigidBody(body_geo)
    if mass:
        body_box.getMassProperties().setMass(mass)
    else:
        body_box.getMassProperties().setMass(body_geo.calculateVolume()*density)
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
            if texture not in LOADED_TEXTURES.keys():
                agxTex = agxOSG.createTexture(TEXTURE_PATH+texture)
                LOADED_TEXTURES.update({texture: agxTex})
            agxOSG.setTexture(body_shape, LOADED_TEXTURES[texture], True, agxOSG.DIFFUSE_TEXTURE, scale[0], -scale[1])
            # if TEXTURE_PATH == 'textures_lowres/' and texture=='yellow_brick.jpg':
            #     scale[0] = 11*scale[0]
            #     scale[1] = 8*scale[1]
            # agxOSG.setTexture(body_shape, TEXTURE_PATH+texture, True, agxOSG.DIFFUSE_TEXTURE, scale[0], scale[1])
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
    body_geo.setName("body")
    body_geo.setEnableCollisions(Collide)
    body_cylinder = agx.RigidBody(body_geo)
    body_cylinder.getMassProperties().setMass(body_geo.calculateVolume()*density)
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
            if texture not in LOADED_TEXTURES.keys():
                agxTex = agxOSG.createTexture(TEXTURE_PATH+texture)
                LOADED_TEXTURES.update({texture: agxTex})
            agxOSG.setTexture(body_shape, LOADED_TEXTURES[texture], True, agxOSG.DIFFUSE_TEXTURE, scale[0], -scale[1])
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
    body_geo.setName("body")
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
            if texture not in LOADED_TEXTURES.keys():
                agxTex = agxOSG.createTexture(TEXTURE_PATH+texture)
                LOADED_TEXTURES.update({texture: agxTex})
            agxOSG.setTexture(body_shape, LOADED_TEXTURES[texture], True, agxOSG.DIFFUSE_TEXTURE, scale[0], -scale[1])
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


def add_OneBodyTire(MiroSystem, radius_tire, width, pos, density_tire=500, texture='test.jpg', scale=[1,1], Collide=True, Fixed=False, rotX=90, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    tire_body = add_cylinderShape(False, radius_tire, width, density_tire, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees, color)

    tire = agxModel.OneBodyTire(tire_body, radius_tire)

    tire.setImplicitFrictionMultiplier(agx.Vec2(1.5, 0.5))
    
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()

    agxSim.add(tire)
    
    return tire_body


def add_TwoBodyTire(MiroSystem, radius_rim, radius_tire, width, pos, density_rim=1000, density_tire= 500, stiffness=10^5, damping=10^3, material = None, texture='test.jpg', scale=[1,1], Collide=True, Fixed=False, rotX=90, rotY=0, rotZ=0, rotOrder=['x','y','z'], rotAngle=0, rotAxis=[1,0,0], rotDegrees=True, color=[0.5, 0.5, 0.5]):
    agxSim = agxPython.getContext().environment.getSimulation()
    agxApp = agxPython.getContext().environment.getApplication()
    agxRoot = agxPython.getContext().environment.getSceneRoot()
    
    rim_body = add_cylinderShape(False, radius_rim, width, density_rim, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees, color)
    tire_body = add_cylinderShape(False, radius_tire, width, density_tire, pos, texture, scale, Collide, Fixed, rotX, rotY, rotZ, rotOrder, rotAngle, rotAxis, rotDegrees, color)
    
    # if material == None:
    #     tire_material = agx.Material('TireMaterial')
    #     rim_body.getGeometry("").setMaterial(tire_material)
    #     tire_body.getGeometry("").setMaterial(tire_material)
    #     agxSim.add(tire_material)

    # else:
    #     rim_body.getGeometry().setMaterial(material)
    #     tire_body.getGeometry().setMaterial(material)
    #     agxSim.add(tire_material)

    tire = agxModel.TwoBodyTire(tire_body, radius_tire, rim_body, radius_rim)

    tire.setStiffness(stiffness*2, agxModel.TwoBodyTire.RADIAL)
    tire.setStiffness(stiffness*10, agxModel.TwoBodyTire.LATERAL)
    tire.setStiffness(stiffness*4, agxModel.TwoBodyTire.BENDING)
    tire.setStiffness(stiffness*0.1, agxModel.TwoBodyTire.TORSIONAL)

    tire.setDampingCoefficient(damping*2, agxModel.TwoBodyTire.RADIAL)
    tire.setDampingCoefficient(damping*10, agxModel.TwoBodyTire.LATERAL)
    tire.setDampingCoefficient(damping*4, agxModel.TwoBodyTire.BENDING)
    tire.setDampingCoefficient(damping*0.1, agxModel.TwoBodyTire.TORSIONAL)

    tire.setImplicitFrictionMultiplier(agx.Vec2(1.5, 0.5))

    agxSim.add(tire)

    return [rim_body, tire_body]

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

def SetBodyAngularFrequency(body, frequency, axis = [0,1,0]):
    agxFreq=agxVecify(axis)
    agxFreq.setLength(frequency)
    body.setAngularVelocity(agxFreq)

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
    # The line below is disabled because it messes up the steering of the example bot. 
    # link.setSolveType(agx.Constraint.DIRECT_AND_ITERATIVE)
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

def LinkBodies_WheelJoint(wheel_body, chassi_body, wheel_joint_pos, wheel_axis, steer_axis, compliance = 1e5, MiroSystem=False):

    wjf = agx.WheelJointFrame(agxVecify(wheel_joint_pos), agxVecify(wheel_axis), agxVecify(steer_axis))
    
    wj = agx.WheelJoint(wjf, wheel_body, chassi_body)
    wj.setCompliance(compliance)
    wj.setSolveType(agx.Constraint.DIRECT_AND_ITERATIVE)
    if MiroSystem:
        MiroSystem.Add(wj)
    return wj

###### Controls shorthand #######
def Keyboard(key):
    '''Returns the numeric value of a keyboard input. Available binds are:\n
    Letters such as 'a' where 'A' refers to Shift + 'a'.\n
    Number pad numerics by 'Numpad_0' etc.\n
    Others: 'KEY_UP' | 'KEY_DOWN' | 'KEY_LEFT' | 'KEY_RIGHT' | 'SPACE' | 'DELETE' | 'HOME' | 'PAGE_UP' | 'PAGE_DOWN' | 'INSERT' | 'END' '''

    controls = {
        'KEY_UP': agxSDK.GuiEventListener.KEY_Up,
        'KEY_DOWN': agxSDK.GuiEventListener.KEY_Down,
        'KEY_LEFT': agxSDK.GuiEventListener.KEY_Left,
        'KEY_RIGHT': agxSDK.GuiEventListener.KEY_Right,
        'SPACE': agxSDK.GuiEventListener.KEY_Space,
        'DELETE': agxSDK.GuiEventListener.KEY_Delete,
        'HOME': agxSDK.GuiEventListener.KEY_Home,
        'PAGE_UP': agxSDK.GuiEventListener.KEY_Page_Down,
        'PAGE_DOWN': agxSDK.GuiEventListener.KEY_Page_Up,
        'INSERT': agxSDK.GuiEventListener.KEY_Insert,
        'END': agxSDK.GuiEventListener.KEY_End,
        'Numpad_1': agxSDK.GuiEventListener.KEY_KP_1,
        'Numpad_2': agxSDK.GuiEventListener.KEY_KP_2,
        'Numpad_3': agxSDK.GuiEventListener.KEY_KP_3,
        'Numpad_4': agxSDK.GuiEventListener.KEY_KP_4,
        'Numpad_5': agxSDK.GuiEventListener.KEY_KP_5,
        'Numpad_6': agxSDK.GuiEventListener.KEY_KP_6,
        'Numpad_7': agxSDK.GuiEventListener.KEY_KP_7,
        'Numpad_8': agxSDK.GuiEventListener.KEY_KP_8,
        'Numpad_9': agxSDK.GuiEventListener.KEY_KP_9,
        'Numpad_0': agxSDK.GuiEventListener.KEY_KP_0,
    }
    if key in controls.keys():
        return controls[key]
    elif len(key) == 1:
        return ord(key)
    else:
        print('Key',key,'is not configured')
        return


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


class AutoController(agxSDK.StepEventListener):
    def __init__(self, Module, Area):
        super().__init__(agxSDK.StepEventListener.PRE_STEP)
        self.module = Module
        self.area = Area

    def pre(self, time):
        if self.module.controllerAI:
            modpos = self.module.GetCenterOfMass()
            hasControl = False
            if(modpos[0] > self.area[0][0] and modpos[0] < self.area[0][1]):
                if(modpos[2] > self.area[1][0] and modpos[2] < self.area[1][1]):
                    hasControl = True
            if hasControl:
                self.module.UseController(True, 1, False, AI = True)
            return
        else: 
            print('No AI controller added to Module!')
            return 

def AddControllerAI(Module, Area):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()
    
    controller = AutoController(Module, Area)

    sim.add(controller)

class UserController(agxSDK.GuiEventListener):
    def __init__(self, Module, Area):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.module = Module
        self.area = Area
    
    def keyboard(self, key, alt, x, y, keydown):
        if self.module.controller:
            modpos = self.module.GetCenterOfMass()
            hasControl = True
            if(modpos[0] > self.area[0][0] and modpos[0] < self.area[0][1]):
                if(modpos[2] > self.area[1][0] and modpos[2] < self.area[1][1]):
                    hasControl = False
            if hasControl:
                self.module.UseController(keydown, key, 1*(alt>0))
            return True
        else: 
            print('No controller added to Module!')
            return False
    

def AddController(Module, Area):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()
    
    controller = UserController(Module, Area)

    sim.add(controller)

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

def CreateLidar1D(lidar_body, nr_of_beams, angle, reach):
    sim = agxPython.getContext().environment.getSimulation()
    # lidar = LidarSensor1D(lidar_body, nr_of_beams, np.deg2rad(angle), range, draw_lines=True)
    
    lidar = LidarSensor1D(sim, lidar_body.getPosition(), agxVecify([-1,0,0]), nr_of_beams, np.deg2rad(angle), reach, lidar_body, True)
    # sim, lidar_body.getPosition(), agxVecify([0,1,0]), nr_of_beams, angle, reach, lidar_body, True
    # (sim, world_position, world_direction, num_side_rayst, rad_range_side, max_length, rb_origin, draw_lines):
    sim.add(lidar)
    return lidar.get_distances



class LidarSensor1D(agxSDK.StepEventListener):
    '''
    A 1D lidar simulated using agxCollide::Line and collision detection.
    '''
    def __init__(self,
                 sim: agxSDK.Simulation,
                 world_position: agx.Vec3,
                 world_direction: agx.Vec3,
                 num_side_rays: int,
                 rad_range_side: int,
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
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE)

        geom = agxCollide.Geometry(agxCollide.Box(0.1, 0.1, 0.1))
        geom.setName("lidar_geom")
        geom.setSensor(True)
        lidar_body = agx.RigidBody(geom)
        lidar_body.setMotionControl(agx.RigidBody.KINEMATICS)

        lidar_body.setRotation(agx.Quat(agx.Vec3().Z_AXIS(), world_direction))
        lidar_body.setPosition(world_position)

        if rb_origin is not None:
            self._relative_transform = lidar_body.getTransform() * rb_origin.getTransform().inverse()

        rays_dict = collections.OrderedDict()

        delta = 0
        start = 0
        if num_side_rays > 0:
            delta = rad_range_side/num_side_rays
            start = -rad_range_side

        for i in range(2*num_side_rays + 1):
            angle = start + i * delta
            z = max_length*math.cos(angle)
            y = max_length*math.sin(angle)
            ray = agxCollide.Geometry(agxCollide.Line(agx.Vec3(0), agx.Vec3(0, y, z)))
            ray.setSensor(True)
            ray.setEnableSerialization(False)
            ray.addGroup("LidarGeom")
            ray.setName("Ray")
            ray.setEnableCollisions(geom, False)
            lidar_body.add(ray)
            rays_dict[ray.getUuid()] = [ray, max_length]

        self.cel = LidarContactSensor(lidar_body, rays_dict, max_length, rb_origin)
        sim.add(self.cel)

        sim.add(lidar_body)
        self._lidar_body = lidar_body
        self._rb_origin = rb_origin
        self._rays_dict = rays_dict
        self._max_length = max_length
        self._draw_lines = draw_lines

        render_manager = sim.getRenderManager()
        if render_manager and self._draw_lines:
            render_manager.disableFlags(agxRender.RENDER_GEOMETRIES)

    def preCollide(self, t):
        if self._draw_lines:
            pos = self._lidar_body.getPosition()
            for k, v in self._rays_dict.items():
                color = v[1] / self._max_length
                ray = v[0].getShapes()[0].asLine()
                f = v[0].getFrame()
                d = f.transformPointToWorld(ray.getSecondPoint()) - pos
                agxRender.RenderSingleton.instance().add(pos, pos + v[1] * d.normal(), 0.025, agx.Vec4f(1-color**0.4, color**0.4, 0, 1))

        # clear rays
        for k in self._rays_dict.keys():
            self._rays_dict[k][1] = self._max_length

        if self._relative_transform:
            self._lidar_body.setTransform(self._relative_transform * self._rb_origin.getTransform())

    def get_distances(self):
        d = []
        for k, v in self._rays_dict.items():
            d.append(v[1])
        d.reverse()
        return d
    
    def getBody(self):
        return self.lidar_body

class LidarContactSensor(agxSDK.ContactEventListener):
    def __init__(self, lidar_body, rays_dict, max_length, rb_origin = None):
        super().__init__(agxSDK.ContactEventListener.IMPACT+agxSDK.ContactEventListener.CONTACT)

        self.setFilter(agxSDK.RigidBodyFilter(lidar_body))
        self.lidar_body = lidar_body
        self.rays_dict = rays_dict
        self.max_length = max_length
        self.rb_origin = rb_origin

    def contact(self, t, gc):
        return self.handle(t, gc)

    def impact(self, t, gc):
        return self.handle(t, gc)

    def handle(self, t, gc):
        g0 = gc.geometry(0)
        g1 = gc.geometry(1)

        if self.rb_origin is not None:
            grb_id = self.rb_origin.getGeometry("body").getUuid()
            if(grb_id == g0.getUuid() or grb_id == g1.getUuid()):
                return agxSDK.ContactEventListener.REMOVE_CONTACT_IMMEDIATELY

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

###############################
    
###############################


class LaserTrigger(agxSDK.ContactEventListener):
    def __init__(self, sideA, sideB, pos, length, rotY=0):
        super().__init__(agxSDK.ContactEventListener.IMPACT+agxSDK.ContactEventListener.CONTACT)
        self.createBeam(pos, length, rotY)
        self.laser_geo.setEnableCollisions(sideA.getGeometry("body"), False)
        self.laser_geo.setEnableCollisions(sideB.getGeometry("body"), False)
        self.setFilter(agxSDK.RigidBodyFilter(self.laser_body))
        self.triggered = False
        self.active = False

    def createBeam(self, pos, length, rotY):
        agxSim = agxPython.getContext().environment.getSimulation()
        agxApp = agxPython.getContext().environment.getApplication()
        agxRoot = agxPython.getContext().environment.getSceneRoot()

        agxPos = agxVecify(pos)
        
        self.laser_geo = agxCollide.Geometry(agxCollide.Cylinder(0.005, length))
        self.laser_geo.setName("body")
        # self.laser_geo.setEnableCollisions(False)

        self.laser_body = agx.RigidBody(self.laser_geo)
        self.laser_body.setMotionControl(1)
        self.laser_body.setPosition(agxPos)

        rotateBody(self.laser_body, rotY=rotY, rotDegrees=False)
        
        # Visualization shape
        self.laser_vis = agxOSG.createVisual(self.laser_body, agxRoot)
        agxOSG.setAlpha(self.laser_vis, 0.6)
        
        agxSim.add(self.laser_body)
        agxSim.add(self)

    def contact(self, t, gc):
        return self.handle(t, gc)

    def impact(self, t, gc):
        return self.handle(t, gc)

    def getTriggered(self):
        return self.triggered

    def setTriggered(self, trigger_status):
        self.triggered = trigger_status
        if self.triggered:
            agxColor = agxRender.Color(0, 1, 0)
        else:
            agxColor = agxRender.Color(1, 0, 0)
        agxOSG.setDiffuseColor(self.laser_vis, agxColor)

    def setActive(self, active_status):
        self.active = active_status

    def handle(self, t, gc):
        # print('yess')
        if self.triggered or not self.active:
            return agxSDK.ContactEventListener.REMOVE_CONTACT_IMMEDIATELY
        g0 = gc.geometry(0)
        g1 = gc.geometry(1)
        triggered = False
        if g0.getUuid() == self.laser_geo.getUuid():
            triggered = True
        if g1.getUuid() == self.laser_geo.getUuid():
            triggered = True
        if triggered:
            self.setTriggered(triggered)

        return agxSDK.ContactEventListener.REMOVE_CONTACT_IMMEDIATELY


class LaserTimer(agxSDK.StepEventListener):
    def __init__(self, MiroSystem, useRealTime=True):
        super().__init__(agxSDK.StepEventListener.POST_STEP)
        self.system = MiroSystem
        self.app = agxPython.getContext().environment.getApplication()
        self.lasers = []
        self.checks = []
        self.complete = False
        self.started = False
        self.useRealTime = useRealTime
        agxPython.getContext().environment.getSimulation().add(self)

    def addCheckpoint(self, posA, posB):
        posA = np.array(posA)
        posB = np.array(posB)
        h = 0.08
        sideA = add_cylinderShape(self.system, 0.025, h, 1000, posA+np.array([0,h/2,0]), texture='black_smere.jpg')
        sideB = add_cylinderShape(self.system, 0.025, h, 1000, posB+np.array([0,h/2,0]), texture='black_smere.jpg')
        dirr = (posA-posB)/np.linalg.norm(posA-posB)
        theta = -np.arccos(np.dot(dirr, np.array([0,0,1])))
        self.lasers.append(LaserTrigger(sideA, sideB, (posA+posB)/2+np.array([0,0.9*h,0]), np.linalg.norm(posA-posB), rotY=theta))
        self.lasers[-1].setTriggered(False)
        if len(self.lasers) == 1:
            self.lasers[0].setActive(True)
        self.checks.append(False)

    def reset(self):
        self.started = False
        self.complete = False
        for i in range(len(self.checks)):
            self.checks[i] = False
            self.app.getSceneDecorator().setText(i+1, str(i+1)+': '+self.getTime())
        for laser in self.lasers:
            laser.setTriggered(False)
            laser.setActive(False)
        self.lasers[0].setActive(True)

    def simTime(self):
        if self.useRealTime:
            return TIME.time()
        else:
            return self.time

    def post(self, time):
        # Check if all checkpoints have been reached
        isComplete = True
        self.time = time
        self.app.getSceneDecorator().setText(0, 'Current time: '+self.getTime())
        N = len(self.checks)
        for i in range(N):
            if not self.checks[i]:
                if self.lasers[i].getTriggered():
                    if i == 0:
                        self.startTime = TIME.time()
                        self.started = True
                    if self.started:
                        self.checks[i] = True
                        app = agxPython.getContext().environment.getApplication()
                        self.app.getSceneDecorator().setText(0, 'Last event: Checkpoint '+str(i+1)+' reached at '+self.getTime())
                        self.app.getSceneDecorator().setText(i+1, str(i+1)+': '+self.getTime())
                        if i < N-1:
                            self.lasers[i+1].setActive(True)

                    else:
                        self.app.getSceneDecorator().setText(0, 'Clock has not been started.')
            if not self.checks[i]:
                isComplete = False
        
        if isComplete and not self.complete:
            self.complete = True
            lapTime = self.simTime() - self.startTime
            self.app.getSceneDecorator().setText(len(self.checks)+1, 'Finished in '+self.getTime())
            self.reset()

        # if(not self.complete and contact.contains(self.start_object) >= 0):
        #     if TIME.time() - self.start > 10:
        #         self.start = TIME.time()
        #         self.checks = [False]*len(self.checks)
        #         for i in range(len(self.checks)):
        #             for j in range(len(self.checkpoints[i])):
        #                 obj = self.checkpoints[i][j]
        #                 obj.setPosition(self.check_positions[i][j])
        #                 obj.setRotation(self.check_rotations[i][j])
        #                 obj.setVelocity(agx.Vec3(0,0,0))
        #                 obj.setAngularVelocity(agx.Vec3(0,0,0))
        #         app = agxPython.getContext().environment.getApplication()
        #         app.getSceneDecorator().setText(0, 'Starting the time, hit the '+str(len(self.checks))+' cones!')
        #         for i in range(len(self.checks)):
        #             app.getSceneDecorator().setText(i+1, str(i+1)+': --:--')
        
        # if(self.complete and contact.contains(self.end_object) >= 0):
        #     if TIME.time() - self.start > 10:
        #         self.app.getSceneDecorator().clearText()
        #         self.app.getSceneDecorator().setText(2,'CHALLENGE COMPLETED!')
        #         self.app.getSceneDecorator().setText(4,'Time: '+self.getTime())
        #         self.complete = False
        #         self.checks = [False]*len(self.checks)
        return agxSDK.ContactEventListener.KEEP_CONTACT
    
    def getTime(self):
        if not self.started:
            return "--:--:--"
        timenum = TIME.time() - self.startTime
        seconds = round(timenum % 60, 2)
        if seconds < 10:
            seconds = '0'+str(seconds)
        else:
            seconds = str(seconds)
        if len(seconds) < 5:
            seconds = seconds[0:3]+'0'+seconds[3]
        minutes = round(np.floor(timenum/60))
        if minutes < 10:
            minutes = '0'+str(minutes)
        else:
            minutes = str(minutes)
        return minutes+':'+seconds

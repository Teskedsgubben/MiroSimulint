
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses.MiroAPI_agx import agxVecify as agxVec
import sys
import os
try:
    import agx
except:
    sys.exit("Could not import AGX for playground, run \"C:\Program Files\Algoryx\AGX-2.29.2.0\setup_env.bat\" in terminal, including citation marks.")

import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxUtil
import agxModel
import agxRender
import agxDriveTrain
from agxPythonModules.models.wheel_loaders import WheelLoaderL70
from agxPythonModules.utils.environment import simulation, root, application, init_app
from agxPythonModules.utils.callbacks import StepEventCallback, KeyboardCallback as Input, GamepadCallback as Gamepad

import time as TIME
import math
import numpy as np
import agx_playground_1 as axp
import random

try:
    import socketio
except:
    print('Socketio import failed')

if(os.path.isfile('robot_local.py')):
    import robot2_local as robot_local

    

controls = {
    'forward': agxSDK.GuiEventListener.KEY_Up,
    'backward': agxSDK.GuiEventListener.KEY_Down,
    'left': agxSDK.GuiEventListener.KEY_Left,
    'right': agxSDK.GuiEventListener.KEY_Right,
    'brake': agxSDK.GuiEventListener.KEY_Delete,
    'fjoink': agxSDK.GuiEventListener.KEY_Home,
    'toggle camera closer': agxSDK.GuiEventListener.KEY_Page_Down,
    'toggle camera farther': agxSDK.GuiEventListener.KEY_Page_Up,
    # 'reset to start': agxSDK.GuiEventListener.KEY_Home,
    'reset on spot': agxSDK.GuiEventListener.KEY_Insert,
    'boost': agxSDK.GuiEventListener.KEY_End
}



def RunPureAGX(MiroSystem):
    # This is the entry point for running pure agx code in the MiroSim environment.
    # This function will be called with SystemList = [sim, app, root] and you can
    # set Args to be whatever you want from the Main function. 
    [sim, app, root] = MiroSystem.Get_APIsystem()
    
    # CreateDigger(sim, [1,0,0.2])
    CustomAgxFunction([sim, app, root])
    axp.RunPureAGX(MiroSystem)
    # addGround(sim, app, root)
    return

def CustomAgxFunction(SystemList): 
    [sim, app, root] = SystemList
    bot_pos = [-11, 1, 7.5]
    # bot_pos = [-287, -151.43, 23.77]
    # bot_pos[0] = bot_pos[0] - 460
    # bot_pos[1] = bot_pos[1] + 2
    players = 1

    if players == 2:
        bot1_pos = [bot_pos[0]-0.35,bot_pos[1],bot_pos[2]]
        bot2_pos = [bot_pos[0]+0.35,bot_pos[1],bot_pos[2]]

        bot1 = buildBot(sim, root, bot1_pos, controller='Arrows', drivetrain = 'RWD', texture='flames.png')
        bot2 = buildBot(sim, root, bot2_pos, controller='Remote', drivetrain = 'AWD', texture='flowers.jpg')

        logger = Logger([bot1, bot2])
        sim.add(logger)

        cameraData                   = app.getCameraData()
        cameraData.eye               = agx.Vec3( 5, 5, 6)
        cameraData.center            = agx.Vec3(-6,-3, 2)
        cameraData.up                = agx.Vec3( 0,0,1 )
        cameraData.nearClippingPlane = 0.1
        cameraData.farClippingPlane  = 5000
        app.applyCameraData( cameraData )
    else:
        scale = 2/3
        # bot_pos = [5,11.2,6.85]
        
        Cam = ComboCam(app, sim, dash_direction=[0, 1, 0], dash_position=[0,-scale/2.5,scale/5], follow_distance=2.5*scale, follow_angle=10, static_position=agxVec([-3,9,-3.6]), static_looker=agxVec([5,6,3]), baserot= agx.Quat(-np.pi/2, agx.Vec3(1,0,0)))
        # Cam = False

        sim.add(CameraConroller(app))
        try:
            botBody = robot_local.buildBots(sim, root, bot_pos, controller='Arrows', drivetrain = 'RWD', texture='flames.png', camera=Cam, scale=scale)
        except:
            botBody = buildBot(sim, root, bot_pos, controller='Arrows', drivetrain = 'RWD', texture='flames.png', camera=Cam, scale=scale)

        # rot_x = agx.Quat(-np.pi/9.8, agx.Vec3(1,0,0))
        # rot_z = agx.Quat(np.pi*0.779, agx.Vec3(0,0,1))
        # botBody.setRotation(botBody.getRotation()*rot_z*rot_x)
        # botBody.setMotionControl(1)
        # sim.add(Starter(botBody, 21))
        # 
        # start_pos = [bot_pos[0], bot_pos[1], bot_pos[2]+0.2]
        # end_pos = [-298, 99.43, -24.77]
        # sim.add(ZoomCam(app, start_pos, start_pos, end_pos, speed=0.003))
        # car = robot_local.TT([sim, app, root], agxVec([6,0.0,2.3]))
        # sim.add(DummyController(car, Cam))     

        # ConeCourse(sim, root, botBody)

        buildRamp(agx.Vec3(-100,0,-0.15), sim, root)



class Starter(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, body, speed):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.body = body
        self.speed = speed

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_BackSpace:
            self.body.setMotionControl(3)
            self.body.setVelocity(self.body.getRotation()*agx.Vec3(0,0,-self.speed))
        else:
            return False
        return True


def ConeCourse(sim, root, body):
    start_plate = addboxx(sim, root, [1,0.002,1], [12,6.6401,-6])
    end_plate = addboxx(sim, root, [1,0.002,1], [-3,0.101, 0.5], color=agxRender.Color.Green())
    timer = Timer(start_plate, body, end_plate)
    sim.add(timer)
    addCones(timer)

def buildRamp(ramp_pos, sim, root):    
    off_angle = np.pi/6.5
    parts = 20
    ramp_length = 40
    ramp_height = 4
    ramp_pos = ramp_pos - agx.Vec3(0,0,ramp_height/2)
    eps_x=-0.0
    eps_z=0.0
    part_pos = agx.Vec3(ramp_pos)
    for i in range(parts):
        ramp_dim = [ramp_length/parts,15, ramp_height] # *np.cos(np.pi/4)
        ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
        theta = -(i)/parts*off_angle
        part_pos = part_pos - agx.Vec3(-np.cos(theta)*ramp_dim[0]-eps_x, 0, np.sin(theta)*ramp_dim[0]-eps_z)
        ramp.setPosition(part_pos) # +arena_size[1]/2-ramp_dim[1]/2
        ramp.setRotation(agx.Quat(theta - off_angle/parts/2, agx.Vec3(0,1,0)))
        ramp.setMotionControl(1)
        sim.add(ramp)
        agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.Gray())
    
    ramp_dim = [15,15, ramp_height] # *np.cos(np.pi/4)
    ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
    theta = -off_angle
    part_pos = part_pos - agx.Vec3(-np.cos(theta)*ramp_dim[0]-eps_x, 0, np.sin(theta)*ramp_dim[0]-eps_z)/2
    ramp.setPosition(part_pos) # +arena_size[1]/2-ramp_dim[1]/2
    ramp.setRotation(agx.Quat(theta - off_angle/parts/2, agx.Vec3(0,1,0)))
    ramp.setMotionControl(1)
    sim.add(ramp)
    agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.Gray())


def addGround(sim, app, root):
    # Create the ground
    ground_material = agx.Material("Ground")

    # Create the height field from a heightmap
    hf = agxCollide.HeightField.createFromFile("textures/terrain_heightfield.png", 800, 800, -25.1, 25.0)

    ground_geometry = agxCollide.Geometry(hf)
    ground = agx.RigidBody(ground_geometry)
    ground.setPosition(agxVec([2,-1,40]))
    ground.setMotionControl(agx.RigidBody.STATIC)
    node = agxOSG.createVisual( ground, root )
    agxOSG.setShininess(node, 5)

    # Add a visual texture.
    agxOSG.setTexture(node, "textures/stone.png", True, agxOSG.DIFFUSE_TEXTURE, 100, 100)
    sim.add(ground)

    createPond(sim, root)

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

class DummyController(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, body, camera=False, baseRot = agx.Quat()):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.body = body
        self.max_speed = 15
        self.acc = -0.15
        self.turnrate = 0.03
        self.camera = camera
        self.cameraswitched = False
        self.camera.SetBody(self.body)


    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_Up:
            self.accelerate(1)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Down:
            self.accelerate(-0.85)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Left:
            z_ax = self.body.getRotation()*agx.Vec3(0,0,1)
            turn = agx.Quat(self.turnrate, z_ax)
            self.body.setVelocity(turn*self.body.getVelocity())
            self.body.setRotation(turn*self.body.getRotation())
            self.accelerate(1)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Right:
            z_ax = self.body.getRotation()*agx.Vec3(0,0,1)
            turn = agx.Quat(-self.turnrate, z_ax)
            self.body.setVelocity(turn*self.body.getVelocity())
            self.body.setRotation(turn*self.body.getRotation())
            self.accelerate(1)
        elif keydown and key == controls['toggle camera closer']:
            if self.camera:
                if(not self.cameraswitched):
                    self.camera.ToggleCam(-1)
                self.cameraswitched = True
        elif keydown and key == controls['toggle camera farther']:
            if self.camera:
                if(not self.cameraswitched):
                    self.camera.ToggleCam(1)
                self.cameraswitched = True
        else:
            self.cameraswitched = False
            return False
        return True

    def accelerate(self, pwr):
        local_vel = self.body.getRotation().conj()*self.body.getVelocity()
        local_vel = local_vel + agx.Vec3(0, pwr*self.acc*(1 - np.abs(local_vel.y())/self.max_speed), 0)
        self.body.setVelocity(self.body.getRotation()*local_vel)

def CreateDigger(sim, pos):
    controls = WheelLoaderL70.default_keyboard_controls()
    controls.engine.forward.key = Input.KEY_Up
    controls.engine.reverse.key = Input.KEY_Down
    controls.elevate_up.key = ord( 'a' )
    controls.elevate_down.key = ord( 'z' )

    truck = WheelLoaderL70(keyboard_controls = controls)
    truck.setPosition(MiroAPI.agxVecify(pos))
    sim.add(truck)




class SocketKiller(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, socket):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.sio = socket

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_Delete:
            self.sio.disconnect()

def addboxx(sim, root, dims, pos, Fixed=True, color = agxRender.Color.Red()):
    dims = np.array(dims)/2
    if type(pos) == type([]):
        pos = agxVec(pos)
    boxx = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(agxVec(dims))))
    boxx.setPosition(pos)
    if(Fixed):
        boxx.setMotionControl(1)
    sim.add(boxx)
    agxOSG.setDiffuseColor(agxOSG.createVisual(boxx, root), color)
    return boxx

# Controls wheel torque from arrow key inputs. Supports 2 or 4 wheel drive.
# Wheels to be controlled must come as a list of [left, right, left, right]
class WheelControllerArrows(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, wheels, body, headlights=[], taillights=[], camera=False, strength=8, wheel_axis=[0,1,0], wheelfjoink=False, turn_ratio=-1/4):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.wheels = wheels
        self.camera = camera
        self.reset_rot = body.getRotation()
        self.body = body
        self.strength = strength/len(wheels)
        self.wheel_axis = [agx.Vec3(wheel_axis[0], wheel_axis[1], wheel_axis[2]), -agx.Vec3(wheel_axis[0], wheel_axis[1], wheel_axis[2])]
        self.whlfjoink = wheelfjoink
        self.trun = turn_ratio
        self.headlights = headlights
        self.taillights = taillights
        self.braking = False
        self.backing = False
        self.throttling = False
        self.cameraswitched = False
        self.restorePosition = self.body.getPosition()+agx.Vec3(0,0,0.4)

        if camera:
            self.camera.SetBody(self.body)
    
    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == controls['boost']:
            # BOOST
            self.body.setVelocity(self.body.getVelocity()*1.06)
        elif keydown and key == controls['fjoink']:
            # Fjoink
            if(self.body.getVelocity().z() < 1):
                self.body.setVelocity(self.body.getVelocity()+agx.Vec3(0,0,6))
                if self.whlfjoink:
                    for wheel in self.wheels:
                        wheel.setVelocity(wheel.getVelocity()+agx.Vec3(0,0,6))
        elif keydown and key == controls['left']:
            # Turn left
            for i in range(0, len(self.wheels), 2):
                self.wheels[i+1].addLocalTorque(self.strength*self.wheel_axis[(i+1)%2])
                self.wheels[i].addLocalTorque(self.trun*self.strength*self.wheel_axis[i%2])

        elif keydown and key == controls['right']:
            # Turn right
            for i in range(0, len(self.wheels), 2):
                self.wheels[i+1].addLocalTorque(self.trun*self.strength*self.wheel_axis[(i+1)%2])
                self.wheels[i].addLocalTorque(self.strength*self.wheel_axis[i%2])

        elif keydown and key == controls['backward']:
            # Back up
            for i in range(0, len(self.wheels)):
                self.wheels[i].addLocalTorque(-self.strength/2*self.wheel_axis[i%2])
            if not self.backing:
                self.backing = True
                for taillight in self.taillights:
                    agxOSG.setTexture(taillight, 'textures/taillight_back.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)                 

        elif keydown and key == controls['forward']:
            # Gain speed
            for i in range(0, len(self.wheels)):
                self.wheels[i].addLocalTorque(self.strength*self.wheel_axis[i%2])
            if not self.throttling:
                self.throttling = True
                for headlight in self.headlights:
                    agxOSG.setTexture(headlight, 'textures/headlight_on.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0) 

        elif keydown and key == controls['brake']:
            # Back up
            for wheel in self.wheels:
                wheel.setAngularVelocityDamping(40*self.body.getMassProperties().getMass())
            if not self.braking:
                self.braking = True
                for taillight in self.taillights:
                    agxOSG.setTexture(taillight, 'textures/taillight_brake.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)  
        
        
        elif keydown and key == controls['toggle camera closer']:
            if self.camera:
                if(not self.cameraswitched):
                    self.camera.ToggleCam(-1)
                self.cameraswitched = True
        elif keydown and key == controls['toggle camera farther']:
            if self.camera:
                if(not self.cameraswitched):
                    self.camera.ToggleCam(1)
                self.cameraswitched = True
        
        # elif keydown and key == controls['reset to start']:
        #     self.body.setPosition(-9, 0 , 7.5)
        #     self.body.setAngularVelocity(0,0,0)
        #     self.body.setVelocity(agx.Vec3(0,0,0))
        #     self.body.setRotation(self.reset_rot)

        elif keydown and key == controls['reset on spot']:
            self.body.setPosition(self.restorePosition)
            self.body.setAngularVelocity(0,0,0)
            self.body.setVelocity(agx.Vec3(0,0,0))
            self.body.setRotation(self.reset_rot)
        else:
            self.cameraswitched = False
            if(self.braking or self.backing):
                if self.braking:
                    self.braking = False
                    for wheel in self.wheels:
                        wheel.setAngularVelocityDamping(0)
                self.backing = False
                for taillight in self.taillights:
                    agxOSG.setTexture(taillight, 'textures/taillight_off.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
            if self.throttling:
                self.throttling = False
                for headlight in self.headlights:
                    agxOSG.setTexture(headlight, 'textures/headlight_off.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
            self.restorePosition = self.body.getPosition()+agx.Vec3(0,0,0.4)
            return False
        return True

class WheelControllerRemote(agxSDK.StepEventListener):
    def __init__(self, wheels, body, socket, camera):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.body = body
        self.wheels = wheels
        self.strength = 8/len(wheels)
        self.sio = socket
        self.sio.connect("http://home.chlav.se:10001")
        self.status = {
            'left': False,
            'right': False,
            'forward': False,
            'backward': False,
            'fjoink': False,
            'reset': False
        }
        @self.sio.on("forward")
        def on_forward(active):
            self.status['forward'] = bool(active)
        @self.sio.on("backward")
        def on_backward(active):
            self.status['backward'] = bool(active)
        @self.sio.on("left")
        def on_left(active):
            self.status['left'] = bool(active)
        @self.sio.on("right")
        def on_right(active):
            self.status['right'] = bool(active)
        @self.sio.on("fjoink")
        def on_fjoink(active):
            self.status['fjoink'] = bool(active)
        @self.sio.on("reset")
        def on_resett(active):
            self.status['reset'] = bool(active)

    def preCollide(self, time):
        return

    def pre(self, time):
        if(self.status['left']):
            # Turn left
            for i in range(0, len(self.wheels), 2):
                self.wheels[i+1].addLocalTorque(0, self.strength,0)
                self.wheels[i].addLocalTorque(0, -self.strength/4,0)
        elif(self.status['right']):
            # Turn right
            for i in range(0, len(self.wheels), 2):
                self.wheels[i].addLocalTorque(0, self.strength,0)
                self.wheels[i+1].addLocalTorque(0, -self.strength/4,0) 
        elif(self.status['backward']):
            # Back up
            for wheel in self.wheels:
                wheel.addLocalTorque(0,-self.strength/2,0) 
        elif(self.status['forward']):
            # Gain speed
            for wheel in self.wheels:
                wheel.addLocalTorque(0, self.strength,0)
        elif(self.status['fjoink']):
            if(self.body.getVelocity().z() < 1E-4):
                self.body.setVelocity(self.body.getVelocity()+agx.Vec3(0,0,4))
        elif(self.status['reset']):
            self.body.setPosition(-9, 0 , 7.5)
        return

    def post(self, time):
        return

class CameraConroller(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, app):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.app = app

    def updateUp(self, axis=[0,1,0]):
        cameraData                   = self.app.getCameraData()
        cameraData.up                = agxVec(axis)
        self.app.applyCameraData(cameraData)

    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == ord('z'):
            self.updateUp()
        else:
            return False
        return True

class Exploder(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.bodylist = []

    def AddBody(self, body):
        self.bodylist.append(body)

    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_BackSpace:
            self.explode()
        else:
            return False
        return True

    def explode(self):
        for body in self.bodylist:
            body.setVelocity(5000*agxVec([0.5-random.random(),0.5-random.random(),0.5-random.random()]))

def buildBot(sim, root, bot_pos, controller='Arrows', drivetrain = 'FWD', color=False, texture=False, camera=False, scale=1):
    EXPLODE = Exploder()
    sim.add(EXPLODE)
    
    strength = 8

    body_wid = 0.32*scale
    body_len = 0.6*scale
    body_hei = 0.15 *scale
    
    wheel_rad = 0.07*scale
    wheel_wid = 0.02*scale
    wheel_dmp = -0.02*scale
    wheel_gap = 0.004*scale

    body = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(body_wid/2, body_hei/2, body_len/2)))
    body.setPosition(bot_pos[0], bot_pos[1], bot_pos[2] + body_hei/2 + wheel_rad + wheel_dmp )
    # body.setMotionControl(1)
    body.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
    sim.add(body)
    
    EXPLODE.AddBody(body)
    vis_body = agxOSG.createVisual(body, root)
    if color:
        agxOSG.setDiffuseColor(vis_body, color)
    elif texture:
        agxOSG.setTexture(vis_body, 'textures/'+texture, True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    else:
        agxOSG.setDiffuseColor(vis_body, agxRender.Color.Green())

    wheel_dx = body_wid/2+wheel_wid/2+wheel_gap

    wheelLF = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelLF.setPosition(bot_pos[0]-wheel_dx, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelLF.setMotionControl(1)
    wheelLF.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelLF)
    
    EXPLODE.AddBody(wheelLF)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelLF, root), agxRender.Color.Red())

    wheelRF = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelRF.setPosition(bot_pos[0]+wheel_dx, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelRF.setMotionControl(1)
    wheelRF.setRotation(agx.Quat(-np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelRF)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelRF, root), agxRender.Color.Red())

    wheelLB = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelLB.setPosition(bot_pos[0]-wheel_dx, bot_pos[1]-(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelLB.setMotionControl(1)
    wheelLB.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelLB)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelLB, root), agxRender.Color.Red())

    wheelRB = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelRB.setPosition(bot_pos[0]+wheel_dx, bot_pos[1]-(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelRB.setMotionControl(1)
    wheelRB.setRotation(agx.Quat(-np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelRB)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelRB, root), agxRender.Color.Red())

    for wheel in [wheelLB, wheelLF, wheelRB, wheelRF]:
        vis_body = agxOSG.createVisual(wheel, root)
        agxOSG.setTexture(vis_body, 'textures/tire.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)

    x_ax = agx.Vec3(1,0,0)
    y_ax = agx.Vec3(0,1,0)
    z_ax = agx.Vec3(0,0,1)

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(-1,0,0))
    hf.setCenter(agx.Vec3(bot_pos[0]-body_wid/2, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad))
    axleLF = agx.Hinge(hf, body, wheelLF)
    sim.add(axleLF)

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(-1,0,0))
    hf.setCenter(agx.Vec3(bot_pos[0]-body_wid/2, bot_pos[1]-(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad))
    axleLB = agx.Hinge(hf, body, wheelLB)
    sim.add(axleLB)

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3( 1,0,0))
    hf.setCenter(agx.Vec3(bot_pos[0]+body_wid/2, bot_pos[1]-(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad))
    axleRB = agx.Hinge(hf, body, wheelRB)
    sim.add(axleRB)
    
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3( 1,0,0))
    hf.setCenter(agx.Vec3(bot_pos[0]+body_wid/2, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad))
    axleRF = agx.Hinge(hf, body, wheelRF)
    sim.add(axleRF)

    ## Headlights
    light_rad = 0.02*scale
    light_dep = 0.01*scale

    headlightL = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(light_rad, light_dep)))
    headlightL.setPosition( bot_pos[0] + 0.79*body_wid/2, bot_pos[1] + body_len/2+light_dep/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp)
    # headlightL.setMotionControl(1)
    # headlightL.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(headlightL)
    headlightL_vis = agxOSG.createVisual(headlightL, root)
    agxOSG.setTexture(headlightL_vis, 'textures/headlight_off.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3( bot_pos[0] + 0.79*body_wid/2, bot_pos[1] + body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp ))
    HLL = agx.Hinge(hf, body, headlightL)
    sim.add(HLL)
    hf.setAxis(agx.Vec3(0,0,1))
    HLL = agx.Hinge(hf, body, headlightL)
    sim.add(HLL)

    headlightR = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(light_rad, light_dep)))
    headlightR.setPosition(bot_pos[0] -0.79*body_wid/2, bot_pos[1] + body_len/2+light_dep/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp )
    # headlightR.setMotionControl(1)
    # headlightR.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(headlightR)
    headlightR_vis = agxOSG.createVisual(headlightR, root)
    agxOSG.setTexture(headlightR_vis, 'textures/headlight_off.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3(bot_pos[0] -0.79*body_wid/2, bot_pos[1] + body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp ))
    HLR = agx.Hinge(hf, body, headlightR)
    sim.add(HLR)
    hf.setAxis(agx.Vec3(0,0,1))
    HLR = agx.Hinge(hf, body, headlightR)
    sim.add(HLR)
    
    light_wid = 0.012*scale
    light_hei = 0.02*scale
    light_dep = 0.003*scale

    taillightL = agx.RigidBody(agxCollide.Geometry( agxCollide.Box(light_wid, light_dep, light_hei)))
    taillightL.setPosition(bot_pos[0] -0.79*body_wid/2,bot_pos[1] -(body_len/2+light_dep/2), bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp)
    sim.add(taillightL)
    taillightL_vis = agxOSG.createVisual(taillightL, root)
    agxOSG.setTexture(taillightL_vis, 'textures/taillight_off.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3(bot_pos[0] -0.79*body_wid/2, bot_pos[1] -body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp + light_hei/3))
    TLL_hi = agx.Hinge(hf, body, taillightL)
    sim.add(TLL_hi)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3(bot_pos[0] -0.79*body_wid/2, bot_pos[1] -body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp - light_hei/3))
    TLL_low = agx.Hinge(hf, body, taillightL)
    sim.add(TLL_low)

    taillightR = agx.RigidBody(agxCollide.Geometry( agxCollide.Box(light_wid, light_dep, light_hei)))
    taillightR.setPosition( bot_pos[0] + 0.79*body_wid/2,bot_pos[1] -(body_len/2+light_dep/2), bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp)
    sim.add(taillightR)
    taillightR_vis = agxOSG.createVisual(taillightR, root)
    agxOSG.setTexture(taillightR_vis, 'textures/taillight_off.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3( bot_pos[0] + 0.79*body_wid/2,bot_pos[1]-body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp + light_hei/3))
    TLR = agx.Hinge(hf, body, taillightR)
    sim.add(TLR)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3( bot_pos[0] + 0.79*body_wid/2,bot_pos[1]-body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp - light_hei/3))
    TLR = agx.Hinge(hf, body, taillightR)
    sim.add(TLR)


    wheels = [wheelLF, wheelRF] # default FWD
    if drivetrain == 'FWD':
        wheels = [wheelLF, wheelRF]
    elif drivetrain == 'RWD':
        wheels = [wheelLB, wheelRB]
    elif drivetrain == 'AWD':
        wheels = [wheelLF, wheelRF, wheelLB, wheelRB]
    
    if controller == 'Remote':
        sio = socketio.Client()
        sim.add(WheelControllerRemote(wheels, body, sio))
        # sim.add(SocketKiller(sio))
    else:
        sim.add(WheelControllerArrows(wheels, body, headlights=[headlightL_vis, headlightR_vis], taillights=[taillightL_vis, taillightR_vis], camera=camera, strength=strength*(scale**5)))


    ################# Stuff to make it fancy #################
    


    windangle = np.pi/4
    windshield = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(0.9*body_wid/2, 0.003*scale, body_hei/3)))
    windshield.setPosition(bot_pos[0], bot_pos[1]+body_len/5, bot_pos[2] + body_hei + wheel_rad + wheel_dmp + np.cos(windangle)*body_hei/3)
    # windshield.setTorque(0,0,100)
    # windshield.setMotionControl(2)
    windshield.setRotation(agx.Quat(windangle, agx.Vec3(1,0,0)))
    sim.add(windshield)
    wind_vis = agxOSG.createVisual(windshield, root)
    agxOSG.setAlpha(wind_vis, 0.45)
    agxOSG.setTexture(wind_vis, 'textures/windshield.jpg', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,0,1))
    hf.setCenter(agx.Vec3(-body_wid/3, body_len/5, bot_pos[2] + body_hei + wheel_rad + wheel_dmp))
    windh1 = agx.Hinge(hf, body, windshield)
    sim.add(windh1)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,0,1))
    hf.setCenter(agx.Vec3(body_wid/3, body_len/5, bot_pos[2] + body_hei + wheel_rad + wheel_dmp))
    windh2 = agx.Hinge(hf, body, windshield)
    sim.add(windh2)

    backwindangle = -np.pi/10
    sh = 0.02*scale
    proportion = 1/16
    wing_dims = [0.95*body_wid/2, 0.0022*scale, 1.25*body_hei*proportion]
    wing = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(wing_dims[0], wing_dims[1], wing_dims[2])))
    wing.setPosition(bot_pos[0], bot_pos[1]-body_len/2.08, bot_pos[2] + body_hei + wheel_rad + wheel_dmp + sh + 0.0011*scale)
    # windshield.setTorque(0,0,100)
    # windshield.setMotionControl(2)
    wing.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
    sim.add(wing)
    wind_vis = agxOSG.createVisual(wing, root)
    # agxOSG.setAlpha(wind_vis, 0.45)
    carbon_scale = 3.5
    agxOSG.setTexture(wind_vis, 'textures/carbonfiber.png', True, agxOSG.DIFFUSE_TEXTURE, carbon_scale, carbon_scale*wing_dims[2]/wing_dims[0])
    
    pole_tilt = np.pi/1.7
    poleL = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(0.0025*scale, sh)))
    poleL.setPosition(bot_pos[0]-body_wid/2.5, bot_pos[1]-body_len/2.1, bot_pos[2] + body_hei + wheel_rad + wheel_dmp + sh/2)
    poleL.setRotation(agx.Quat(pole_tilt, agx.Vec3(1,0,0)))
    sim.add(poleL)
    pole_vis = agxOSG.createVisual(poleL, root)
    agxOSG.setTexture(pole_vis, 'textures/chrome.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    
    poleR = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(0.0025*scale, sh)))
    poleR.setPosition(bot_pos[0]+body_wid/2.5, bot_pos[1]-body_len/2.1, bot_pos[2] + body_hei + wheel_rad + wheel_dmp + sh/2)
    poleR.setRotation(agx.Quat(pole_tilt, agx.Vec3(1,0,0)))
    sim.add(poleR)
    pole_vis = agxOSG.createVisual(poleR, root)
    agxOSG.setTexture(pole_vis, 'textures/chrome.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,0,1))
    hf.setCenter(wing.getPosition() + agx.Vec3(body_wid/2.5, 0, 0))
    windh1 = agx.Hinge(hf, body, wing)
    sim.add(windh1)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,0,1))
    hf.setCenter(wing.getPosition() - agx.Vec3(body_wid/2.5, 0, 0))
    windh2 = agx.Hinge(hf, body, wing)
    sim.add(windh2)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,np.cos(pole_tilt), np.sin(pole_tilt)))
    hf.setCenter(agx.Vec3(poleL.getPosition()))
    windh1 = agx.Hinge(hf, body, poleL)
    sim.add(windh1)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,np.cos(pole_tilt), np.sin(pole_tilt)))
    hf.setCenter(agx.Vec3(poleR.getPosition()))
    windh2 = agx.Hinge(hf, body, poleR)
    sim.add(windh2)


    plate_dh = -0.043*scale
    plate_dep = 0.001*scale
    plate_front = agx.RigidBody(agxCollide.Geometry( agxCollide.Box(body_wid*0.21, plate_dep, body_hei/11)))
    plate_front.setPosition(bot_pos[0],bot_pos[1] + body_len/2+plate_dep/2, bot_pos[2] + body_hei/2 + wheel_rad + wheel_dmp + plate_dh)
    sim.add(plate_front)
    plate_vis = agxOSG.createVisual(plate_front, root)
    agxOSG.setTexture(plate_vis, 'textures/brumbo.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(plate_front.getPosition() + agx.Vec3( body_wid/2.5, -plate_dep, 0))
    hing = agx.Hinge(hf, body, plate_front)
    sim.add(hing)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(plate_front.getPosition() + agx.Vec3(-body_wid/2.5, -plate_dep, 0))
    hing = agx.Hinge(hf, body, plate_front)
    sim.add(hing)

    
    plate_back = agx.RigidBody(agxCollide.Geometry( agxCollide.Box(body_wid*0.21, plate_dep, body_hei/11)))
    plate_back.setPosition(bot_pos[0],bot_pos[1] - body_len/2-plate_dep/2, bot_pos[2] + body_hei/2 + wheel_rad + wheel_dmp + plate_dh)
    sim.add(plate_back)
    plate_vis = agxOSG.createVisual(plate_back, root)
    agxOSG.setTexture(plate_vis, 'textures/brumbo.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(plate_back.getPosition() + agx.Vec3( body_wid/2.5, plate_dep, 0))
    hing = agx.Hinge(hf, body, plate_back)
    sim.add(hing)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(plate_back.getPosition() + agx.Vec3(-body_wid/2.5, plate_dep, 0))
    hing = agx.Hinge(hf, body, plate_back)
    sim.add(hing)

    # return a pointer to the body
    return body

# Create a class that is triggered at various steps in the simulation
class Logger(agxSDK.StepEventListener):
    def __init__(self, logbodies):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        import socketio
        self.sio = socketio.Client()
        self.sio.connect("http://home.chlav.se:10001")
        self.bodies = logbodies

    def preCollide(self, time):
        return

    def pre(self, time):
        return
    
    def post(self, time):
        data = []
        for body in self.bodies:
            pos = body.getPosition()
            data.append({
                'x': pos.x(),
                'y': pos.y(),
                'z': pos.z(),
            })
        self.sio.emit("pos", data)
        return

# Create a class that is triggered at various steps in the simulation
class FollowCam(agxSDK.StepEventListener):
    def __init__(self, app, object_to_follow, distance=2.5, angle=10):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.app = app
        self.body = object_to_follow
        self.dist = distance
        self.angl = np.deg2rad(angle)
        
        self.relative_position = self.dist*agx.Vec3(0,-np.cos(self.angl), np.sin(self.angl))
        self.looker = self.body.getPosition()
        self.position = self.relative_position + self.looker 
        self.updateCamera()

    def preCollide(self, time):
        return

    def pre(self, time):
        relative_position = -self.body.getVelocity()

        if(relative_position.length() > 1E-2):
            relative_position.set(0.0, 2)
            relative_position.setLength(self.dist)
            relative_position.set(relative_position.x()*np.cos(self.angl), relative_position.y()*np.cos(self.angl), self.dist*np.sin(self.angl))
            
            relative_position = self.relative_position + relative_position/60
            relative_position.setLength(self.dist)
            relative_position.set(relative_position.x()*np.cos(self.angl), relative_position.y()*np.cos(self.angl), self.dist*np.sin(self.angl))

            self.relative_position = relative_position
            self.looker = self.body.getPosition()
            self.position = self.relative_position + self.looker 

            self.updateCamera()
        return
    
    def updateCamera(self):
        cameraData                   = self.app.getCameraData()
        cameraData.eye               = self.position
        cameraData.center            = self.looker
        cameraData.up                = agx.Vec3( 0, 0, 1 )
        cameraData.nearClippingPlane = 0.1
        cameraData.farClippingPlane  = 5000
        self.app.applyCameraData( cameraData )

    def post(self, time):
        return






# Create a class that is triggered at various steps in the simulation
class DashCam(agxSDK.StepEventListener):
    def __init__(self, app, body, direction=[0,1,0], relative_position=[0, 0, 0.15]):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.app = app
        self.body = body
        
        self.dir = agx.Vec3(direction[0], direction[1], direction[2])
        self.rel_pos = agx.Vec3(relative_position[0], relative_position[1], relative_position[2])
        
        self.baserot = agx.Quat(-np.pi/2, agx.Vec3(1,0,0))
        rotq = self.baserot*self.body.getRotation()
        self.position = self.body.getPosition() + rotq*self.rel_pos
        self.looker = self.position + rotq*self.dir
        self.up = rotq*agx.Vec3(0,0,1)

        self.updateCamera()

    def preCollide(self, time):
        return

    def pre(self, time):
        if(self.body.getVelocity().length() > 1E-2):
            rotq = self.baserot*self.body.getRotation()
            self.position = self.body.getPosition() + rotq*self.rel_pos
            self.looker = self.position + rotq*self.dir
            self.up = rotq*agx.Vec3(0,0,1)

            self.updateCamera()
        return
    
    def updateCamera(self):
        cameraData                   = self.app.getCameraData()
        cameraData.eye               = self.position
        cameraData.center            = self.looker
        cameraData.up                = self.up
        cameraData.nearClippingPlane = 0.1
        cameraData.farClippingPlane  = 5000
        self.app.applyCameraData( cameraData )

    def post(self, time):
        return


class ComboCam(agxSDK.StepEventListener):
    def __init__(self, app, sim, dash_direction=[0,1,0], dash_position=[0, 0, 0.15], follow_distance=2.5, follow_angle=10, default=1, far_factors=[1.75, 2.25], static_position=agxVec([-3,8,-5.6]), static_looker=agxVec([5,5,3]), baserot=agx.Quat()):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.camera_modes = ['dash', 'follow near', 'follow far', 'static']
        self.cam_i = default
        self.app = app
        sim.add(self)

        # DashCam Prep
        self.dash_dir = agx.Vec3(dash_direction[0], dash_direction[1], dash_direction[2])
        self.dash_rel_pos = agx.Vec3(dash_position[0], dash_position[1], dash_position[2])
        self.baserot = baserot

        # FollowCam Prep
        self.ff = far_factors
        self.dist = follow_distance
        self.angle = np.deg2rad(follow_angle)
        self.follow_rel_pos = self.dist*agx.Vec3(0,-np.cos(self.angle), np.sin(self.angle))

        # StaticCam Prep
        self.static_position = static_position
        self.static_looker = static_looker
        self.static_up = agx.Vec3(0,0,1)
        self.static = False

    def SetBody(self, body):
        self.body = body

    def preCollide(self, time):
        return

    def pre(self, time):
        if self.camera_modes[self.cam_i] == 'follow near':
            self.follow_update(self.dist, self.angle)
        if self.camera_modes[self.cam_i] == 'follow far':
            self.follow_update(self.dist*self.ff[0], self.angle*self.ff[1])
        if self.camera_modes[self.cam_i] == 'dash':
            self.dash_update()
        if self.camera_modes[self.cam_i] == 'static':
            self.static_update()
    
    def post(self, time):
        return

    def follow_update(self, distance, angle):
        relative_position = -self.body.getVelocity()

        if(relative_position.length() > 1E-2):
            relative_position.set(0.0, 2)
            relative_position.setLength(distance)
            relative_position.set(relative_position.x()*np.cos(angle), relative_position.y()*np.cos(angle), distance*np.sin(angle))
            
            relative_position = self.follow_rel_pos + relative_position/60
            relative_position.setLength(distance)
            relative_position.set(relative_position.x()*np.cos(angle), relative_position.y()*np.cos(angle), distance*np.sin(angle))

            self.follow_rel_pos = relative_position
            self.looker = self.body.getPosition()
            self.position = self.follow_rel_pos + self.looker 
            self.up = agx.Vec3(0,0,1)

            self.updateCamera()

    def dash_update(self):
        if(self.body.getVelocity().length() > 1E-2):
            rotq = self.baserot*self.body.getRotation()
            self.position = self.body.getPosition() + rotq*self.dash_rel_pos
            self.looker = self.position + rotq*self.dash_dir
            self.up = rotq*agx.Vec3(0,0,1)
            self.updateCamera()

    def static_update(self):
        if not self.static:
            self.position = self.static_position
            self.looker = self.static_looker
            self.up = self.static_up
            self.static = True
            self.updateCamera()
        cameraData = self.app.getCameraData()
        self.static_position = agx.Vec3(cameraData.eye)
        self.static_looker = agx.Vec3(cameraData.center)
        self.static_up = agx.Vec3(cameraData.up)
    
    
    def ToggleCam(self, add = 1):
        self.cam_i = (self.cam_i+add) % len(self.camera_modes)
        self.static = False
        if self.camera_modes[self.cam_i] == 'follow near':
            self.follow_rel_pos = -self.body.getVelocity()
            self.follow_rel_pos.set(0.0, 2)
            self.follow_rel_pos.setLength(self.dist)
            self.follow_rel_pos.set(self.follow_rel_pos.x()*np.cos(self.angle), self.follow_rel_pos.y()*np.cos(self.angle), self.dist*np.sin(self.angle))
        if self.camera_modes[self.cam_i] == 'follow far':
            self.follow_rel_pos = -self.body.getVelocity()
            self.follow_rel_pos.set(0.0, 2)
            self.follow_rel_pos.setLength(self.dist*self.ff[0])
            self.follow_rel_pos.set(self.follow_rel_pos.x()*np.cos(self.angle*self.ff[1]), self.follow_rel_pos.y()*np.cos(self.angle*self.ff[1]), self.dist*np.sin(self.angle*self.ff[1]))
        # print(self.camera_modes[self.cam_i])

    def updateCamera(self):
        cameraData                   = self.app.getCameraData()
        cameraData.eye               = self.position
        cameraData.center            = self.looker
        cameraData.up                = self.up
        cameraData.nearClippingPlane = 0.1
        cameraData.farClippingPlane  = 5000
        self.app.applyCameraData( cameraData )

class Timer(agxSDK.ContactEventListener):
    def __init__(self, start_object, robot_body, end_object=False):
        super().__init__(agxSDK.ContactEventListener.ALL)
        self.app = agxPython.getContext().environment.getApplication()
        self.start_object = start_object
        if end_object:
            self.end_object = end_object
        else:
            self.end_object = start_object
        self.body = robot_body
        self.start = False
        self.checkpoints = []
        self.check_positions = []
        self.check_rotations = []
        self.checks = []
        self.complete = False

    def addCheckpoint(self, checkpoint_object_list=[]):
        pos_list = []
        rot_list = []
        for obj in checkpoint_object_list:
            pos_list.append(obj.getPosition())
            rot_list.append(obj.getRotation())
        self.check_positions.append(pos_list)
        self.check_rotations.append(rot_list)
        self.checkpoints.append(checkpoint_object_list)
        self.checks.append(False)

    def impact(self, time, contact):
        # Check if all checkpoints have been reached
        isComplete = True
        for i in range(len(self.checks)):
            if not self.checks[i]:
                for obj in self.checkpoints[i]:
                    if contact.contains(obj) >= 0 and contact.contains(self.body) >= 0:
                        if self.start:
                            self.checks[i] = True
                            app = agxPython.getContext().environment.getApplication()
                            self.app.getSceneDecorator().setText(0, 'Last event: Checkpoint '+str(i+1)+' reached at '+self.getTime())
                            self.app.getSceneDecorator().setText(i+1, str(i+1)+': '+self.getTime())
                        else:
                            self.app.getSceneDecorator().setText(0, 'Clock has not been started.')
            if not self.checks[i]:
                isComplete = False
        
        if isComplete and not self.complete:
            self.complete = True
            self.app.getSceneDecorator().setText('All checkpoints reached, go for the goal!')

        if(not self.complete and contact.contains(self.start_object) >= 0):
            if TIME.time() - self.start > 10:
                self.start = TIME.time()
                self.checks = [False]*len(self.checks)
                for i in range(len(self.checks)):
                    for j in range(len(self.checkpoints[i])):
                        obj = self.checkpoints[i][j]
                        obj.setPosition(self.check_positions[i][j])
                        obj.setRotation(self.check_rotations[i][j])
                        obj.setVelocity(agx.Vec3(0,0,0))
                        obj.setAngularVelocity(agx.Vec3(0,0,0))
                app = agxPython.getContext().environment.getApplication()
                app.getSceneDecorator().setText(0, 'Starting the time, hit the '+str(len(self.checks))+' cones!')
                for i in range(len(self.checks)):
                    app.getSceneDecorator().setText(i+1, str(i+1)+': --:--')
        
        if(self.complete and contact.contains(self.end_object) >= 0):
            if TIME.time() - self.start > 10:
                self.app.getSceneDecorator().clearText()
                self.app.getSceneDecorator().setText(2,'CHALLENGE COMPLETED!')
                self.app.getSceneDecorator().setText(4,'Time: '+self.getTime())
                self.complete = False
                self.checks = [False]*len(self.checks)
        return agxSDK.ContactEventListener.KEEP_CONTACT
    
    def getTime(self):
        timenum = TIME.time() - self.start
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





    # obstacles(sim, root, arena_pos[2])

def addCones(timer=False):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()
    cone_dims = [0.008, 0.08, 0.25]

    cone_positions = [
        [12,6.64,11],
        [6.5,7.698,3],
        [-7,3.32,7],
        [16,3.32,11],
        [3,0,14],
        [-5,0,4],
        [6,0,-8],
        [0,0.1,-1],
    ]

    for cone_pos in cone_positions:
        plate_rel_h = 0.015
        dh = np.array([0,0,cone_dims[2]*plate_rel_h])
        cone_pos = np.array(cone_pos)
        bottom = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(agxVec([cone_dims[1]*1.2, cone_dims[2]*plate_rel_h, cone_dims[1]*1.2]))))
        bottom.setPosition(agxVec(cone_pos+dh))
        sim.add(bottom)
        agxOSG.setDiffuseColor(agxOSG.createVisual(bottom, root), agxRender.Color.Orange())
        cone = agx.RigidBody( agxCollide.Geometry( agxCollide.Cone(cone_dims[0], cone_dims[1], cone_dims[2])))
        cone.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
        cone.setPosition(agxVec(cone_pos+2*dh))
        agxOSG.setDiffuseColor(agxOSG.createVisual(cone, root), agxRender.Color.Orange())
        sim.add(cone)

        hf = agx.HingeFrame()
        hf.setAxis(agx.Vec3(0,0,1))
        hf.setCenter(agxVec(cone_pos+2*dh))
        H = agx.Hinge(hf, bottom, cone)
        sim.add(H)
        
        traffic_cone = [bottom, cone]
        if timer:
            timer.addCheckpoint(traffic_cone)


class CycleCam(agxSDK.StepEventListener):
    def __init__(self, app, target, distance=2.5, tilt=16, start_angle=0):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.app = app
        self.dist = distance
        self.dlooker = distance/5
        self.tilt = np.deg2rad(tilt)
        angle = np.deg2rad(start_angle)
        self.speed=0.002
        
        self.relative_position = self.dist*agx.Vec3(np.sin(angle),-np.cos(self.tilt)*np.cos(angle), np.sin(self.tilt))
        self.relative_looker = self.dist*agx.Vec3(np.sin(angle+np.pi/2),-np.cos(self.tilt)*np.cos(angle+np.pi/2), np.sin(self.tilt))
        
        self.target = agx.Vec3(target[0], target[1], target[2])
        self.position = self.relative_position + self.target
        self.looker = self.relative_looker + self.target  

        self.updateCamera()

    def preCollide(self, time):
        return

    def pre(self, time):
        relative_position = agx.Quat(self.speed, agx.Vec3(0,0,1))*self.relative_position
        relative_position.setLength(self.dist)

        relative_looker = agx.Quat(self.speed, agx.Vec3(0,0,1))*self.relative_looker
        relative_looker.setLength(self.dlooker)

        self.relative_position = relative_position
        self.relative_looker = relative_looker

        self.position = self.relative_position + self.target 
        self.looker = self.relative_looker + self.target 

        self.updateCamera()
        return
    
    def updateCamera(self):
        cameraData                   = self.app.getCameraData()
        cameraData.eye               = self.position
        cameraData.center            = self.looker
        cameraData.up                = agx.Vec3( 0, 0, 1 )
        cameraData.nearClippingPlane = 0.1
        cameraData.farClippingPlane  = 5000
        self.app.applyCameraData( cameraData )

    def post(self, time):
        return

class ZoomCam(agxSDK.StepEventListener):
    def __init__(self, app, target, start, end, speed=0.0001):
        super().__init__(agxSDK.StepEventListener.PRE_COLLIDE+agxSDK.StepEventListener.PRE_STEP+agxSDK.StepEventListener.POST_STEP)
        self.app = app
        self.looker = agx.Vec3(target[0], target[1], target[2])
        self.start = agx.Vec3(start[0], start[1], start[2])
        self.end = agx.Vec3(end[0], end[1], end[2])
        self.position = self.start
        self.speed = speed
        self.ratio = 0
        
        self.updateCamera()

    def preCollide(self, time):
        return

    def pre(self, time):
        self.position = (1-self.ratio**4)*self.start + self.ratio**4*self.end
        self.ratio = self.ratio + self.speed
        self.updateCamera()
        return
    
    def updateCamera(self):
        cameraData                   = self.app.getCameraData()
        cameraData.eye               = self.position
        cameraData.center            = self.looker
        cameraData.up                = agx.Vec3( 0, 0, 1 )
        cameraData.nearClippingPlane = 0.1
        cameraData.farClippingPlane  = 5000
        self.app.applyCameraData( cameraData )

    def post(self, time):
        return
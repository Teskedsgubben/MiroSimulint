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

controls = {
    'forward': agxSDK.GuiEventListener.KEY_Up,
    'backward': agxSDK.GuiEventListener.KEY_Down,
    'left': agxSDK.GuiEventListener.KEY_Left,
    'right': agxSDK.GuiEventListener.KEY_Right,
    'brake': agxSDK.GuiEventListener.KEY_Delete,
    'fjoink': agxSDK.GuiEventListener.KEY_End,
    'toggle camera closer': agxSDK.GuiEventListener.KEY_Page_Down,
    'toggle camera farther': agxSDK.GuiEventListener.KEY_Page_Up,
    'reset to start': agxSDK.GuiEventListener.KEY_Home,
    'reset on spot': agxSDK.GuiEventListener.KEY_Insert,
}

def ControlModule(MiroMod):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    wheels = []
    wheels.append(MiroMod.GetComponent('Wheel: Left').GetBody())
    wheels.append(MiroMod.GetComponent('Wheel: Right').GetBody())
    # wheels.append(MiroMod.Get_Component('Wheel: Front').GetBody())
    body = MiroMod.GetComponent('Top Body').GetBody()
    cam = ComboCam(app, sim)
    sim.add(WheelControllerArrows(wheels, body, strength=1, wheel_axis=[0,-1,0], camera=cam))


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

        self.camera.SetBody(self.body)
    
    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == controls['fjoink']:
            # Fjoink
            if(self.body.getVelocity().z() < 1E-2):
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
        
        elif keydown and key == controls['reset to start']:
            self.body.setPosition(-9, 0 , 7.5)
            self.body.setAngularVelocity(0,0,0)
            self.body.setVelocity(agx.Vec3(0,0,0))
            self.body.setRotation(self.reset_rot)

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
        self.baserot = self.body.getRotation()*agx.Quat(np.pi/2, agx.Vec3(0,0,1))

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
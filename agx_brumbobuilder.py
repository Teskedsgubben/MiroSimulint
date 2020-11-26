
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import sys
try:
    import agx
except:
    sys.exit("Could not import AGX for playground, run \"C:\Program Files\Algoryx\AGX-2.29.2.0\setup_env.bat\" in terminal, including citation marks.")

import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxModel
import agxRender
import agxDriveTrain
from agxPythonModules.models.wheel_loaders import WheelLoaderL70
from agxPythonModules.utils.environment import simulation, root, application, init_app
from agxPythonModules.utils.callbacks import StepEventCallback, KeyboardCallback as Input, GamepadCallback as Gamepad

import time
import math
import numpy as np

try:
    import socketio
except:
    print('Socketio import failed')

def RunPureAGX(MiroSystem):
    # This is the entry point for running pure agx code in the MiroSim environment.
    # This function will be called with SystemList = [sim, app, root] and you can
    # set Args to be whatever you want from the Main function. 
    [sim, app, root] = MiroSystem.Get_APIsystem()
    BrumboDemo(sim, app, root, 1.0)
    return


class BrumboCreator(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, sim, root, bot_pos):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.body_built = False
        self.wheel_built = False
        self.wheel_turned = False
        self.wheel_connected = False
        self.pos = bot_pos

        self.sim = sim
        self.root = root

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        bot_pos = self.pos  
        strength = 8

        body_wid = 0.32
        body_len = 0.6
        body_hei = 0.15
        
        wheel_rad = 0.07
        wheel_wid = 0.02
        wheel_dmp = -0.02
        wheel_gap = 0.001
        if keydown and not self.body_built and key == agxSDK.GuiEventListener.KEY_Insert:
            self.body_built = True
            self.body = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(body_wid/2, body_hei/2, body_len/2)))
            self.body.setPosition(bot_pos[0], bot_pos[1], bot_pos[2] + body_hei/2 + wheel_rad + wheel_dmp )
            self.body.setMotionControl(1)
            self.body.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
            self.sim.add(self.body)

            agxOSG.setTexture(agxOSG.createVisual(self.body, self.root), 'textures/flames.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)

        elif keydown and not self.wheel_built and key == agxSDK.GuiEventListener.KEY_Home:
            wheel_dx = body_wid/2+wheel_wid/2+wheel_gap
            self.wheelLF = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
            self.wheelLF.setPosition(bot_pos[0]-wheel_dx-0.08, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
            self.wheelLF.setMotionControl(1)
            self.sim.add(self.wheelLF)
            self.wheelLF.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
            
            agxOSG.setTexture(agxOSG.createVisual(self.wheelLF, self.root), 'textures/tire.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)

        elif keydown and not self.wheel_built and key == agxSDK.GuiEventListener.KEY_Delete:
            self.wheelLF.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
            
        elif keydown and not self.wheel_built and key == agxSDK.GuiEventListener.KEY_End:
            wheel_dx = body_wid/2+wheel_wid/2+wheel_gap
            self.wheelLF.setPosition(bot_pos[0]-wheel_dx, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
            hf = agx.HingeFrame()
            hf.setAxis(agx.Vec3(-1,0,0))
            hf.setCenter(agx.Vec3(bot_pos[0]-body_wid/2, bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad))
            axleLF = agx.Hinge(hf, self.body, self.wheelLF)
            self.sim.add(axleLF)

        else:
            return False
        return True


def BrumboDemo(sim, app, root, scale):
    position = [-9.7, 5.8, 7.54]
    sim.add(BrumboCreator(sim, root, position))
    sim.add(CycleCam(app, position))

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
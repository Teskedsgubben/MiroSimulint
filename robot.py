import sys

try:
    import agx
except:
    sys.exit("Could not import AGX, run \"C:\Program Files\Algoryx\AGX-2.29.2.0\setup_env.bat\" in terminal, including citation marks.")

import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxModel
import agxRender

import time
import math
import numpy as np

import socketio

class SocketKiller(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, socket):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.sio = socket

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_Delete:
            self.sio.disconnect()


# Controls wheel torque from arrow key inputs. Supports 2 or 4 wheel drive.
# Wheels to be controlled must come as a list of [left, right, left, right]
class WheelControllerArrows(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, wheels, body):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.wheels = wheels
        self.body = body
        self.strength = 8/len(wheels)
        # self.root = agxPython.getContext().environment.getSceneRoot()
        # app = agxPython.getContext().environment.getApplication()

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_Left:
            # Turn left
            for i in range(0, len(self.wheels), 2):
                self.wheels[i+1].addLocalTorque(0, self.strength,0)
                self.wheels[i].addLocalTorque(0, -self.strength/4,0)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Right:
            # Turn right
            for i in range(0, len(self.wheels), 2):
                self.wheels[i].addLocalTorque(0, self.strength,0)
                self.wheels[i+1].addLocalTorque(0, -self.strength/4,0)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Down:
            # Back up
            for wheel in self.wheels:
                wheel.addLocalTorque(0,-self.strength/2,0)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Up:
            # Gain speed
            for wheel in self.wheels:
                wheel.addLocalTorque(0, self.strength,0)
        elif keydown and key == agxSDK.GuiEventListener.KEY_Home:
            self.body.setPosition(-9, 0 , 7.5)
            for wheel in self.wheels:
                wheel.setPosition(-9.4, 0 , 7.5)

        else:
            return False
        return True

# Controls wheel torque from arrow key inputs. Supports 2 or 4 wheel drive.
# Wheels to be controlled must come as a list of [left, right, left, right]
class WheelControllerNumpad(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, wheels):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.wheels = wheels
        self.strength = 8/len(wheels)
        # self.root = agxPython.getContext().environment.getSceneRoot()
        # app = agxPython.getContext().environment.getApplication()

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_KP_4:
            # Turn left
            for i in range(0, len(self.wheels), 2):
                self.wheels[i+1].addLocalTorque(0, self.strength,0)
                self.wheels[i].addLocalTorque(0, -self.strength/4,0)

        elif keydown and key == agxSDK.GuiEventListener.KEY_KP_6:
            # Turn right
            for i in range(0, len(self.wheels), 2):
                self.wheels[i].addLocalTorque(0, self.strength,0)
                self.wheels[i+1].addLocalTorque(0, -self.strength/4,0)

        elif keydown and key == agxSDK.GuiEventListener.KEY_KP_2:
            # Back up
            for wheel in self.wheels:
                wheel.addLocalTorque(0,-self.strength/2,0)

        elif keydown and key == agxSDK.GuiEventListener.KEY_KP_8:
            # Gain speed
            for wheel in self.wheels:
                wheel.addLocalTorque(0, self.strength,0)
        else:
            return False
        return True

class WheelControllerRemote(agxSDK.StepEventListener):
    def __init__(self, wheels, body, socket):
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

class Fjoink(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, body):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.body = body
        self.hopper = agxSDK.GuiEventListener.KEY_Page_Down

    def setHopper(self, hopper):
        self.hopper = hopper
        return self

    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == self.hopper:
            if(self.body.getVelocity().z() < 1E-4):
                self.body.setVelocity(self.body.getVelocity()+agx.Vec3(0,0,5))
        else:
            return False
        return True





def buildBot(sim_system, bot_pos, controller='Arrows', drivetrain = 'FWD', color=False, texture=False):
    [sim, app, root] = sim_system
    scale = 1

    body_wid = 0.32*scale
    body_len = 0.6*scale
    body_hei = 0.16 *scale
    
    wheel_rad = 0.07*scale
    wheel_wid = 0.02*scale
    wheel_dmp = -0.02*scale

    body = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(body_wid/2, body_len/2, body_hei/2)))
    body.setPosition(bot_pos[0], bot_pos[1], bot_pos[2] + body_hei/2 + wheel_rad + wheel_dmp )
    # body.setMotionControl(1)
    body.setRotation(agx.Quat(np.pi, agx.Vec3(0,0,1)))
    sim.add(body)
    vis_body = agxOSG.createVisual(body, root)
    if color:
        agxOSG.setDiffuseColor(vis_body, color)
    elif texture:
        agxOSG.setTexture(vis_body, 'textures/'+texture, True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    else:
        agxOSG.setDiffuseColor(vis_body, agxRender.Color.Green())

    wheelLF = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelLF.setPosition(bot_pos[0]-(body_wid/2+wheel_wid/2), bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelLF.setMotionControl(1)
    wheelLF.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelLF)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelLF, root), agxRender.Color.Red())

    wheelRF = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelRF.setPosition(bot_pos[0]+(body_wid/2+wheel_wid/2), bot_pos[1]+(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelRF.setMotionControl(1)
    wheelRF.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelRF)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelRF, root), agxRender.Color.Red())

    wheelLB = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelLB.setPosition(bot_pos[0]-(body_wid/2+wheel_wid/2), bot_pos[1]-(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelLB.setMotionControl(1)
    wheelLB.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelLB)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelLB, root), agxRender.Color.Red())

    wheelRB = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(wheel_rad, wheel_wid)))
    wheelRB.setPosition(bot_pos[0]+(body_wid/2+wheel_wid/2), bot_pos[1]-(body_len/2-wheel_rad*1.8), bot_pos[2]+wheel_rad)
    # wheelRB.setMotionControl(1)
    wheelRB.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(wheelRB)
    # agxOSG.setDiffuseColor(agxOSG.createVisual(wheelRB, root), agxRender.Color.Red())

    for wheel in [wheelLB, wheelLF, wheelRB, wheelRF]:
        vis_body = agxOSG.createVisual(wheel, root)
        agxOSG.setTexture(vis_body, 'textures/tire.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)

    light_rad = 0.02
    light_dep = 0.01

    headlightL = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(light_rad, light_dep)))
    headlightL.setPosition( bot_pos[0] + 0.79*body_wid/2, bot_pos[1] + body_len/2+light_dep/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp)
    # headlightL.setMotionControl(1)
    # headlightL.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(headlightL)
    agxOSG.setTexture(agxOSG.createVisual(headlightL, root), 'textures/light.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3( bot_pos[0] + 0.79*body_wid/2, bot_pos[1] + body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp ))
    HLL = agx.Hinge(hf, body, headlightL)
    sim.add(HLL)

    headlightR = agx.RigidBody(agxCollide.Geometry( agxCollide.Cylinder(light_rad, light_dep)))
    headlightR.setPosition(bot_pos[0] -0.79*body_wid/2, bot_pos[1] + body_len/2+light_dep/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp )
    # headlightR.setMotionControl(1)
    # headlightL.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(headlightR)
    agxOSG.setTexture(agxOSG.createVisual(headlightR, root), 'textures/light.png', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(0,1,0))
    hf.setCenter(agx.Vec3(bot_pos[0] -0.79*body_wid/2, bot_pos[1] + body_len/2, bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp ))
    HLR = agx.Hinge(hf, body, headlightR)
    sim.add(HLR)


    light_wid = 0.012
    light_hei = 0.02
    light_dep = 0.003

    taillightL = agx.RigidBody(agxCollide.Geometry( agxCollide.Box(light_wid, light_dep, light_hei)))
    taillightL.setPosition(bot_pos[0] -0.79*body_wid/2,bot_pos[1] -(body_len/2+light_dep/2), bot_pos[2] + 0.7*body_hei + wheel_rad + wheel_dmp)
    # taillightL.setMotionControl(1)
    # headlightL.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(taillightL)
    agxOSG.setDiffuseColor(agxOSG.createVisual(taillightL, root), agxRender.Color.Red())
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
    # taillightR.setMotionControl(1)
    # headlightL.setRotation(agx.Quat(np.pi/2, agx.Vec3(0,0,1)))
    sim.add(taillightR)
    agxOSG.setDiffuseColor(agxOSG.createVisual(taillightR, root), agxRender.Color.Red())
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

    windangle = np.pi/4
    windshield = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(0.9*body_wid/2, 0.005, body_hei/3)))
    windshield.setPosition(bot_pos[0], bot_pos[1]+body_len/5, bot_pos[2] + body_hei + wheel_rad + wheel_dmp + np.cos(windangle)*body_hei/3)
    # windshield.setTorque(0,0,100)
    # windshield.setMotionControl(2)
    windshield.setRotation(agx.Quat(windangle, agx.Vec3(1,0,0)))
    sim.add(windshield)
    agxOSG.setTexture(agxOSG.createVisual(windshield, root), 'textures/windshield.jpg', True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)


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

    wheels = [wheelLF, wheelRF] # default FWD
    if drivetrain == 'FWD':
        wheels = [wheelLF, wheelRF]
    elif drivetrain == 'RWD':
        wheels = [wheelLB, wheelRB]
    elif drivetrain == 'AWD':
        wheels = [wheelLF, wheelRF, wheelLB, wheelRB]
    
    if controller == 'Numpad':
        sim.add(WheelControllerNumpad(wheels))
        sim.add(Fjoink(body).setHopper(agxSDK.GuiEventListener.KEY_KP_Subtract))
    elif controller == 'Remote':
        sio = socketio.Client()
        sim.add(WheelControllerRemote(wheels, body, sio))
        # sim.add(SocketKiller(sio))
        sim.add(Fjoink(body))
    else:
        sim.add(WheelControllerArrows(wheels, body))
        sim.add(Fjoink(body))

    # return a pointer to the body
    return body
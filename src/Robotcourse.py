import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

import sys

try:
    import agx
except:
    print("Could not import AGX to run Robotcourse")

import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxModel
import agxRender

import time as TIME
import math
import random

width = 8

class Timer(agxSDK.ContactEventListener):
    def __init__(self, trigger_object):
        super().__init__(agxSDK.ContactEventListener.ALL)
        self.trigger = trigger_object
        self.start = TIME.time()
        self.checkpoints = []
        self.checks = []

    def addCheckpoint(self, checkpoint_object):
        self.checkpoints.append(checkpoint_object)
        self.checks.append(False)

    def impact(self, time, contact):
        # Check if all checkpoints have been reached
        complete = True
        for i in range(len(self.checks)):
            if(not self.checks[i] and contact.contains(self.checkpoints[i]) >= 0):
                self.checks[i] = True
                print('Checkpoint '+str(i+1)+' reached!')
            if not self.checks[i]:
                complete = False
        
        if(complete and contact.contains(self.trigger) >= 0):
            if TIME.time() - self.start > 10:
                timenum = TIME.time() - self.start
                seconds = str(round(timenum % 60, 2))
                minutes = round(np.floor(timenum/60))
                if minutes < 10:
                    minutes = '0'+str(minutes)
                else:
                    minutes = str(minutes)
                print('Time: '+minutes+':'+seconds)
            self.start = TIME.time()
            for i in range(len(self.checks)):
                self.checks[i] = False
        return agxSDK.ContactEventListener.KEEP_CONTACT

def buildArena(arena_pos):
    sim = agxPython.getContext().environment.getSimulation()
    app = agxPython.getContext().environment.getApplication()
    root = agxPython.getContext().environment.getSceneRoot()

    arena_size = [width, width, 0.2]
    h = 0.7
    
    floor = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(arena_size[0]/2, arena_size[1]/2, arena_size[2]/2)))
    floor.setPosition(arena_pos[0], arena_pos[1], arena_pos[2]-arena_size[2]/2)
    floor.setMotionControl(1)
    sim.add(floor)
    agxOSG.setDiffuseColor(agxOSG.createVisual(floor, root), agxRender.Color.Gray())

    sides = 8
    side_len = width/(1+np.sqrt(2)) + arena_size[2]/2/np.sqrt(2)
    base_pos = agx.Vec3(arena_pos[0], arena_pos[1], arena_pos[2]-arena_size[2]/2+h/2)
    for w in range(sides):
        theta = -w*np.pi/4
        rot = agx.Quat(theta, agx.Vec3(0,0,1))
        rot_pos = agx.Vec3(np.sin(theta)*width/2, -np.cos(theta)*width/2, 0)

        wall = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(side_len/2, arena_size[2]/2, h/2)))
        wall.setPosition(base_pos + rot_pos)
        wall.setMotionControl(1)
        wall.setRotation(rot)
        sim.add(wall)
        agxOSG.setDiffuseColor(agxOSG.createVisual(wall, root), agxRender.Color.DarkGray())
                                              
    # obstacles(sim, root, arena_pos[2])

def obstacles(sim, root, h):
    #start plattform
    dims = [1.5*(width/14), 1.5*(width/14), 0.06]
    pos = [-6*(width/14), 0, h+dims[2]/2]
    startbox = addboxx(sim, root, dims, pos)

    #timer
    timer = Timer(startbox)
    sim.add(timer)

    dims = [0.1*(width/14), 1.5*(width/14), 0.3]
    pos = [-6.75*(width/14), 0, h+dims[2]/2]
    addboxx(sim, root, dims, pos)
    
    dims = [0.1*(width/14), 1.5*(width/14), 0.3]
    pos = [-5.25*(width/14), 0, h+dims[2]/2]
    addboxx(sim, root, dims, pos)
    
    dims = [1.6*(width/14), 0.1*(width/14), 0.3]
    pos = [-6*(width/14), -0.75*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    # wall

    dims = [4.0*(width/14), 0.1*(width/14), 0.22]
    pos = [-3.3*(width/14), -0.6*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    # Random stuff in the first quarter
    dims = [0.2*(width/14), 0.2*(width/14), 0.8]
    pos = [-4*(width/14), 0, h+dims[2]/2]
    addboxx(sim, root, dims, pos)
    
    dims = [0.4*(width/14), 0.25*(width/14), 0.2]
    pos = [-3*(width/14), 1.5*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)


    for i in range(30):
        x = -0.5*(width/14) - random.random()*4.75*(width/14)
        y = -0.5*(width/14) + random.random()*6*(width/14)
        dims = [random.random()*0.6*(width/14), random.random()*0.6*(width/14), random.random()*0.6]
        pos = agx.Vec3(x, y, 0)
        if pos.length() < 1.5*(width/14):
            pos.setLength(1.5*(width/14)+random.random()*3.75*(width/14))
        if pos.length() > 7.0*(width/14):
            pos.setLength(1.5*(width/14)+random.random()*5.5*(width/14))
        pos.set(h+dims[2]/2, 2)
        addboxx(sim, root, dims, pos)
    
    # Pole in the middle with walls around
    dims = [0.28*(width/14), 1.4*(width/14)]
    pos = [0, 0, h+dims[1]/2]
    can = addcylinder(sim, root, dims, pos, texture='textures/schrodbull.png')
    can.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
    pos = [0, 0, h+dims[1]]
    dims = [0.28*(width/14), 0.025*(width/14)]
    pos[2] = pos[2] + dims[1]/2
    lid = addcylinder(sim, root, dims, pos, texture='textures/sodacan_lid.png')
    lid.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))

    dims = [0.3*(width/14), 2.0*(width/14), 0.4]
    pos = [-1.15*(width/14), 0, h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [2.6*(width/14), 0.3*(width/14), 0.4]
    pos = [0, -1.15*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [0.3*(width/14), 2.0*(width/14), 0.4]
    pos = [1.15*(width/14), 0, h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [0.3*(width/14), 7.0*(width/14), 0.4]
    pos = [0, 3.5*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)
    
    # Seesaw board
    dims = [2.1*(width/14), 0.25*(width/14), 0.3]
    pos = [2.1*(width/14), 0.4*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)
    seesaw(sim, root, [3.75*(width/14),0.9*(width/14),h*(width/14)], -0.85*np.pi, h=0.1)
    dims = [0.5*(width/14), 3.8*(width/14), 0.18]
    pos = [4.8*(width/14), 3.15*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    # Ballroom walls
    dims = [0.25*(width/14), 4.3*(width/14), 0.3]
    pos = [6.0*(width/14), 0.0, h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [0.25*(width/14), 1.0*(width/14), 0.3]
    pos = [2.1*(width/14), -1.0*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [0.25*(width/14), 1.4*(width/14), 0.3]
    pos = [3.0*(width/14), -0.4*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [0.25*(width/14), 2.4*(width/14), 0.3]
    pos = [2.5*(width/14), -3.0*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [1.1*(width/14), 0.25*(width/14), 0.3]
    pos = [3.1*(width/14), -3.1*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [0.66*(width/14), 0.25*(width/14), 0.3]
    pos = [2.3*(width/14), -1.65*(width/14), h+dims[2]/2]
    wall_1 = addboxx(sim, root, dims, pos)
    dims = [2.8*(width/14), 0.25*(width/14), 0.3]
    pos = [3.95*(width/14), -2.0*(width/14), h+dims[2]/2]
    wall_2 = addboxx(sim, root, dims, pos)
    dims = [3.91*(width/14), 0.25*(width/14), 0.3]
    pos = [4.65*(width/14), -3.45*(width/14), h+dims[2]/2]
    wall_3 = addboxx(sim, root, dims, pos)
    wall_1.setRotation(agx.Quat(-np.pi/4, agx.Vec3(0,0,1)))
    wall_2.setRotation(agx.Quat(-np.pi/4, agx.Vec3(0,0,1)))
    wall_3.setRotation(agx.Quat( np.pi/4, agx.Vec3(0,0,1)))

    # Ballroom balls
    for i in range(200):
        x = 4.0*(width/14) + random.random()*2.8*(width/14)
        y = 0.75*(width/14) - random.random()*2.5*(width/14)
        rad = 0.025*(width/14) + random.random()*0.075*(width/14)
        pos = agx.Vec3(x, y, h+rad+3*random.random()*rad)
        addball(sim, root, rad, pos, Fixed=False)

    # Climbing ramp
    dx = 0.8
    bot_tilt = 0.0445
    dims = [dx*(width/14), 2.5*(width/14), 0.6]
    bot_tilt = np.arcsin(0.45/(2.5*4))
    dif = dims[1]/2*np.cos(bot_tilt)-0.002*np.sin(bot_tilt)
    dh = 2*np.sin(bot_tilt)*dif
    for i in range(4):
        angle = (i+1)*np.pi
        pos = [2*(width/14)-dx*i*(width/14), -4.7*(width/14)-0.015*(-1)**i*(width/14), -0.3+h+(i+1/2)*dh]
        hip = addboxx(sim, root, dims, pos)
        hip.setRotation(agx.Quat( bot_tilt, agx.Vec3(1,0,0)))
        hip.setRotation(hip.getRotation()*agx.Quat(angle, agx.Vec3(0,0,1)))
        addboxx(sim, root, [2*dx*(width/14), 1.1*(width/14), dims[2]], [2*(width/14)-dx*(i+1/2)*(width/14), -4.7*(width/14)-1.8*((-1)**i)*(width/14), -0.3+h+(i+1)*dh])
    
    # Bridge boxes
    dims = [1.5*(width/14), 1.8*(width/14), 0.45*(width/14)]
    pos = [-1.5*(width/14), -3.25*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)

    dims = [1.5*(width/14), 1.8*(width/14), 0.45*(width/14)]
    pos = [-4.5*(width/14), -3.25*(width/14), h+dims[2]/2]
    addboxx(sim, root, dims, pos)
    
    # Bridge part
    bridge = addboxx(sim, root, [1.5*(width/14), 0.5*(width/14), 0.08], [-3.0*(width/14), -3.25*(width/14), h+0.45*(width/14)-0.04])
    timer.addCheckpoint(bridge)
    
    # Swinging ball over bridge
    rad = 0.4
    pendulum = addball(sim, root, rad, [-3.0*(width/14), -3.25*(width/14), h+0.45*(width/14)+rad+0.01], Fixed=False)
    pendulum.setVelocity(agx.Vec3(0,5,0))
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3( 1,0,0))
    hf.setCenter(agx.Vec3(-3.0*(width/14), -3.25*(width/14), 3.0 + h+0.45+rad+0.01))
    axleP = agx.Hinge(hf, pendulum)
    sim.add(axleP)
    # addboxx(sim, root, [1.5, 0.5, 0.08], )

    # final ramp
    addboxx(sim, root, [0.1*(width/14), 2.5*(width/14), 0.5*(width/14)], [-6.5*(width/14), -2.05*(width/14), h+0.5*(width/14)/2])
    addboxx(sim, root, [0.1*(width/14), 2.5*(width/14), 0.5*(width/14)], [-5.5*(width/14), -2.05*(width/14), h+0.5*(width/14)/2])

    hip = addboxx(sim, root, [0.9*(width/14), 1.5*(width/14), 0.1*(width/14)], [-6.0*(width/14), -1.53*(width/14), h+0.026*(width/14)+np.sin(0.15)*1.5/2])
    hip.setRotation(agx.Quat(0.15, agx.Vec3(1,0,0)))

    addboxx(sim, root, [0.9*(width/14), 2.0*(width/14), 0.2*(width/14)], [-6.0*(width/14), -2.25*(width/14), h+0.075*(width/14)])
    addboxx(sim, root, [1.4*(width/14), 0.8*(width/14), 0.2*(width/14)], [-5.8*(width/14), -3.7*(width/14), h+0.45*(width/14)-0.1])

    hip = addboxx(sim, root, [0.9*(width/14), 1.5*(width/14), 0.1*(width/14)], [-6.0*(width/14), -3.0*(width/14), h+0.026+np.sin(0.15)*1.5/2*(width/14)])
    hip.setRotation(agx.Quat(-0.15, agx.Vec3(1,0,0)))

    

def seesaw(sim, root, pos, angle, h=0.08):
    d = 0.8
    # Sides
    dims = [0.6*(width/14), 0.15*(width/14), h*3/2]
    pos_s = [pos[0]+(d/2+0.3)*np.cos(angle)*(width/14), pos[1]+(d/2+0.3)*np.sin(angle)*(width/14), pos[2]+h/2]
    sideP = addboxx(sim, root, dims, pos_s)
    dims = [0.6*(width/14), 0.15*(width/14), h*3/2]
    pos_s = [pos[0]-(d/2+0.3)*np.cos(angle)*(width/14), pos[1]-(d/2+0.3)*np.sin(angle)*(width/14), pos[2]+h/2]
    sideN = addboxx(sim, root, dims, pos_s)
    # Main board
    dims = [d*(width/14), 0.9*(width/14), 0.004]
    pos_s = [pos[0]+0.06*np.sin(angle)*(width/14), pos[1]-0.06*np.cos(angle)*(width/14), pos[2]+h]
    board = addboxx(sim, root, dims, pos_s, Fixed=False)

    sideP.setRotation(agx.Quat(angle, agx.Vec3(0,0,1)))
    sideN.setRotation(agx.Quat(angle, agx.Vec3(0,0,1)))
    board.setRotation(agx.Quat(angle, agx.Vec3(0,0,1)))

    #Some stops under
    bot_tilt = 0.17
    dims = [d, 0.43, 0.004]
    dif = 0.215*np.cos(bot_tilt)*(width/14)-0.002*np.sin(bot_tilt)*(width/14)
    pos_s = [pos[0]+(0.06+dif)*np.sin(angle)*(width/14), pos[1]-(0.06+dif)*np.cos(angle)*(width/14), pos[2]+np.sin(bot_tilt)*dif]
    bottom1 = addboxx(sim, root, dims, pos_s, color=agxRender.Color.DarkGray())
    pos_s = [pos[0]+(0.06-dif)*np.sin(angle)*(width/14), pos[1]-(0.06-dif)*np.cos(angle)*(width/14), pos[2]+np.sin(bot_tilt)*dif]
    bottom2 = addboxx(sim, root, dims, pos_s, color=agxRender.Color.DarkGray())

    
    bottom1.setRotation(agx.Quat( bot_tilt, agx.Vec3(1,0,0)))
    bottom1.setRotation(bottom1.getRotation()*agx.Quat(angle, agx.Vec3(0,0,1)))
    
    bottom2.setRotation(agx.Quat(-bot_tilt, agx.Vec3(1,0,0)))
    bottom2.setRotation(bottom2.getRotation()*agx.Quat(angle, agx.Vec3(0,0,1)))
    

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3( np.cos(angle),np.sin(angle),0))
    hf.setCenter(agx.Vec3(pos[0]+(d/2)*np.cos(angle)*(width/14), pos[1]+(d/2)*np.sin(angle)*(width/14), pos[2]+h))
    axleP = agx.Hinge(hf, board, sideP)
    sim.add(axleP)

    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3(  np.cos(angle),np.sin(angle),0))
    hf.setCenter(agx.Vec3(pos[0]*(width/14)-(d/2)*np.cos(angle)*(width/14), pos[1]*(width/14)-(d/2)*np.sin(angle)*(width/14), pos[2]+h))
    axleN = agx.Hinge(hf, board, sideN)
    sim.add(axleN)



    

def addboxx(sim, root, dims, pos, Fixed=True, color = agxRender.Color.Red()):
    if type(pos) == type([]):
        pos = agx.Vec3(pos[0], pos[1], pos[2])
    boxx = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(dims[0]/2, dims[1]/2, dims[2]/2)))
    boxx.setPosition(pos)
    if(Fixed):
        boxx.setMotionControl(1)
    sim.add(boxx)
    agxOSG.setDiffuseColor(agxOSG.createVisual(boxx, root), color)
    return boxx

def addcylinder(sim, root, dims, pos, Fixed=True, color = agxRender.Color.Red(), texture=False):
    if type(pos) == type([]):
        pos = agx.Vec3(pos[0], pos[1], pos[2])
    cyl = agx.RigidBody( agxCollide.Geometry( agxCollide.Cylinder(dims[0], dims[1])))
    cyl.setPosition(pos)
    if(Fixed):
        cyl.setMotionControl(1)
    sim.add(cyl)
    vis_body = agxOSG.createVisual(cyl, root)
    if texture:
        agxOSG.setTexture(vis_body, texture, True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    else:
        agxOSG.setDiffuseColor(vis_body, color)
    
    return cyl

def addball(sim, root, rad, pos, Fixed=True):
    if type(pos) == type([]):
        pos = agx.Vec3(pos[0], pos[1], pos[2])
    ball = agx.RigidBody( agxCollide.Geometry( agxCollide.Sphere(rad)))
    ball.setPosition(pos)
    if(Fixed):
        ball.setMotionControl(1)
    sim.add(ball)
    agxOSG.setDiffuseColor(agxOSG.createVisual(ball, root), agxRender.Color.Red())
    return ball

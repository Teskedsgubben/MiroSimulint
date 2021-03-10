#------------------------------------------------------
#
# Some sort of Robotcourse for the peeps to combat eachother 
#
# Currently under verry much development, grab some coffe or other beverage and get to work!
#
# Authors:      Felix Djuphammar, Philip Beckman
#
#------------------------------------------------------

from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses.MiroAPI_agx import agxVecify as agxVec
import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

import sys

try:
    import agx
except:
    print("Could not import AGX to run Robotcourse_local")

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

# Global course paramters
width = 8
height = 0.6

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
    
    floor = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(arena_size[0]/2, arena_size[1]/2, arena_size[2]/2)))
    floor.setPosition(arena_pos[0], arena_pos[1], arena_pos[2]-arena_size[2]/2)
    floor.setMotionControl(1)
    sim.add(floor)
    agxOSG.setDiffuseColor(agxOSG.createVisual(floor, root), agxRender.Color.Gray())

    sides = 8
    side_len = width/(1+np.sqrt(2)) + arena_size[2]/2/np.sqrt(2)
    base_pos = agx.Vec3(arena_pos[0], arena_pos[1], arena_pos[2]-arena_size[2]/2+height/2)
    for w in range(sides):
            theta = -w*np.pi/4
            rot = agx.Quat(theta, agx.Vec3(0,0,1))
            rot_pos = agx.Vec3(np.sin(theta)*width/2, -np.cos(theta)*width/2, 0)

            wall = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(side_len/2, arena_size[2]/2, height/2)))
            wall.setPosition(base_pos + rot_pos)
            wall.setMotionControl(1)
            wall.setRotation(rot)
            sim.add(wall)
            agxOSG.setDiffuseColor(agxOSG.createVisual(wall, root), agxRender.Color.DarkGray())

    obstacles(sim, root, arena_pos[2])

def obstacles(sim, root, height):
    #--------------------------------
    # Central stuff like walls and tower and stuff
    #---------------------------------
    #Start plattform
    dims = [1.5*(width/14), 1.5*(width/14), 0.06]
    pos = [-3.5*(width/14), 0, height+0.405]
    startbox = addboxx(sim, root, dims, pos)
    #Pole in the middle
    dims = [0.28*(width/14), 1.4*(width/14)]
    pos = [0, 0, height+dims[1]/2+0.3]
    can = addcylinder(sim, root, dims, pos, texture='textures/schrodbull.png')
    can.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
    #Lidd
    pos = [0, 0, height+dims[1]+0.3]
    dims = [0.28*(width/14), 0.025*(width/14)]
    pos[2] = pos[2] + dims[1]/2
    lid = addcylinder(sim, root, dims, pos, texture='textures/sodacan_lid.png')
    lid.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
    #West Wall
    dims = [7.0*(width/14), 0.3*(width/14) ,0.4]
    pos = [-3.5*(width/14), 0, height+dims[2]/2]
    addboxx(sim, root, dims, pos)
    #East Wall
    dims = [7.0*(width/14), 0.3*(width/14) ,0.4]
    pos = [+3.5*(width/14), 0, height+dims[2]/2]
    addboxx(sim, root, dims, pos)
    #South Wall
    dims = [0.3*(width/14), 7.0*(width/14), 0.4]
    pos = [0, -3.5*(width/14), height+dims[2]/2]
    addboxx(sim, root, dims, pos)
    #North wall
    dims = [0.3*(width/14), 7.0*(width/14), 0.4]
    pos = [0, 3.5*(width/14), height+dims[2]/2]
    addboxx(sim, root, dims, pos)

    #--------------
    #   Zone 1
    #--------------

    #Halfcircle track
    buildTurn(agx.Vec3(-3.4*(width/14), (width/224), height+0.4), sim, root)

    #Add water beneath track
        #Snacka med Felix ang detta
    #--------------
    #   Zone 2
    #--------------

    #Floor 
    dims = [6.8*(width/14), 6.8*(width/14), 0.06]
    pos = [3.5*(width/14), 3.5*(width/14), height+0.4]
    addboxx(sim, root, dims, pos)
    #Mountains and stuff via highmap?
        #Eventuellt att det finns kod för detta. Annars Felix
    #--------------
    #   Zone 3
    #--------------

    #Floor 
    dims = [6.8*(width/14), 6.8*(width/14), 0.06]
    pos = [3.5*(width/14),-3.5*(width/14), height+0.4]
    addboxx(sim, root, dims, pos)
    #Maze or other things via highmap? or just add all the walls?
        #Finns lite färdig kod från andra banan
    #--------------
    #   Zone 4
    #--------------

    #Halfcircle track
    buildTurn2(agx.Vec3(0.1*(width/14),-3.5*(width/14), height+0.4), sim, root)

    #Add the balls that knock you down
        #Finns färdig kod från andra banan

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

def buildTurn(ramp_pos, sim, root):    
    off_angle = np.pi/2
    parts = 25
    ramp_width = 1 
    ramp_length = 3 
    ramp_height = 0.06
    eps_x=-0.0
    eps_z=0.0
    part_pos = agx.Vec3(ramp_pos)
    for i in range(parts):
        ramp_dim = [ramp_width,ramp_length/parts, ramp_height]
        ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
        theta = -(i)/parts*off_angle
        part_pos = part_pos -  agx.Vec3(np.sin(theta)*ramp_dim[1]-eps_x, -np.cos(theta)*ramp_dim[1]-eps_z, 0)
        ramp.setPosition(part_pos) 
        ramp.setRotation(agx.Quat(theta - off_angle/parts/2, agx.Vec3(0,0,1)))
        ramp.setMotionControl(1)
        sim.add(ramp)
        agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.Red())

def buildTurn2(ramp_pos, sim, root):    
    off_angle = np.pi/2
    parts = 25
    ramp_width = 1 
    ramp_length = 3 
    ramp_height = 0.06
    eps_x=-0.0
    eps_z=0.0
    part_pos = agx.Vec3(ramp_pos)
    for i in range(parts):
        ramp_dim = [ramp_length/parts, ramp_width, ramp_height]
        ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
        theta = -(i)/parts*off_angle
        part_pos = part_pos -  agx.Vec3(np.cos(theta)*ramp_dim[0]-eps_x, np.sin(theta)*ramp_dim[0]-eps_z, 0)
        ramp.setPosition(part_pos)
        ramp.setRotation(agx.Quat(theta - off_angle/parts/2, agx.Vec3(0,0,1)))
        ramp.setMotionControl(1)
        sim.add(ramp)
        agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.Red())
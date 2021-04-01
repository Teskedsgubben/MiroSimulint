#------------------------------------------------------
#
# Some sort of Robotcourse for the peeps to combat eachother 
#
# Currently under verry much development, grab some coffe or other beverage and get to work!
#
# Authors:      Felix Djuphammar, Philip Beckman, Malin Rantala
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
import agxTerrain

import time as TIME
import math
import random

# Banans mått
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
    agxOSG.setDiffuseColor(agxOSG.createVisual(floor, root), agxRender.Color.Black())
    agxOSG.setShininess(agxOSG.createVisual(floor, root), 128)

    sides = 8
    side_len = width/(1+np.sqrt(2)) + arena_size[2]/2/np.sqrt(2)
    base_pos = agx.Vec3(arena_pos[0], arena_pos[1], arena_pos[2]-arena_size[2]/2+height/2)
    for w in [1, 2, 4, 5, 6, 7, 8]: # Build sides for an octagon, except the fourth in the iteration
            theta = -w*np.pi/4
            rot = agx.Quat(theta, agx.Vec3(0,0,1))
            rot_pos = agx.Vec3(np.sin(theta)*width/2, -np.cos(theta)*width/2, 0)

            wall = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(side_len/2, arena_size[2]/2, height/2)))
            wall.setPosition(base_pos + rot_pos)
            wall.setMotionControl(1)
            wall.setRotation(rot)
            sim.add(wall)
            agxOSG.setDiffuseColor(agxOSG.createVisual(wall, root), agxRender.Color.DarkOrange())
    # Build the remaining edge of the arena

    # Square corner 1 
    theta = -2*np.pi/4 
    rot = agx.Quat(theta, agx.Vec3(0,0,1))
    rot_pos = agx.Vec3(np.sin(theta)*width/2, -np.cos(theta)*width/2, 0)

    wall = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(side_len/2, arena_size[2]/2, height/2)))
    wall.setPosition(base_pos + rot_pos + agx.Vec3(0, side_len - 1, 0))
    wall.setMotionControl(1)
    wall.setRotation(rot)
    sim.add(wall)
    agxOSG.setDiffuseColor(agxOSG.createVisual(wall, root), agxRender.Color.DarkOrange())

    # Square corner 2
    theta = -4*np.pi/4  
    rot = agx.Quat(theta, agx.Vec3(0,0,1))
    rot_pos = agx.Vec3(np.sin(theta)*width/2, -np.cos(theta)*width/2, 0)

    wall = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(side_len/2, arena_size[2]/2, height/2)))
    wall.setPosition(base_pos + rot_pos + agx.Vec3(-(side_len - 1), 0, 0))
    wall.setMotionControl(1)
    wall.setRotation(rot)
    sim.add(wall)
    agxOSG.setDiffuseColor(agxOSG.createVisual(wall, root), agxRender.Color.DarkOrange())

    obstacles(sim, root, arena_pos[2])

def obstacles(sim, root, height):
    #--------------------------------
    # Central stuff like walls and tower and stuff
    #---------------------------------
   
    addVolcano(sim, root)
    createLava(sim, root)
   
    # #Sodacan in the middle
    # dims = [0.28*(width/14), 1.4*(width/14)]
    # pos = [0, 0, height+dims[1]/2+0.3]
    # can = addcylinder(sim, root, dims, pos, texture='textures/schrodbull.png')
    # can.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))
    
    # #Lid for sodacan
    # pos = [0, 0, height+dims[1]+0.3]
    # dims = [0.28*(width/14), 0.025*(width/14)]
    # pos[2] = pos[2] + dims[1]/2
    # lid = addcylinder(sim, root, dims, pos, texture='textures/sodacan_lid.png')
    # lid.setRotation(agx.Quat(np.pi/2, agx.Vec3(1,0,0)))

    # Texture: white_bricks.jpg
    wallHeight = 0.12
    #West Wall
    dims = [7.0*(width/14), 0.3*(width/14) ,wallHeight]
    pos = [-3.5*(width/14), 0, height+dims[2]/2]
    addboxx(sim, root, dims, pos, texture='textures/stone.png')

    #East Walls
    dims = [1.0*(width/14), 0.3*(width/14) ,wallHeight + 0.4] # Added height for the heightmap
    pos = [3.8, 0, height+dims[2]/2]
    addboxx(sim, root, dims, pos, texture='textures/stone.png')

    dims = [4.0*(width/14), 0.3*(width/14) ,wallHeight + 0.4]
    pos = [+2.5*(width/14), 0, height+dims[2]/2]
    addboxx(sim, root, dims, pos, texture='textures/stone.png')

    #South Wall
    dims = [0.3*(width/14), 7.0*(width/14), wallHeight]
    pos = [0, -3.5*(width/14), height+dims[2]/2]
    addboxx(sim, root, dims, pos, texture='textures/stone.png')

    #North wall
    #dims = [0.3*(width/14), 7.0*(width/14), 0.2]
    #pos = [0, 3.5*(width/14), height+dims[2]/2]
    #addboxx(sim, root, dims, pos)

    #-------------- Zone 1 --------------
    # BIG JUMP
    buildRamp(agx.Vec3(-1.2,2.1,height), sim, root)
    
    # Ramp to bridge
    ramp_dim = [1, 2, wallHeight+0.14] # *np.cos(np.pi/4)
    ramp_pos = agx.Vec3(-3.2,1.31,0)
    ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
    theta = -np.arcsin(ramp_dim[2]/ramp_dim[0])/2
    ramp.setPosition(ramp_pos) # +arena_size[1]/2-ramp_dim[1]/2
    ramp.setRotation(agx.Quat(theta, agx.Vec3(1,0,0)))
    ramp.setMotionControl(1)
    sim.add(ramp)
    agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.DarkOrange())

    #Startbox
    dims = [1, 0.5, 0.06]
    pos = [-3.2, 0.115, height+wallHeight+0.02]
    startbox = addboxx(sim, root, dims, pos, texture='textures/arenatextures/start.png')

    #-------------- Zone 2 --------------
    addField(sim, root)

    #-------------- Zone 3 --------------
    
    for i in range(15):
        x = 6*(width/14) - random.random()*5*(width/14)
        y = -6*(width/14) + random.random()*6*(width/14)
        dims = [random.random()*0.5*(width/14), random.random()*0.5*(width/14), random.random()*1.2*(width/14)]
        pos = agx.Vec3(x, y, 0)
        if pos.length() < 1.5*(width/14):
            pos.setLength(1.5*(width/14)+random.random()*5*(width/14))
        if pos.length() > 7.0*(width/14):
            pos.setLength(1.5*(width/14)+random.random()*5*(width/14))
        pos.set(height+dims[2]/2, 2)
        addboxx(sim, root, dims, pos, texture = 'textures/arenatextures/windows.png')



    # Ramp to bridge
    ramp_dim = [2, 1, wallHeight+0.24] # *np.cos(np.pi/4)
    ramp_pos = agx.Vec3(1, -3.305 ,0)
    ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
    theta = -np.arcsin(ramp_dim[2]/ramp_dim[0])/2
    ramp.setPosition(ramp_pos) # +arena_size[1]/2-ramp_dim[1]/2
    ramp.setRotation(agx.Quat(theta, agx.Vec3(0,-1,0)))
    ramp.setMotionControl(1)
    sim.add(ramp)
    agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.DarkOrange())

    #Startbox
    dims = [0.2, 1, 0.06]
    pos = [-0.05, -3.305, height+wallHeight+0.02]
    addboxx(sim, root, dims, pos, texture='textures/arenatextures/plankis.png')

    #--------------
    #   Zone 4
    #--------------

    #Halfcircle track
    buildTurn2(agx.Vec3(0.1*(width/14),-5.8*(width/14), height+wallHeight+0.02), sim, root)

    # Swinging ball over bridge
    rad = 0.4
    pendulum = addball(sim, root, rad, [-2.0*(width/14), -2.25*(width/14), height+0.4+0.45*(width/14)+rad+0.01], Fixed=False)
    pendulum.setVelocity(agx.Vec3(0,4,0))
    hf = agx.HingeFrame()
    hf.setAxis(agx.Vec3( 1,-1,0))
    hf.setCenter(agx.Vec3(-3.5*(width/14), -3.5*(width/14), 3.0 + height+0.45+rad+0.01))
    axleP = agx.Hinge(hf, pendulum)
    sim.add(axleP)
    # addboxx(sim, root, [1.5, 0.5, 0.08], )

    createPond(sim, root)

def create_water_visual(geo, root):
    node = agxOSG.createVisual(geo, root)

    diffuse_color = agxRender.Color.Red()
    ambient_color = agxRender.Color.Orange()
    specular_color = agxRender.Color.Red()
    agxOSG.setDiffuseColor(node, diffuse_color)
    agxOSG.setAmbientColor(node, ambient_color)
    agxOSG.setSpecularColor(node, specular_color)
    agxOSG.setShininess(node, 128)
    agxOSG.setAlpha(node, 0.999)
    
    agxOSG.setTexture(agxOSG.createVisual(geo, root), 'textures/arenatextures/lava.png', True, agxOSG.DIFFUSE_TEXTURE, 20, 20)
    return node

def createPond(sim, root):
    # water_material = agx.Material("waterMaterial")
    # water_material.getBulkMaterial().setDensity(4025)
    
    # water = agxCollide.Geometry(agxCollide.Box(2, 2, 0.15))
    # water.setMaterial(water_material)
    # water.setPosition(agxVec([2, 0, 2]))
    # sim.add(water)
    
    # controller = agxModel.WindAndWaterController()
    # controller.addWater(water)
    # create_water_visual(water, root)
    # sim.add(controller)
    
    water_material = agx.Material("waterMaterial")
    water_material.getBulkMaterial().setDensity(4025)

    hf = agxCollide.HeightField.createFromFile("textures/arenatextures/lavapond.png", 4, 3.9, 0, 0.15)

    water = agxCollide.Geometry(hf)
    water.setMaterial(water_material)
    water.setPosition(agxVec([1.9, 0, 1.9]))
    sim.add(water)
    
    controller = agxModel.WindAndWaterController()
    controller.addWater(water)
    create_water_visual(water, root)
    sim.add(controller)


def addboxx(sim, root, dims, pos, Fixed=True, color = agxRender.Color.Red(), texture=False):
    if type(pos) == type([]):
        pos = agx.Vec3(pos[0], pos[1], pos[2])
    boxx = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(dims[0]/2, dims[1]/2, dims[2]/2)))
    boxx.setPosition(pos)
    if(Fixed):
        boxx.setMotionControl(1)
    sim.add(boxx)
    vis_body = agxOSG.createVisual(boxx, root)
    if texture:
        agxOSG.setTexture(vis_body, texture, True, agxOSG.DIFFUSE_TEXTURE, 1.0, 1.0)
    else:
        agxOSG.setDiffuseColor(vis_body, color)
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
    # agxOSG.setDiffuseColor(agxOSG.createVisual(ball, root), agxRender.Color.Black())
    agxOSG.setTexture(agxOSG.createVisual(ball , root), 'textures_lowres/eyeball.png', True, agxOSG.DIFFUSE_TEXTURE, 1, 1)
    return ball

def buildTurn2(ramp_pos, sim, root):    
    off_angle = np.pi/2
    parts = 40
    ramp_width = 1 
    ramp_length = 5
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
        agxOSG.setTexture(agxOSG.createVisual(ramp, root), 'textures/arenatextures/plankis.png', True, agxOSG.DIFFUSE_TEXTURE, 1, 2)


def buildRamp(ramp_pos, sim, root):    
    off_angle = np.pi/6.5
    parts = 10
    ramp_length = 1.2
    ramp_height = 2
    ramp_width = 3.9
    ramp_pos = ramp_pos - agx.Vec3(0,0,ramp_height/2)
    eps_x=-0.0
    eps_z=0.0
    part_pos = agx.Vec3(ramp_pos)
    for i in range(parts):
        ramp_dim = [ramp_length/parts,ramp_width, ramp_height] # *np.cos(np.pi/4)
        ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
        theta = -(i)/parts*off_angle
        part_pos = part_pos - agx.Vec3(-np.cos(theta)*ramp_dim[0]-eps_x, 0, np.sin(theta)*ramp_dim[0]-eps_z)
        ramp.setPosition(part_pos) # +arena_size[1]/2-ramp_dim[1]/2
        ramp.setRotation(agx.Quat(theta - off_angle/parts/2, agx.Vec3(0,1,0)))
        ramp.setMotionControl(1)
        sim.add(ramp)
        # agxOSG.setTexture(agxOSG.createVisual(ramp, root), 'textures/arenatextures/plankis.png', True, agxOSG.DIFFUSE_TEXTURE, 5, 5)
        agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.Black())
    
    ramp_dim = [0.6,ramp_width, ramp_height] # *np.cos(np.pi/4)
    ramp = agx.RigidBody( agxCollide.Geometry( agxCollide.Box(ramp_dim[0]/2, ramp_dim[1]/2, ramp_dim[2]/2)))
    theta = -off_angle
    part_pos = part_pos - agx.Vec3(-np.cos(theta)*ramp_dim[0]-eps_x, 0, np.sin(theta)*ramp_dim[0]-eps_z)/2
    ramp.setPosition(part_pos) # +arena_size[1]/2-ramp_dim[1]/2
    ramp.setRotation(agx.Quat(theta - off_angle/parts/2, agx.Vec3(0,1,0)))
    ramp.setMotionControl(1)
    sim.add(ramp)
    # agxOSG.setTexture(agxOSG.createVisual(ramp, root), 'textures/arenatextures/plankis.png', True, agxOSG.DIFFUSE_TEXTURE, 5, 5)
    agxOSG.setDiffuseColor(agxOSG.createVisual(ramp, root), agxRender.Color.Black())

def addField(sim, root):
    # Create the ground
    ground_material = agx.Material("Ground")

    # Create the height field from a heightmap
    hf = agxCollide.HeightField.createFromFile("textures/arenatextures/heightmaptest2.png", 3.9, 3.8, 0.05, 0.5)

    ground_geometry = agxCollide.Geometry(hf)
    ground = agx.RigidBody(ground_geometry)
    ground.setPosition(agxVec([-1.95, 0, -1.95]))
    ground.setMotionControl(agx.RigidBody.STATIC)
    # ground.setMaterial(agx.Material("groundmaterial"))
    node = agxOSG.createVisual( ground, root )
    agxOSG.setShininess(node, 5)

    # Add a visual texture.
    agxOSG.setTexture(node, "textures/stone.png", True, agxOSG.DIFFUSE_TEXTURE, 1, 1)
    sim.add(ground)

    ####
    #wheelMaterial = agx.Material("wheelmaterial")
    #sim.add(shovelMaterial)
    # ... set the shovel material on the shovel bodies
    #terrainMaterial = terrain.getMaterial( agxTerrain.Terrain.MaterialType.TERRAIN )
    #wheelTerrainCM = agx.ContactMaterial( wheelMaterial, terrainMaterial )
    
    #wheelTerrainCM.setFrictionCoefficient( 0.4 )
    #wheelTerrainCM.setYoungsModulus( 1e8 )
    #wheelTerrainCM.setRestitution( 0.0 )
    #wheelTerrainCM.setAdhesion( 0, 0 )
    #sim.add(wheelTerrainCM)

def addVolcano(sim, root):
    # Create the ground
    ground_material = agx.Material("Ground")

    # Create the height field from a heightmap
    hf = agxCollide.HeightField.createFromFile("textures/arenatextures/volcano.png", 2, 2, 0, 1.3)

    ground_geometry = agxCollide.Geometry(hf)
    ground = agx.RigidBody(ground_geometry)
    ground.setPosition(agxVec([0, 0, 0.4]))
    ground.setMotionControl(agx.RigidBody.STATIC)
    # ground.setMaterial(agx.Material("groundmaterial"))
    node = agxOSG.createVisual( ground, root )
    agxOSG.setShininess(node, 5)

    # Add a visual texture.
    agxOSG.setTexture(node, "textures/stone.png", True, agxOSG.DIFFUSE_TEXTURE, 7, 7)
    sim.add(ground)

def createLava(sim, root):
    water_material = agx.Material("waterMaterial")
    water_material.getBulkMaterial().setDensity(4025)

    hf = agxCollide.HeightField.createFromFile("textures/arenatextures/lavariver.png", 1.99, 2, 0, 1.323)

    water = agxCollide.Geometry(hf)
    water.setMaterial(water_material)
    water.setPosition(agxVec([0, 0, 0.41]))
    sim.add(water)
    
    controller = agxModel.WindAndWaterController()
    controller.addWater(water)
    create_water_visual(water, root)
    sim.add(controller)

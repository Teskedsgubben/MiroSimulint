from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

from src import MIT_Walls
from src import MIT_Stage
from src import MIT_Tables
from src import MIT_Entrance
from src import MIT_Props
from src import MIT_CSplan4

try:
    from src import Robotcourse
except:
    print('Robotcourse is only currently available in AGX')

def build_MIT(MiroSystem, SPEEDMODE = False):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    MIT_Walls.build(MiroSystem, SPEEDMODE)
    MIT_Stage.build(MiroSystem, SPEEDMODE)
    MIT_Tables.build(MiroSystem, SPEEDMODE)
    MIT_Entrance.build(MiroSystem, SPEEDMODE)
    MIT_CSplan4.build(MiroSystem, SPEEDMODE)

    if MiroAPI.API == 'AGX':
        Robotcourse.buildArena([0,0,0.02])

    mit_carpet_floor(MiroSystem)
    # roof(MiroSystem)
    if not SPEEDMODE:
        MIT_Props.AddProps(MiroSystem)

def mit_carpet_floor(MiroSystem):
    # Add MIT floor as a box
    MIT_floor_x = 4.5 + 4.8 + 4.5
    MIT_floor_z = 4.5 + 4.8 + 4.5
    MIT_floor_pos = np.array([1.6, -1, -1.9])

    MiroAPI.add_boxShape(MiroSystem, MIT_floor_x, 2, MIT_floor_z, MIT_floor_pos, 'MITfloor.png',scale=[23,18])

def roof(MiroSystem):
    frame_h = 1.0
    dy = 2/3
    xspan = [-5.25, 8.35]
    yspan = [9.96, 13.96]
    zspan = [-8.9, 5.1]

    dec = -(yspan[1]-yspan[0]-frame_h)/(zspan[1]-zspan[0])
    dy = yspan[1]-yspan[0]-frame_h
    #sides
    p1 = np.array([-dy/2, 0, 0])
    p2 = np.array([0.16+dy/2, 0, 0])
    d1 = np.array([0, 0,-1])
    d2 = np.array([dec,0,-1])
    s = 0.98
    sideS = MiroAPI.stepShape(p1,d1, p2,d2, zspan[1]-zspan[0], 0.2, [s,s,s])
    sideN = MiroAPI.stepShape(p1,d1, p2,d2, zspan[1]-zspan[0], 0.2, [s,s,s])
    MiroAPI.rotateBody(sideS, rotZ=90)
    MiroAPI.rotateBody(sideN, rotZ=90)
    MiroAPI.MoveBodyTo(sideS, np.array([xspan[0]-0.05,  yspan[0]+frame_h + (yspan[1]-yspan[0]-frame_h)/2, zspan[1]+0.1]))
    MiroAPI.MoveBodyTo(sideN, np.array([xspan[1]+0.25,  yspan[0]+frame_h + (yspan[1]-yspan[0]-frame_h)/2, zspan[1]+0.1]))
    MiroSystem.Add(sideS)
    MiroSystem.Add(sideN)

    beams = 4
    dx = (xspan[1] - xspan[0])/(beams-1)
    for b in range(beams):
        p1 = np.array([xspan[0] + dx*b - 0.06, yspan[1]-0.12, zspan[1]-0.06])
        p2 = np.array([xspan[0] + dx*b + 0.06, yspan[1]-0.12, zspan[1]-0.06])
        d1 = np.array([0,dec,-1])
        d2 = np.array([0,dec,-1])
        MiroAPI.add_stepShape(MiroSystem, p1,d1, p2,d2, (zspan[1]-zspan[0])*(np.sqrt(1+dec**2)), 0.2)
    
    beams = 10
    dx = (xspan[1] - xspan[0])/(beams-1)
    for b in range(beams):
        pos = np.array([xspan[0] + dx*b, (yspan[1] + yspan[0] + frame_h)/2, zspan[1]])
        MiroAPI.add_boxShapeHemi(MiroSystem, 0.05, (yspan[1] - yspan[0] - frame_h)/2, 0.05, pos, 'white_smere.jpg', scale=[100, 1.5])

    beams = 5
    dy = (yspan[1]-yspan[0]-frame_h)/(beams-1)
    for b in range(beams):
        pos = np.array([(xspan[0]+xspan[1])/2, yspan[0]+frame_h+0.06+dy*b, zspan[1]])
        MiroAPI.add_boxShapeHemi(MiroSystem, (xspan[1]-xspan[0])/2+0.06, 0.06, 0.06, pos, 'white_smere.jpg', scale=[100, 1.5])


    beams = 5
    h_0 = yspan[1]+0.12*dec
    dz = (zspan[1]-zspan[0])/(beams-1) - 0.28/beams
    for b in range(beams):
        pos = np.array([(xspan[0]+xspan[1])/2, h_0+dec*dz*b, zspan[1]-0.12-dz*b])
        MiroAPI.add_boxShapeHemi(MiroSystem, (xspan[1]-xspan[0])/2+0.06, 0.06, 0.06, pos, 'white_smere.jpg', rotX=np.sin(dec), scale=[100, 1.5])

    # West wall
    pos = np.array([(xspan[0]+xspan[1])/2, yspan[0]+frame_h/2, zspan[1]])
    MiroAPI.add_boxShapeHemi(MiroSystem, (xspan[1]-xspan[0]+0.5)/2, frame_h/2, 0.1, pos, 'white concrete.jpg', scale=[40, 5])

    # East wall
    pos = np.array([(xspan[0]+xspan[1])/2, yspan[0]+frame_h/2, zspan[0]])
    MiroAPI.add_boxShapeHemi(MiroSystem, (xspan[1]-xspan[0]+0.5)/2, frame_h/2, 0.1, pos, 'white concrete.jpg', scale=[40, 5])

    # South wall
    pos = np.array([xspan[0]-0.15,yspan[0]+frame_h/2,(zspan[1]+zspan[0])/2])
    MiroAPI.add_boxShapeHemi(MiroSystem, 0.1, frame_h/2, (zspan[1]-zspan[0])/2-0.1, pos, 'white concrete.jpg', scale=[40, 5])
    
    # North wall
    pos = np.array([xspan[1]+0.15,yspan[0]+frame_h/2,(zspan[1]+zspan[0])/2])
    MiroAPI.add_boxShapeHemi(MiroSystem, 0.1, frame_h/2, (zspan[1]-zspan[0])/2-0.1, pos, 'white concrete.jpg', scale=[40, 5])

    # MA roof
    roofMA_width = 6.6
    pos = np.array([xspan[1] + roofMA_width/2 + 0.052, yspan[0]+0.098, -0.2])
    MiroAPI.add_boxShapeHemi(MiroSystem, roofMA_width/2, 0.1, 12.5, pos, 'white concrete.jpg', scale=[40, 80])
    
    # MC roof
    roofMC_width = 3.165
    pos = np.array([(xspan[1]+xspan[0])/2,yspan[0]+0.098,zspan[1]+roofMC_width/2+0.1])
    MiroAPI.add_boxShapeHemi(MiroSystem, (xspan[1]-xspan[0])/2 + 0.052, 0.1, roofMC_width/2, pos, 'white concrete.jpg', scale=[80, 10])

    # Computer Science roof
    roofMC_width = 3.165
    pos = np.array([6.85,yspan[0]+0.098,zspan[1]+roofMC_width+2.092])
    MiroAPI.add_boxShapeHemi(MiroSystem, 1.552, 0.1, 1.992, pos, 'white concrete.jpg', scale=[80, 10])
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

from src import MIT_Walls
from src import MIT_Stage
from src import MIT_Tables
from src import MIT_Entrance
from src import MIT_Props
from src import MIT_Offices
from src import MIT_Roof
from src import Robotcourse_building
from src import Robotcourse

# Demotrack
# try:
#     from src import Robotcourse_local as Robotcourse
# except:
#     try:
#         from src import Robotcourse
#     except:
#         print('Robotcourse is only currently available in AGX')

# ---- CHOOSE YOUR COURSE ----

def build_MIT(MiroSystem, SPEEDMODE = False):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    MIT_Walls.build(MiroSystem, SPEEDMODE)
    MIT_Stage.build(MiroSystem, SPEEDMODE)
    MIT_Tables.build(MiroSystem, SPEEDMODE)
    MIT_Entrance.build(MiroSystem, SPEEDMODE)
    MIT_Offices.build(MiroSystem, SPEEDMODE)
    MIT_Roof.build(MiroSystem, SPEEDMODE)

    if MiroAPI.API == 'AGX':
        # CHOOSE YOUR COURSE HERE: Robotcouse is the democourse, Robotcourse_building is the main course.

        Robotcourse_building.buildArena(MiroSystem, [0,0,0])
        # Robotcourse.buildArena([0,0,0.1])

    mit_carpet_floor(MiroSystem)
    if not SPEEDMODE:
        mit_outside_ground(MiroSystem)
        MIT_Props.AddProps(MiroSystem)

def mit_carpet_floor(MiroSystem):
    # Add MIT floor as a box
    MIT_floor_x = 4.5 + 4.8 + 4.5
    MIT_floor_z = 4.5 + 4.8 + 4.5
    MIT_floor_pos = np.array([1.6, -1, -1.9])

    MiroAPI.add_boxShape(MiroSystem, MIT_floor_x, 2, MIT_floor_z, MIT_floor_pos, 'MITfloor.png',scale=[23,18])

def mit_outside_ground(MiroSystem):
    # Add a ground outside as a huge box
    MIT_ground_x = 1000
    MIT_ground_z = 80
    MIT_floor_pos = np.array([300, -1.15, 20])

    MiroAPI.add_boxShape(MiroSystem, MIT_ground_x, 2, MIT_ground_z, MIT_floor_pos, 'grey concrete.jpg',scale=[23,18])

    dims = [4, 0.6, 10]
    pos = [15, -0.15, 25]
    MiroAPI.add_boxShape(MiroSystem, dims[0], dims[1], dims[2], pos, rotX= 0*np.arcsin(dims[1]/dims[2]), rotZ= 1*np.arcsin(dims[1]/dims[0]), texture='grey concrete.jpg',scale=[23,18], rotDegrees=False)

    dims = [4, 0.6, 10]
    pos = [20, -0.15, 25]
    MiroAPI.add_boxShape(MiroSystem, dims[0], dims[1], dims[2], pos, rotX= 0*np.arcsin(dims[1]/dims[2]), rotZ= -1*np.arcsin(dims[1]/dims[0]), texture='grey concrete.jpg',scale=[23,18], rotDegrees=False)
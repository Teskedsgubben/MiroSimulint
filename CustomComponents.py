import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

from src import Components
from src import Sensors

# Custom Component Example, returns a component based on the MC0XX function with custom dimenstions
def MC0_Custom(rot = [0,0,0], pos = [0,0,0], Fixed = False):
    M1 = 0.30
    M2 = 0.30
    M3 = 0.03
    return Components.MC0XX(M1, M2, M3, rot, pos, Fixed)
    
# Custom Component Example, returns a component based on a .obj file
def KristerK(rot = [0,0,0], pos = [0,0,0], Fixed = False): 
    # Create blank MiroComponent
    CustomComponent = MC.MiroComponent()
    
    # Import .obj file from object_files directory and set color [R, G, B]
    CustomComponent.ImportObj('K.obj', color = [1, 0.2, 0.6])

    # Set collision as box if the import collision does not work properly.
    # Dimensions can be found when importing the .obj file for the first time
    # as it is the scaled and prints the dimensions. Calibrate the offset by 
    # running the code, press I and check "Draw Collision Shapes" and alter 
    # the offset until the collision box matches the object (close enough)
    Kx = 0.06
    Ky = 0.02
    Kz = 0.07
    CustomComponent.SetCollisionAsBox(0.06, 0.02, 0.07, offset = [-0.065, -0.01, 0.015])
    
    # Add linkpoints to enable connecting with other components
    CustomComponent.AddLinkPoint('A', [0, 1, 0], [0, Ky/2, 0])
    CustomComponent.AddLinkPoint('B', [0,-1, 0], [0,-Ky/2, 0])
    CustomComponent.AddLinkPoint('C', [0, 0,-1], [-Kx/3.5,0,-Kz/2])
    
    CustomComponent.Rotate(rot)
    CustomComponent.MoveToPosition(pos)

    return CustomComponent


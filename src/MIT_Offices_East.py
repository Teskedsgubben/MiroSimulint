from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

def build(MiroSystem, SPEEDMODE = False):
    Plan4_Rum3(MiroSystem)
    return

def Plan4_Rum3(MiroSystem):
    MiroAPI.add_boxShape(MiroSystem, 4, 0.85, 3, [-4.5, 6.64, -10.3], rotX=-16, friction=2000)
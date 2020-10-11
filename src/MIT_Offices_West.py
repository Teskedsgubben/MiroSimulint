from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

def build(MiroSystem, SPEEDMODE = False):
    MiroAPI.add_boxShape(MiroSystem, 0.5, 1.85, 0.5, [1, 6.64 + 1.85/2, 6], Fixed=False)
    return
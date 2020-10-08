import numpy as np

from MiroClasses import MiroModule as MM
from MiroClasses import MiroComponent as MC

def build(MiroSystem, SPEEDMODE = False):
    course_comp = MC.MiroComponent()
        
    # Import .obj file from object_files directory and set color [R, G, B]
    course_comp.ImportObj('Bana_robottavlingen.obj', color = [0.7, 0.7, 0.7])

    course_module = MM.Module()
    course_module.AddComponent(course_comp, 'Course Base')

    MiroSystem.Add_MiroModule(course_module, 'Course', [4,1,-4])
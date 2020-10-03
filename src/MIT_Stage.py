import numpy as np
import os

from MiroClasses import MiroAPI_chrono as MiroAPI
from src import Shapes as shp

def build(ChSystem, SPEEDMODE = False):
    stage(ChSystem)
    screen(ChSystem, SPEEDMODE)
    back_stage(ChSystem)

#coner position (-7.5,0,-11)
def stage(system): 
    theta_f = 0 
    theta_b = np.pi/2
    pos_f = np.array([-4.3, 0, -8.8])
    dir_f = np.array([np.cos(theta_f), 0, np.sin(theta_f)]) 
    pos_b = np.array([-5.3, 0, -7.8])
    dir_b = np.array([np.cos(theta_b), 0, np.sin(theta_b)])
    step = MiroAPI.stepShape(pos_f, dir_f, pos_b, dir_b, 3, 0.3, [0.02,0.02,0.02])
    system.Add(step)

def screen(system, SPEEDMODE = False):
    size_length = 4
    size_width = 0.01
    size_height = size_length/(4/3)

    # Screen
    grouplogo_file = '../GroupLogo_local.png'
    if not os.path.isfile('GroupLogo_local.png'):
        grouplogo_file = '../GroupLogo.png'
    alpha = np.pi/10
    beta = np.pi/4
    corner_pos = np.array([-5.3,3.55,-8.8])
    delta_tilt = np.array([np.sin(alpha)/np.sqrt(2), np.cos(alpha), np.sin(alpha)/np.sqrt(2)])*size_height/2
    screen_pos = corner_pos + np.array([1/np.sqrt(8),0, 1/np.sqrt(8)])*size_length + delta_tilt
    MiroAPI.add_boxShape(system, size_length, size_height, size_width, screen_pos, texture=grouplogo_file, scale=[-4,-3], rotX=alpha, rotY=beta, rotDegrees=False)

    # Top cylinder
    r = 0.08
    roll_pos = screen_pos + delta_tilt*((1.9*r+size_height)/size_height)
    MiroAPI.add_cylinderShape(system, 0.08, 4.15, 1000, roll_pos, texture=False, rotAngle=90, rotAxis=[1,0,1])

    if not SPEEDMODE:
        # Hanging bars
        bar_h = 0.05
        roller_mid = screen_pos + delta_tilt*((3.9*r+size_height)/size_height) + np.array([0,bar_h/2,0])
        dz = np.array([0, 0, 0.25])
        dx = np.array([0.25, 0, 0])

        offset = np.array([1/np.sqrt(2), 0, -1/np.sqrt(2)])*1.8
        MiroAPI.add_boxShape(system, bar_h, bar_h, 1.2, roller_mid + offset - dz, texture=False)
        MiroAPI.add_boxShape(system, 1.2, bar_h, bar_h, roller_mid - offset - dx, texture=False)

def back_stage(system):
    coner_pos = np.array([-5.3,1.55,-8.8]) # Real coner -5.3,1.25,-8.8
    length = 1.3
    in_screen_pos = coner_pos + np.array([1/np.sqrt(2),0, 1/np.sqrt(2)])*length

    size_len = 2.5
    size_width = 0.05
    size_height = 2.5

    MiroAPI.add_boxShape(system,size_len,size_height,size_width,in_screen_pos, texture='tf-logo.jpg', scale=[-4,-3], rotY=45)
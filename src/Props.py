from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

from MiroClasses import MiroNotifier as MN
from MiroClasses import MiroComponent as MC

def robotcourse(MiroSystem, target):
    course_comp = MC.MiroComponent()
        
    # Import .obj file from object_files directory and set color [R, G, B]
    course_comp.ImportObj('Bana_robottavlingen.obj', color = [0.7, 0.7, 0.7])

    course_comp.MoveToPosition([target[0], target[1], target[2]])

    MiroSystem.Add(course_comp.GetBody())

def dartboard(MiroSystem, target):
    h = 0.15
    eps = 0.0025
    size = 1
    pos_a = np.array([target[0], target[1]-eps, target[2]])
    pos_b = np.array([target[0], target[1]-(h+2*eps)/2, target[2]])
    
    # Create dartboard layer
    MiroAPI.add_cylinderShape(MiroSystem, size, eps, 1000, pos_a, 'target_dart.png', Collide=False, scale=[-1,1])

    # Create Hitbox
    MiroAPI.add_cylinderShape(MiroSystem, size, h, 1000, pos_b, 'black_smere.jpg', scale=[8,-1])

def trialsurface(MiroSystem, target):
    nx = 10
    dz = 1.4
    diag = 0.2
    eps = 0.008
    
    box_side = diag/np.sqrt(2)
    h = diag/2

    for i in range(nx):
        pos = np.array([target[0] - (nx - 1 - 2*i)*diag/2, target[1]-h, target[2]])
        MiroAPI.add_boxShape(MiroSystem, box_side, box_side, dz, pos, rotZ=45, texture='white concrete.jpg')

    th = 1.2*h
    pos = np.array([target[0], target[1]-h-th/2, target[2]])
    MiroAPI.add_boxShape(MiroSystem, nx*diag+2*eps, th, dz+2*eps, pos, texture='wood_ikea_style.png')

    r = 0.03
    h = target[1]-th-h
    d = 0.1
    # [+, +]
    pos = np.array([target[0] + nx*diag/2 - d, h/2, target[2] + dz/2 -d])
    MiroAPI.add_cylinderShape(MiroSystem, r, h, 2500, pos, 'chrome.png', scale=[2,2])

    # [-, +]
    pos = np.array([target[0] - nx*diag/2 + d, h/2, target[2] + dz/2 -d])
    MiroAPI.add_cylinderShape(MiroSystem, r, h, 2500, pos, 'chrome.png', scale=[2,2])

    # [-, -]
    pos = np.array([target[0] - nx*diag/2 + d, h/2, target[2] - dz/2 +d])
    MiroAPI.add_cylinderShape(MiroSystem, r, h, 2500, pos, 'chrome.png', scale=[2,2])

    # [+, -]
    pos = np.array([target[0] + nx*diag/2 - d, h/2, target[2] - dz/2 +d])
    MiroAPI.add_cylinderShape(MiroSystem, r, h, 2500, pos, 'chrome.png', scale=[2,2])    
    

def sodacan(MiroSystem, target, text = 'schrodbull.png', angle = 0, SPEEDMODE = False):
    h = 0.22
    r = 0.04
    eps = 0.003
    epsvec = np.array([0, eps/2, 0])
    
    pos_can = np.array([target[0], target[1]+h/2+eps, target[2]])

    # Create Can Hitbox
    can = MiroAPI.add_cylinderShape(MiroSystem, r, h, 50, pos_can, rotY=angle, texture=text, Fixed=False, scale=[1,-1])

    # Create lid and bottom
    pos_lid = np.array([target[0], target[1]+eps*3/2+h, target[2]])
    lid = MiroAPI.add_cylinderShape(MiroSystem, r, eps, 150, pos_lid, rotY=angle, texture='sodacan_lid.png', Fixed=False, scale=[1,1])
    
    pos_bot = np.array([target[0], target[1]+eps/2, target[2]])
    bot = MiroAPI.add_cylinderShape(MiroSystem, r, eps, 200, pos_bot, rotY=angle, texture='sodacan_bot.png', Fixed=False, scale=[1,1])

    MiroSystem.Add(MiroAPI.LinkBodies_Hinge(can, lid, pos_lid-epsvec, [0, 1,0]))
    MiroSystem.Add(MiroAPI.LinkBodies_Hinge(can, bot, pos_bot+epsvec, [0,-1,0]))

def painting(MiroSystem, pos, text = 'DemoBengan.png', rot = 0, dims = [1, 0.6]):
    MiroAPI.add_boxShapeHemi(MiroSystem, dims[0], dims[1], 0.05, pos, rotY=rot, texture=text, Collide=False)

def pokeball(MiroSystem, pos, rot = 0):
    r = 0.05

    MiroAPI.add_sphereShape(MiroSystem, r, [pos[0], pos[1]+r, pos[2]], texture='pokeball.jpg', density = 100, Fixed=False, rotY=rot)

def eyeball(MiroSystem, pos, radius=0.1):
    MiroAPI.add_sphereShape(MiroSystem, radius, [pos[0], pos[1]+radius, pos[2]], texture='eyeball.png', density = 100, Fixed=False, rotY=-30)

def coin(MiroSystem, target, angle = 0):
    h = 0.0012
    r = 0.012
    
    pos_coin = np.array([target[0], target[1]+h/2, target[2]])
    MiroAPI.add_cylinderShape(MiroSystem, r, h, 150, pos_coin, rotY=angle, texture='gammal5kr.png', Fixed=False, scale=[1,-1])

def MIT_door(MiroSystem, pos, rot = 0):
    b = 1.0
    h = 2.1

    pos = [pos[0], pos[1]+h/2, pos[2]]
    MiroAPI.add_boxShape(MiroSystem, b, h, 0.16, pos, rotY=rot, texture='MIT_door.png', Collide=False)

def floorvent(MiroSystem, target, SPEEDMODE = False):
    h = 0.85
    r = 0.30

    h1 = 0.20
    h3 = 0.04
    h2 = h - h1 - h3
    
    pos_base = np.array([target[0], target[1]+h1/2, target[2]])
    pos_vent = np.array([target[0], target[1]+h2/2+h1, target[2]])
    pos_topp = np.array([target[0], target[1]+h3/2+h1+h2, target[2]])

    MiroAPI.add_cylinderShape(MiroSystem, r-0.02, h1, 1500, pos_base, texture='vents_surface.jpg')
    MiroAPI.add_cylinderShape(MiroSystem, r, h2, 1500, pos_vent, texture='vents.jpg')
    MiroAPI.add_cylinderShape(MiroSystem, r, h3, 1500, pos_topp, texture='vents_surface.jpg')

def UNbox(MiroSystem, pos, goal_nr, skew):
    pos[1] = pos[1]+0.2
    MiroAPI.add_boxShape(MiroSystem, 0.4, 0.4, 0.4, pos, density=8, rotY=skew, texture='UN_'+str(goal_nr)+'.png', Fixed=False)

def sponsorFlag(MiroSystem, pos, logo):
    foot_h = 0.08
    foot_r = 0.3
    leg_h = 0.4
    leg_r = 0.02
    sign_h = 1.7
    sign_w = 0.6
    sign_t = 0.06

    foot_pos = [pos[0], pos[1]+foot_h/2, pos[2]]
    leg_pos = [pos[0], pos[1]+foot_h+leg_h/2, pos[2]]
    sign_pos = [pos[0], pos[1]+foot_h+leg_h+sign_h/2, pos[2]]

    # Foot
    foot = MiroAPI.add_cylinderShape(MiroSystem, foot_r, foot_h, 1000, foot_pos, texture='gammal5kr.png', Fixed=False, scale=[1,-1])
    # Pole
    leg = MiroAPI.add_cylinderShape(MiroSystem, leg_r, leg_h, 500, leg_pos, texture='gammal5kr.png', Fixed=False, scale=[1,-1])
    # Sign
    sign = MiroAPI.add_boxShape(MiroSystem, sign_w, sign_h, sign_t, sign_pos, density=30, texture=logo, Fixed=False)
    # Hinges
    h1 = [pos[0], pos[1]+foot_h, pos[2]]
    h2 = [pos[0], pos[1]+foot_h+leg_h, pos[2]]
    MiroAPI.LinkBodies_Hinge(foot, leg, h1, [0,1,0], MiroSystem)
    MiroAPI.LinkBodies_Hinge(leg, sign, h2, [0,1,0], MiroSystem)

def measureBox(MiroSystem, pos, dims):
    pos = np.array(pos)
    d = 0.02
    lx = dims[0] + 2*d
    ly = dims[1] + d
    lz = dims[2]
    # Base
    MiroAPI.add_boxShape(MiroSystem, dims[0], d, dims[2], pos+np.array([0,d/2,0]), texture='wood_ikea_style.png')
    # x -
    MiroAPI.add_boxShape(MiroSystem, d, ly, lz, pos+np.array([-(dims[0]+d)/2, (dims[1]+d)/2, 0]), texture='wood_ikea_style.png')
    # x +
    MiroAPI.add_boxShape(MiroSystem, d, ly, lz, pos+np.array([ (dims[0]+d)/2, (dims[1]+d)/2, 0]), texture='wood_ikea_style.png')
    # z -
    MiroAPI.add_boxShape(MiroSystem, lx, ly, d, pos+np.array([ 0, (dims[1]+d)/2,-(dims[2]+d)/2]), texture='wood_ikea_style.png')
    # z +
    MiroAPI.add_boxShape(MiroSystem, lx, ly, d, pos+np.array([ 0, (dims[1]+d)/2, (dims[2]+d)/2]), texture='wood_ikea_style.png')
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

def build(MiroSystem, SPEEDMODE = False):
    pos_south = [1.7, 0, 12.16]
    pos_north = [8.67, 0, 12.16]
    if(SPEEDMODE):
        QuickEntrance(MiroSystem, pos_south, pos_north)
    else:
        FullEntrance(MiroSystem, pos_south, pos_north)
    
def QuickEntrance(MiroSystem, pos_south, pos_north):
    h = 3.1

    center = np.array([(pos_south[0]+pos_north[0])/2, (pos_south[1]+pos_north[1])/2 + h/2, (pos_south[2]+pos_north[2])/2])
    wid = np.abs(pos_south[0]-pos_north[0])

    # Door wall
    MiroAPI.add_boxShape(MiroSystem, wid/2, h/2, 0.05, center, texture='MITentrance_quick.png')
    
    # south wall
    p = np.array([pos_south[0]-0.05, 1.51, pos_south[2] -0.89/2])
    MiroAPI.add_boxShape(MiroSystem, 0.1, 3.02, 0.89, p, texture='MITentrance_quick.png')

def FullEntrance(MiroSystem, pos_south, pos_north):
    d = 0.08
    l = 3.02

    p = np.array([pos_south[0]+2.89, 1.51, pos_south[2]-0.6])
    MiroAPI.add_boxShape(MiroSystem, 2*d, l, 2*d, p, texture='white concrete.jpg', scale=[4, 12])

    p = np.array([pos_south[0]+2.89, 2.7, pos_south[2]-0.6-d-0.01])
    MiroAPI.add_boxShape(MiroSystem, 0.568*0.7, 0.285*0.7, 0.02, p, texture='exit.png')

    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+(1/2)*d, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+   0.68, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+   2.72, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+   3.06, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+   5.10, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+   5.44, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+   6.58, 1.51, pos_south[2]])
    greenpole(MiroSystem, d, l, 0, 0, [pos_north[0]-(1/2)*d, 1.51, pos_north[2]])

    
    greenpole(MiroSystem, d, (pos_north[0] - pos_south[0]), 0, 90, [(pos_north[0] + pos_south[0])/2, 2.5+d/2, pos_north[2]-d/20])
    greenpole(MiroSystem, d, (pos_north[0] - pos_south[0]), 0, 90, [(pos_north[0] + pos_south[0])/2, 3.0-d/2, pos_north[2]-d/20])

    # Small bits on floor
    for s in [[(1/2)*d, 0.68], [2.72, 3.06], [5.10, 5.44], [6.58, pos_north[0]-pos_south[0]-(1/2)*d]]:
        greenpole(MiroSystem, d, (s[1] - s[0] - d), 0, 90, [pos_south[0]+ (s[1] + s[0])/2, d/2, pos_north[2]])

    # Revolving door ground rings
    r = 0.98
    pos = np.array([pos_south[0]+1.70, 0, pos_south[2]])
    MiroAPI.add_cylinderShape(MiroSystem, r, 0.02, 1000, pos, 'MITentrance_floor.png', Collide=False)
    pos = np.array([pos_south[0]+4.08, 0, pos_south[2]])
    MiroAPI.add_cylinderShape(MiroSystem, r, 0.02, 1000, pos, 'MITentrance_floor.png', Collide=False)

    # Revolving door top rings
    pos = np.array([pos_south[0]+1.70, 2.45, pos_south[2]])
    MiroAPI.add_cylinderShape(MiroSystem, r, 0.1, 1000, pos, 'MITentrance.png')
    pos = np.array([pos_south[0]+4.08, 2.45, pos_south[2]])
    MiroAPI.add_cylinderShape(MiroSystem, r, 0.1, 1000, pos, 'MITentrance.png')
    
    # Revolving doors
    revolute_door(MiroSystem, d, 0.98, 15, [pos_south[0]+1.70, 2.4-d/2, pos_south[2]])
    revolute_door(MiroSystem, d, 0.98, 50, [pos_south[0]+4.08, 2.4-d/2, pos_south[2]])

    # Side door, inner
    normal_door(MiroSystem, d, 1.1-d, 192, [pos_south[0]+6.58-d, 2.5-d/2, pos_south[2]])

    ########### INNER PART STOPS HERE ###########
    width = pos_north[0] - pos_south[0] + 3.04
    depth = 5
    inner_depth = 2.8
    p = np.array([pos_south[0]-2+width/2, -0.08, pos_south[2] + depth/2])
    MiroAPI.add_boxShape(MiroSystem, width, 0.16, 5, p, 'stone_floor.jpg')
    p = np.array([p[0], 3.08, p[2]])
    MiroAPI.add_boxShape(MiroSystem, width, 0.16, 5, p, 'stone_floor.jpg')

    # Outer door frames
    z = pos_south[2]+inner_depth
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+0.00+d/2, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    0.33, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    1.51, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    1.59, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    2.77, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    3.25, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    4.43, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    4.51, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+    5.69, 1.51, z])
    greenpole(MiroSystem, d, l, 0, 0, [pos_south[0]+6.02-d/2, 1.51, z])

    # Outer doors
    normal_door(MiroSystem, d, 1.1-d, -15, [pos_south[0]+0.33+d, 2.5-d/2, z]) # south outward
    normal_door(MiroSystem, d, 1.1-d, 172, [pos_south[0]+2.77-d, 2.5-d/2, z]) # south inward

    normal_door(MiroSystem, d, 1.1-d,  -8, [pos_south[0]+3.25+d, 2.5-d/2, z]) # north outward
    normal_door(MiroSystem, d, 1.1-d, 161, [pos_south[0]+5.69-d, 2.5-d/2, z]) # north inward
    
    greenpole(MiroSystem, d, 6.02, 0, 90, [pos_south[0]+3.01, 2.5+d/2, z-d/20])
    greenpole(MiroSystem, d, 6.02, 0, 90, [pos_south[0]+3.01, 3.0-d/2, z-d/20])

    # Small bits on floor
    for s in [[d/2, 0.33], [2.77, 3.25], [5.69, 6.02-d/2]]:
        greenpole(MiroSystem, d, (s[1] - s[0] - d), 0, 90, [pos_south[0]+ (s[1] + s[0])/2, d/2, z])

    # south wall
    p = np.array([pos_south[0]-0.05, 1.51, pos_south[2] + inner_depth/2-0.89/2])
    MiroAPI.add_boxShape(MiroSystem, 0.1, 3.02, inner_depth+0.89, p, 'yellow_brick.jpg', scale=[7,9])

    # north wall
    np.array([pos_north[0]+0.05, 1.51, pos_south[2] + inner_depth/2])
    MiroAPI.add_boxShape(MiroSystem, 0.1, 3.02, inner_depth, p, 'yellow_brick.jpg', scale=[6,9])

    # WEST WALL
    w = 2
    dw = 0.96

    p = np.array([pos_north[0]+w/2-dw, 1.51, z])
    MiroAPI.add_boxShape(MiroSystem, w, 3.02, 0.16, p, 'yellow_brick.jpg', scale=[2,9])

    p = np.array([pos_south[0]-dw, 1.51, z])
    MiroAPI.add_boxShape(MiroSystem, w, 3.02, 0.16, p, 'yellow_brick.jpg', scale=[2,9])

    # Cement pillars outside
    r = 0.12
    p = np.array([pos_south[0]-1, 1.51, z - r + (depth-inner_depth)*(3/4)])
    MiroAPI.add_cylinderShape(MiroSystem, r, 3.02, 1000, p, 'white concrete.jpg')

    
    p = np.array([pos_north[0]+1-0.96, 1.51, z - r + (depth-inner_depth)*(3/4)])
    MiroAPI.add_cylinderShape(MiroSystem, r, 3.02, 1000, p, 'white concrete.jpg')
    
    p = np.array([pos_south[0]+1.6, 1.51, z - r + (depth-inner_depth)])
    MiroAPI.add_cylinderShape(MiroSystem, r, 3.02, 1000, p, 'white concrete.jpg')
    
    p = np.array([pos_north[0]-1.6-0.96, 1.51, z - r + (depth-inner_depth)])
    MiroAPI.add_cylinderShape(MiroSystem, r, 3.02, 1000, p, 'white concrete.jpg')

def greenpole(MiroSystem, d, l, spin, tilt, pos):
    p = np.array(pos)
    return MiroAPI.add_boxShape(MiroSystem, d, l, d, p, 'MITentrance.png', rotY=spin, rotZ=tilt, rotOrder=['z','y'], scale=[0.5,50])

def normal_door(MiroSystem, d, l, spin, pos):
    top = pos[1]
    mid = pos[1]/2+d/4
    bot = d/2
    # vertical frame poles
    pos[1] = mid
    greenpole(MiroSystem, d, top-bot+d, spin, 0, pos)
    p = [pos[0] + np.cos(np.deg2rad(spin))*(l-d/2), mid, pos[2] - np.sin(np.deg2rad(spin))*(l-d/2)]
    greenpole(MiroSystem, d, top-bot+d, spin, 0, p)

    # top and bottom frame
    p = [pos[0] + (1/2)*np.cos(np.deg2rad(spin))*(l-d/2), top, pos[2] - (1/2)*np.sin(np.deg2rad(spin))*(l-d/2)]
    greenpole(MiroSystem, d, l-d, spin, 90, p)
    p[1] = bot
    greenpole(MiroSystem, d, l-d, spin, 90, p)

    # handle
    r = 0.02
    h = 0.40
    dist = 0.30

    # poles through door
    pb = [pos[0] + np.cos(np.deg2rad(spin))*(l-d/2)*0.86, mid+h*(1/3), pos[2] - np.sin(np.deg2rad(spin))*(l-d/2)*0.86]
    MiroAPI.add_cylinderShape(MiroSystem, r/2, dist, 2500, pb, 'chrome.png', rotY=spin-90, rotZ=90, rotOrder=['z','y'], Collide=False, scale=[2,2])
    pb[1] = mid-h*(1/3)
    MiroAPI.add_cylinderShape(MiroSystem, r/2, dist, 2500, pb, 'chrome.png', rotY=spin-90, rotZ=90, rotOrder=['z','y'], Collide=False, scale=[2,2])
    
    # disks on door
    MiroAPI.add_cylinderShape(MiroSystem, r*1.2, 0.01, 2500, pb, 'brushsteel.png', rotY=spin-90, rotZ=90, rotOrder=['z','y'], Collide=False, scale=[2,2])
    pb[1] = mid+h*(1/3)
    MiroAPI.add_cylinderShape(MiroSystem, r*1.2, 0.01, 2500, pb, 'brushsteel.png', rotY=spin-90, rotZ=90, rotOrder=['z','y'], Collide=False, scale=[2,2])
    
    # handle bars
    ph1 = [pb[0] + np.cos(np.deg2rad(spin+90))*(dist/2), mid, pb[2] - np.sin(np.deg2rad(spin+90))*(dist/2)]
    ph2 = [pb[0] - np.cos(np.deg2rad(spin+90))*(dist/2), mid, pb[2] + np.sin(np.deg2rad(spin+90))*(dist/2)]

    MiroAPI.add_cylinderShape(MiroSystem, r, h, 2500, ph1, 'chrome.png', scale=[2,2])
    MiroAPI.add_cylinderShape(MiroSystem, r, h, 2500, ph2, 'chrome.png', scale=[2,2])
    
def revolute_door(MiroSystem, d, l, spin, pos):
    l=l-0.03
    top = pos[1]
    mid = pos[1]/2+d/4
    bot = d/2
    # top cross
    greenpole(MiroSystem, d, 2*(l-d), spin   , 90, pos)
    greenpole(MiroSystem, d, 2*(l-d), spin+90, 90, pos)
    
    # bottom cross
    pos[1] = bot
    greenpole(MiroSystem, d, 2*(l-d), spin   , 90, pos)
    greenpole(MiroSystem, d, 2*(l-d), spin+90, 90, pos)

    # middle pole
    pos[1] = mid
    greenpole(MiroSystem, d, top-bot, spin, 0, pos)

    for phi in [0, 90, 180, 270]:
        angle = spin + phi
        p = [pos[0] + np.cos(np.deg2rad(angle))*(l-d/2), mid, pos[2] - np.sin(np.deg2rad(angle))*(l-d/2)]
        greenpole(MiroSystem, d, top-bot+d, angle, 0, p)

    # side walls
    wid = 0.4
    thick = 0.02
    angle = -13
    p = np.array([pos[0]-(l+0.03+thick/2), pos[1], pos[2]])
    p[0] = p[0] - np.sin(np.deg2rad(angle))*wid/2
    p[2] = p[2] - np.cos(np.deg2rad(angle))*wid/2
    MiroAPI.add_boxShape(MiroSystem, thick, top-bot+d, wid, p, 'MITentrance.png', rotY=angle)
        
    p[2] = p[2] + np.cos(np.deg2rad(angle))*wid
    MiroAPI.add_boxShape(MiroSystem, thick, top-bot+d, wid, p, 'MITentrance.png', rotY=-angle)

    p[0] = p[0] + np.sin(np.deg2rad(angle))*wid + 2*(l+0.03+thick/2)
    MiroAPI.add_boxShape(MiroSystem, thick, top-bot+d, wid, p, 'MITentrance.png', rotY=angle)

    p[2] = p[2] - np.cos(np.deg2rad(angle))*wid
    MiroAPI.add_boxShape(MiroSystem, thick, top-bot+d, wid, p, 'MITentrance.png', rotY=-angle)
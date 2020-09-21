import pychrono.core as chrono
import numpy as np

def MIT_Entrance(ChSystem, SPEEDMODE = False):
    pos_south = [1.7, 0, 12.16]
    pos_north = [8.67, 0, 12.16]
    if(SPEEDMODE):
        QuickEntrance(ChSystem, pos_south, pos_north)
    else:
        FullEntrance(ChSystem, pos_south, pos_north)
    
def QuickEntrance(ChSystem, pos_south, pos_north):
    h = 3.1

    center = chrono.ChVectorD((pos_south[0]+pos_north[0])/2, (pos_south[1]+pos_north[1])/2 + h/2, (pos_south[2]+pos_north[2])/2)
    wid = np.abs(pos_south[0]-pos_north[0])

    door = chrono.ChBody()
    door.SetBodyFixed(True)
    door.SetCollide(True)
    door.SetPos(center)
    # compute rot from v=pn-ps -> dot(v, nx) = |v|cos(rot) if rot is needed
    # door.SetRot(chrono.Q_from_AngAxis(rot,chrono.ChVectorD(0,1,0)))
    
    # Collision shape
    door.GetCollisionModel().ClearModel()
    door.GetCollisionModel().AddBox(wid/2, h/2, 0.05) # hemi sizes
    door.GetCollisionModel().BuildModel()

    # Visualization shape
    door_shape = chrono.ChBoxShape()
    door_shape.GetBoxGeometry().Size = chrono.ChVectorD(wid/2, h/2, 0.05)
    door.GetAssets().push_back(door_shape)
    door_texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/MITentrance_quick.png'))
    door_texture.SetTextureScale(4, 3)
    door.GetAssets().push_back(door_texture)
    
    ChSystem.Add(door)

    # south wall
    p = chrono.ChVectorD(pos_south[0]-0.05, 1.51, pos_south[2] -0.89/2)
    wall = chrono.ChBodyEasyBox(0.1, 3.02, 0.89, 3000)
    wall.SetBodyFixed(True)
    wall.SetCollide(False)
    wall.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/yellow_brick.jpg'))
    texture.SetTextureScale(2, 9)
    wall.GetAssets().push_back(texture)
    ChSystem.Add(wall)

def FullEntrance(ChSystem, pos_south, pos_north):
    d = 0.08
    l = 3.02

    p = chrono.ChVectorD(pos_south[0]+2.89, 1.51, pos_south[2]-0.6)
    pole = chrono.ChBodyEasyBox(2*d, l, 2*d, 1000)
    pole.SetBodyFixed(True)
    pole.SetCollide(False)
    pole.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/white concrete.jpg'))
    texture.SetTextureScale(4, 12)
    pole.GetAssets().push_back(texture)
    ChSystem.Add(pole)

    p = chrono.ChVectorD(pos_south[0]+2.89, 2.7, pos_south[2]-0.6-d-0.01)
    pole = chrono.ChBodyEasyBox(0.568*0.7, 0.285*0.7, 0.02, 1000)
    pole.SetBodyFixed(True)
    pole.SetCollide(False)
    pole.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/exit.png'))
    texture.SetTextureScale(4, 3)
    pole.GetAssets().push_back(texture)
    ChSystem.Add(pole)

    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+(1/2)*d, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+   0.68, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+   2.72, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+   3.06, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+   5.10, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+   5.44, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+   6.58, 1.51, pos_south[2]]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_north[0]-(1/2)*d, 1.51, pos_north[2]]))

    
    ChSystem.Add(greenpole(d, (pos_north[0] - pos_south[0]), 0, 90, [(pos_north[0] + pos_south[0])/2, 2.5+d/2, pos_north[2]-d/20]))
    ChSystem.Add(greenpole(d, (pos_north[0] - pos_south[0]), 0, 90, [(pos_north[0] + pos_south[0])/2, 3.0-d/2, pos_north[2]-d/20]))

    # Small bits on floor
    for s in [[(1/2)*d, 0.68], [2.72, 3.06], [5.10, 5.44], [6.58, pos_north[0]-pos_south[0]-(1/2)*d]]:
        ChSystem.Add(greenpole(d, (s[1] - s[0] - d), 0, 90, [pos_south[0]+ (s[1] + s[0])/2, d/2, pos_north[2]]))

    # Revolving door ground rings
    r = 0.98
    round_floor_S = chrono.ChBodyEasyCylinder(r, 0.02, 1000)
    round_floor_S.SetBodyFixed(True)
    round_floor_S.SetPos(chrono.ChVectorD(pos_south[0]+1.70, 0, pos_south[2]))
    round_floor_S.SetCollide(False)

    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITentrance_floor.png'))
    texture.SetTextureScale(-1, 1)
    round_floor_S.GetAssets().push_back(texture)

    round_floor_N = round_floor_S.Clone()
    round_floor_N.SetPos(chrono.ChVectorD(pos_south[0]+4.08, 0, pos_south[2]))
    
    ChSystem.Add(round_floor_S)
    ChSystem.Add(round_floor_N)

    # Revolving door top rings
    round_door_S = chrono.ChBodyEasyCylinder(r, 0.1, 1000)
    round_door_S.SetBodyFixed(True)
    round_door_S.SetPos(chrono.ChVectorD(pos_south[0]+1.70, 2.45, pos_south[2]))
    round_door_S.SetCollide(False)

    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITentrance.png'))
    texture.SetTextureScale(-1, 1)
    round_door_S.GetAssets().push_back(texture)

    round_door_N = round_door_S.Clone()
    round_door_N.SetPos(chrono.ChVectorD(pos_south[0]+4.08, 2.45, pos_south[2]))
    
    ChSystem.Add(round_door_S)
    ChSystem.Add(round_door_N)

    # Revolving doors
    revolute_door(ChSystem, d, 0.98, 15, [pos_south[0]+1.70, 2.4-d/2, pos_south[2]])
    revolute_door(ChSystem, d, 0.98, 50, [pos_south[0]+4.08, 2.4-d/2, pos_south[2]])

    # Side door, inner
    normal_door(ChSystem, d, 1.1-d, 192, [pos_south[0]+6.58-d, 2.5-d/2, pos_south[2]])

    ########### INNER PART STOPS HERE ###########
    width = pos_north[0] - pos_south[0] + 3.04
    depth = 5
    inner_depth = 2.8
    p = chrono.ChVectorD(pos_south[0]-2+width/2, -0.08, pos_south[2] + depth/2)
    floor = chrono.ChBodyEasyBox(width, 0.16, 5, 3000)
    floor.SetBodyFixed(True)
    floor.SetCollide(True)
    floor.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/stone_floor.jpg'))
    texture.SetTextureScale(12, 9)
    floor.GetAssets().push_back(texture)

    ChSystem.Add(floor)

    roof = floor.Clone()
    p.y = 3.08
    roof.SetPos(p)
    ChSystem.Add(roof)

    # Outer door frames
    z = pos_south[2]+inner_depth
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+0.00+d/2, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    0.33, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    1.51, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    1.59, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    2.77, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    3.25, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    4.43, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    4.51, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+    5.69, 1.51, z]))
    ChSystem.Add(greenpole(d, l, 0, 0, [pos_south[0]+6.02-d/2, 1.51, z]))

    # Outer doors
    normal_door(ChSystem, d, 1.1-d, -15, [pos_south[0]+0.33+d, 2.5-d/2, z]) # south outward
    normal_door(ChSystem, d, 1.1-d, 172, [pos_south[0]+2.77-d, 2.5-d/2, z]) # south inward

    normal_door(ChSystem, d, 1.1-d,  -8, [pos_south[0]+3.25+d, 2.5-d/2, z]) # north outward
    normal_door(ChSystem, d, 1.1-d, 161, [pos_south[0]+5.69-d, 2.5-d/2, z]) # north inward
    
    ChSystem.Add(greenpole(d, 6.02, 0, 90, [pos_south[0]+3.01, 2.5+d/2, z-d/20]))
    ChSystem.Add(greenpole(d, 6.02, 0, 90, [pos_south[0]+3.01, 3.0-d/2, z-d/20]))

    # Small bits on floor
    for s in [[d/2, 0.33], [2.77, 3.25], [5.69, 6.02-d/2]]:
        ChSystem.Add(greenpole(d, (s[1] - s[0] - d), 0, 90, [pos_south[0]+ (s[1] + s[0])/2, d/2, z]))

    # south wall
    p = chrono.ChVectorD(pos_south[0]-0.05, 1.51, pos_south[2] + inner_depth/2-0.89/2)
    wall = chrono.ChBodyEasyBox(0.1, 3.02, inner_depth+0.89, 3000)
    wall.SetBodyFixed(True)
    wall.SetCollide(False)
    wall.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/yellow_brick.jpg'))
    texture.SetTextureScale(7, 9)
    wall.GetAssets().push_back(texture)
    ChSystem.Add(wall)

    # north wall
    p.x = pos_north[0]+0.05
    p.z = p.z + 0.89/2
    wall = chrono.ChBodyEasyBox(0.1, 3.02, inner_depth, 3000)
    wall.SetBodyFixed(True)
    wall.SetCollide(False)
    wall.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/yellow_brick.jpg'))
    texture.SetTextureScale(6, 9)
    wall.GetAssets().push_back(texture)
    ChSystem.Add(wall)

    # WEST WALL
    w = 2
    dw = 0.96

    p = chrono.ChVectorD(pos_north[0]+w/2-dw, 1.51, z)
    wall = chrono.ChBodyEasyBox(w, 3.02, 0.16, 3000)
    wall.SetBodyFixed(True)
    wall.SetCollide(False)
    wall.SetPos(p)

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/yellow_brick.jpg'))
    texture.SetTextureScale(2, 9)
    wall.GetAssets().push_back(texture)
    ChSystem.Add(wall)

    wall=wall.Clone()
    p.x = pos_south[0]-w/2
    wall.SetPos(p)
    ChSystem.Add(wall)

    # Cement pillars outside
    r = 0.12
    pillar = chrono.ChBodyEasyCylinder(r, 3.02, 1000)
    pillar.SetBodyFixed(True)
    pillar.SetPos(chrono.ChVectorD(pos_south[0]-1, 1.51, z - r + (depth-inner_depth)*(3/4)))
    pillar.SetCollide(False)

    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white concrete.jpg'))
    texture.SetTextureScale(-1, 1)
    pillar.GetAssets().push_back(texture)
    ChSystem.Add(pillar)

    pillar = pillar.Clone()
    pillar.SetPos(chrono.ChVectorD(pos_north[0]+1-0.96, 1.51, z - r + (depth-inner_depth)*(3/4)))
    ChSystem.Add(pillar)

    pillar = pillar.Clone()
    pillar.SetPos(chrono.ChVectorD(pos_south[0]+1.6, 1.51, z - r + (depth-inner_depth)))
    ChSystem.Add(pillar)
    
    pillar = pillar.Clone()
    pillar.SetPos(chrono.ChVectorD(pos_north[0]-1.6-0.96, 1.51, z - r + (depth-inner_depth)))
    ChSystem.Add(pillar)


def greenpole(d, l, spin, tilt, pos):
    p = chrono.ChVectorD(pos[0], pos[1], pos[2])
    pole = chrono.ChBodyEasyBox(d, l, d, 1000)
    pole.SetBodyFixed(True)
    pole.SetCollide(False)
    pole.SetPos(p)
    pole.SetRot(chrono.Q_from_AngAxis(np.deg2rad(tilt),chrono.ChVectorD(0,0,1)))
    pole.SetRot(chrono.Q_from_AngAxis(np.deg2rad(spin),chrono.ChVectorD(0,1,0))*pole.GetRot())

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/MITentrance.png'))
    texture.SetTextureScale(0.5, 50)
    pole.GetAssets().push_back(texture)

    return pole

def normal_door(ChSystem, d, l, spin, pos):
    top = pos[1]
    mid = pos[1]/2+d/4
    bot = d/2
    # vertical frame poles
    pos[1] = mid
    ChSystem.Add(greenpole(d, top-bot+d, spin, 0, pos))
    p = [pos[0] + np.cos(np.deg2rad(spin))*(l-d/2), mid, pos[2] - np.sin(np.deg2rad(spin))*(l-d/2)]
    ChSystem.Add(greenpole(d, top-bot+d, spin, 0, p))

    # top and bottom frame
    p = [pos[0] + (1/2)*np.cos(np.deg2rad(spin))*(l-d/2), top, pos[2] - (1/2)*np.sin(np.deg2rad(spin))*(l-d/2)]
    ChSystem.Add(greenpole(d, l-d, spin, 90, p))
    p[1] = bot
    ChSystem.Add(greenpole(d, l-d, spin, 90, p))

    # handle
    r = 0.02
    h = 0.40
    dist = 0.30

    # poles through door
    pb = [pos[0] + np.cos(np.deg2rad(spin))*(l-d/2)*0.86, mid+h*(1/3), pos[2] - np.sin(np.deg2rad(spin))*(l-d/2)*0.86]
    bar = chrono.ChBodyEasyCylinder(r/2, dist, 2500)
    bar.SetPos(chrono.ChVectorD(pb[0], pb[1], pb[2]))
    bar.SetRot(chrono.Q_from_AngAxis(np.pi/2,chrono.ChVectorD(0,0,1)))
    bar.SetRot(chrono.Q_from_AngAxis(np.deg2rad(spin-90),chrono.ChVectorD(0,1,0))*bar.GetRot())
    bar.SetBodyFixed(True)
    bar.SetCollide(False)

    # Frame texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/chrome.png'))
    texture.SetTextureScale(2, 2)
    bar.GetAssets().push_back(texture)

    ChSystem.Add(bar)

    
    pb[1] = mid-h*(1/3)
    bar = bar.Clone()
    bar.SetPos(chrono.ChVectorD(pb[0], pb[1], pb[2]))
    ChSystem.Add(bar)
    
    # disks on door
    pb[1] = mid+h*(1/3)
    disk = chrono.ChBodyEasyCylinder(r*1.2, 0.01, 2500)
    disk.SetPos(chrono.ChVectorD(pb[0], pb[1], pb[2]))
    disk.SetRot(chrono.Q_from_AngAxis(np.pi/2,chrono.ChVectorD(0,0,1)))
    disk.SetRot(chrono.Q_from_AngAxis(np.deg2rad(spin-90),chrono.ChVectorD(0,1,0))*disk.GetRot())
    disk.SetBodyFixed(True)
    disk.SetCollide(False)

    # Frame texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/brushsteel.png'))
    texture.SetTextureScale(2, 2)
    disk.GetAssets().push_back(texture)

    ChSystem.Add(disk)

    pb[1] = mid-h*(1/3)
    disk = disk.Clone()
    disk.SetPos(chrono.ChVectorD(pb[0], pb[1], pb[2]))
    ChSystem.Add(disk)


    # handle bars
    ph1 = [pb[0] + np.cos(np.deg2rad(spin+90))*(dist/2), mid, pb[2] - np.sin(np.deg2rad(spin+90))*(dist/2)]
    ph2 = [pb[0] - np.cos(np.deg2rad(spin+90))*(dist/2), mid, pb[2] + np.sin(np.deg2rad(spin+90))*(dist/2)]
    handle = chrono.ChBodyEasyCylinder(r, h, 2500)
    handle.SetPos(chrono.ChVectorD(ph1[0], ph1[1], ph1[2]))
    handle.SetBodyFixed(True)
    handle.SetCollide(False)

    # Frame texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/chrome.png'))
    texture.SetTextureScale(2, 2)
    handle.GetAssets().push_back(texture)

    ChSystem.Add(handle)

    handle = handle.Clone()
    handle.SetPos(chrono.ChVectorD(ph2[0], ph2[1], ph2[2]))
    ChSystem.Add(handle)


    

def revolute_door(ChSystem, d, l, spin, pos):
    l=l-0.03
    top = pos[1]
    mid = pos[1]/2+d/4
    bot = d/2
    # top cross
    ChSystem.Add(greenpole(d, 2*(l-d), spin   , 90, pos))
    ChSystem.Add(greenpole(d, 2*(l-d), spin+90, 90, pos))
    
    # bottom cross
    pos[1] = bot
    ChSystem.Add(greenpole(d, 2*(l-d), spin   , 90, pos))
    ChSystem.Add(greenpole(d, 2*(l-d), spin+90, 90, pos))

    # middle pole
    pos[1] = mid
    ChSystem.Add(greenpole(d, top-bot, spin, 0, pos))

    for phi in [0, 90, 180, 270]:
        angle = spin + phi
        p = [pos[0] + np.cos(np.deg2rad(angle))*(l-d/2), mid, pos[2] - np.sin(np.deg2rad(angle))*(l-d/2)]
        ChSystem.Add(greenpole(d, top-bot+d, angle, 0, p))

    # side walls
    wid = 0.4
    thick = 0.02
    angle = -13
    p = chrono.ChVectorD(pos[0]-(l+0.03+thick/2), pos[1], pos[2])
    p.x = p.x - np.sin(np.deg2rad(angle))*wid/2
    p.z = p.z - np.cos(np.deg2rad(angle))*wid/2
    wall = chrono.ChBodyEasyBox(thick, top-bot+d, wid, 1000)
    wall.SetBodyFixed(True)
    wall.SetCollide(False)
    wall.SetPos(p)
    wall.SetRot(chrono.Q_from_AngAxis(np.deg2rad(angle),chrono.ChVectorD(0,1,0)))

    texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/MITentrance.png'))
    texture.SetTextureScale(4, 3)
    wall.GetAssets().push_back(texture)

    ChSystem.Add(wall)

    wall = wall.Clone()
    p.z = p.z + np.cos(np.deg2rad(angle))*wid
    wall.SetPos(p)
    wall.SetRot(chrono.Q_from_AngAxis(np.deg2rad(-angle),chrono.ChVectorD(0,1,0)))
    ChSystem.Add(wall)

    wall = wall.Clone()
    p.x = p.x + np.sin(np.deg2rad(angle))*wid + 2*(l+0.03+thick/2)
    wall.SetPos(p)
    wall.SetRot(chrono.Q_from_AngAxis(np.deg2rad(angle),chrono.ChVectorD(0,1,0)))
    ChSystem.Add(wall)

    wall = wall.Clone()
    p.z = p.z - np.cos(np.deg2rad(angle))*wid
    wall.SetPos(p)
    wall.SetRot(chrono.Q_from_AngAxis(np.deg2rad(-angle),chrono.ChVectorD(0,1,0)))
    ChSystem.Add(wall)
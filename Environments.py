import pychrono.core as chrono
import os
import numpy as np

import Shapes as shp 

import Environments_Johan
import Environments_Marcus
import Environments_Franz

def MIT_place(system, SPEEDMODE = False):
    target = [2,2.1,-3]

    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    chrono.SetChronoDataPath(os.getcwd() + "/")

    Environments_Johan.Johan_Components(system, SPEEDMODE)
    Environments_Marcus.Marcus_Components(system, SPEEDMODE)
    Environments_Franz.Franz_Components(system, SPEEDMODE)

    # Add MIT floor as a box
    MIT_floor_x = 8
    MIT_floor_z = 8

    body_floor = chrono.ChBody()
    body_floor.SetBodyFixed(True)
    body_floor.SetPos(chrono.ChVectorD(0.5, -1, -3))    #2.5, -1, -1
    
    # Collision shape
    body_floor.GetCollisionModel().ClearModel()
    body_floor.GetCollisionModel().AddBox(MIT_floor_x, 1, MIT_floor_z) # hemi sizes
    body_floor.GetCollisionModel().BuildModel()
    body_floor.SetCollide(True)
    
    # Visualization shape
    body_floor_shape = chrono.ChBoxShape()
    body_floor_shape.GetBoxGeometry().Size = chrono.ChVectorD(MIT_floor_x, 1, MIT_floor_z)
    body_floor.GetAssets().push_back(body_floor_shape)
    
    body_floor_texture = chrono.ChTexture()
    body_floor_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MITfloor.png'))
    body_floor_texture.SetTextureScale(23, 18)
    body_floor.GetAssets().push_back(body_floor_texture)
    
    system.Add(body_floor)

    # Create the shaking table, as a box
    
    size_table_x = 1
    size_table_y = 0.2
    size_table_z = 1
    
    body_table = chrono.ChBody()
    body_table.SetPos(chrono.ChVectorD(0, 1-size_table_y/2, 0 ))
    
    # Collision shape
    body_table.GetCollisionModel().ClearModel()
    body_table.GetCollisionModel().AddBox(size_table_x/2, size_table_y/2, size_table_z/2) # hemi sizes
    body_table.GetCollisionModel().BuildModel()
    body_table.SetCollide(True)
    
    # Visualization shape
    body_table_shape = chrono.ChBoxShape()
    body_table_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_table_x/2, size_table_y/2, size_table_z/2)
    body_table_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    body_table.GetAssets().push_back(body_table_shape)
    
    body_table_texture = chrono.ChTexture()
    body_table_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/grid.png'))
    body_table_texture.SetTextureScale(1, 1)
    body_table.GetAssets().push_back(body_table_texture)
    
    system.Add(body_table)
    
    
    # Create a constraint that blocks free 3 x y z translations and 3 rx ry rz rotations
    # of the table respect to the floor, and impose that the relative imposed position
    # depends on a specified motion law.
    
    link_shaker = chrono.ChLinkLockLock()
    link_shaker.Initialize(body_table, body_floor, chrono.CSYSNORM)
    system.Add(link_shaker)
    
    # ..create the function for imposed x horizontal motion, etc.
    mfunY = chrono.ChFunction_Sine(0,1.5,0.001)  # phase, frequency, amplitude
    link_shaker.SetMotion_Y(mfunY)
    
    # ..create the function for imposed y vertical motion, etc.
    mfunZ = chrono.ChFunction_Sine(0,1.5,0.12)  # phase, frequency, amplitude
    link_shaker.SetMotion_Z(mfunZ)


    roof(system)
    target_box(system, target)
    # can(system, [2.8,0.85,-9.8])
    if not SPEEDMODE:
        can(system, [1.9,2.1,-3.5], 'schrodbull.png')
        can(system, [1.98,2.1,-3.3], 'joultcola.png')

    return target

def can(system, target, text):
    h = 0.22
    r = 0.04
    eps = 0.003
    pos_bot = chrono.ChVectorD(target[0], target[1]+eps/2, target[2])
    pos_can = chrono.ChVectorD(target[0], target[1]+eps+h/2, target[2])
    pos_lid = chrono.ChVectorD(target[0], target[1]+eps*3/2+h, target[2])
    
    # Create top
    lid = chrono.ChBodyEasyCylinder(r, eps, 100)
    lid.SetPos(chrono.ChVectorD(pos_lid))
    lid.SetBodyFixed(False)
    lid.SetCollide(False)

    # Collision shape
    lid.SetCollide(True)
    lid.GetCollisionModel().ClearModel()
    lid.GetCollisionModel().AddCylinder(r, r, eps/2)
    lid.GetCollisionModel().BuildModel()
    
    # Body texture
    lid_texture = chrono.ChTexture()
    lid_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/sodacan_lid.png'))
    lid_texture.SetTextureScale(1, 1)
    lid.GetAssets().push_back(lid_texture)
    
    system.Add(lid)

    # Create bottom
    bot = chrono.ChBodyEasyCylinder(r, eps, 100)
    bot.SetPos(chrono.ChVectorD(pos_bot))
    bot.SetBodyFixed(False)
    bot.SetCollide(False)

    # Collision shape
    bot.SetCollide(True)
    bot.GetCollisionModel().ClearModel()
    bot.GetCollisionModel().AddCylinder(r, r, eps/2)
    bot.GetCollisionModel().BuildModel()
    
    # Body texture
    bot_texture = chrono.ChTexture()
    bot_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/sodacan_bot.png'))
    bot_texture.SetTextureScale(1, 1)
    bot.GetAssets().push_back(bot_texture)
    
    system.Add(bot)

    # Create Can Hitbox
    can = chrono.ChBodyEasyCylinder(r, h, 150)
    can.SetBodyFixed(False)

    # Collision shape
    can.SetCollide(True)
    can.GetCollisionModel().ClearModel()
    can.GetCollisionModel().AddCylinder(r, r, h/2)
    can.GetCollisionModel().BuildModel()

    # Frame texture
    can_texture = chrono.ChTexture()
    can_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/'+text))
    can_texture.SetTextureScale(1, -1)
    can.GetAssets().push_back(can_texture)

    can.SetPos(chrono.ChVectorD(pos_can))

    # can.SetPos_dt(chrono.ChVectorD(0,1,10))

    system.Add(can)
    
    epsvec = chrono.ChVectorD(0,eps/2,0)
    
    rot_lid = can.GetRot() * chrono.Q_from_AngAxis( np.pi/2,chrono.ChVectorD(1,0,0))
    rot_bot = can.GetRot() * chrono.Q_from_AngAxis(-np.pi/2,chrono.ChVectorD(1,0,0))

    lidlink = chrono.ChLinkRevolute()
    mframe_lid = chrono.ChFrameD(pos_lid-epsvec, rot_lid)
    lidlink.Initialize(can, lid, mframe_lid)

    botlink = chrono.ChLinkRevolute()
    mframe_bot = chrono.ChFrameD(pos_bot+epsvec, rot_bot)
    botlink.Initialize(can, bot, mframe_bot)


    # lidlink = chrono.ChLinkMateFix()
    # lidlink.Initialize(can, lid)
    system.Add(lidlink)

    # botlink = chrono.ChLinkMateFix()
    # botlink.Initialize(can, bot)
    system.Add(botlink)

def target_box(system, target):
    h = 0.15
    eps = 0.0025
    size = 1
    pos_a = chrono.ChVectorD(target[0], target[1]-eps, target[2])
    pos_b = chrono.ChVectorD(target[0], target[1]-(h+2*eps)/2, target[2])
    
    # Create dartboard layer
    targetBox = chrono.ChBodyEasyCylinder(size, eps, 1000)
    targetBox.SetBodyFixed(True)
    targetBox.SetPos(chrono.ChVectorD(pos_a))
    targetBox.SetCollide(False)
    
    # Body texture
    targetBox_texture = chrono.ChTexture()
    targetBox_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/target_dart.png'))
    targetBox_texture.SetTextureScale(-1, 1)
    targetBox.GetAssets().push_back(targetBox_texture)
    
    system.Add(targetBox)

    # Create Hitbox
    targetFrame = chrono.ChBodyEasyCylinder(size, h, 1000)
    targetFrame.SetBodyFixed(True)

    # Collision shape
    targetFrame.SetCollide(True)
    targetFrame.GetCollisionModel().ClearModel()
    targetFrame.GetCollisionModel().AddCylinder(size, size, h/2)
    targetFrame.GetCollisionModel().BuildModel()

    # Frame texture
    targetFrame_texture = chrono.ChTexture()
    targetFrame_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/black_smere.jpg'))
    targetFrame_texture.SetTextureScale(8, -1)
    targetFrame.GetAssets().push_back(targetFrame_texture)

    targetFrame.SetPos(chrono.ChVectorD(pos_b))

    system.Add(targetFrame)

def roof(system):
    h = 14.12
    dy = 2/3
    z = 5.06
    dec = -0.1325
    xspan = [-7.44, 8.34]

    #sides
    p1 = chrono.ChVectorD(-0.06-1.5*dy, 0, 0)
    p2 = chrono.ChVectorD(+0.06+1.5*dy, 0, 0)
    d1 = chrono.ChVectorD(0, 0,-1)
    d2 = chrono.ChVectorD(dec,0,-1)
    s = 0.98
    sideS = shp.step(p1,d1, p2,d2, 15.65, 0.2, [s,s,s])
    sideN = shp.step(p1,d1, p2,d2, 15.65, 0.2, [s,s,s])
    qr = chrono.Q_from_AngAxis(np.pi/2, chrono.ChVectorD(0,0,1))
    sideS.SetRot(qr)
    sideN.SetRot(qr)
    sideS.SetPos(chrono.ChVectorD(-7.5,h-0.06,5.1))
    sideN.SetPos(chrono.ChVectorD(8.6,h-0.06,5.1))
    system.Add(sideS)
    system.Add(sideN)

    beams = 4
    dx = (xspan[1] - xspan[0])/(beams-1)
    for b in range(beams):
        p1 = chrono.ChVectorD(xspan[0] + dx*b - 0.06, h+0.8, z-0.06)
        p2 = chrono.ChVectorD(xspan[0] + dx*b + 0.06, h+0.8, z-0.06)
        d1 = chrono.ChVectorD(0,dec,-1)
        d2 = chrono.ChVectorD(0,dec,-1)
        system.Add(shp.step(p1,d1, p2,d2, 16.3-0.1, 0.2))
    

    # Beam texture
    beam_texture = chrono.ChTexture()
    beam_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white_smere.jpg'))
    beam_texture.SetTextureScale(100, 1.5)

    beams = 10
    dx = (xspan[1] - xspan[0])/(beams-1)
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD(xspan[0] + dx*b, h-0.025, z))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD(0.05, 1, 0.05)
        step_comp.GetAssets().push_back(step_comp_shape)
        step_comp.GetAssets().push_back(beam_texture)
        system.Add(step_comp)

    beams = 4
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD((xspan[0]+xspan[1])/2, h-1.06+dy*b, z))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD((xspan[1]-xspan[0])/2+0.06, 0.06, 0.06)
        step_comp.GetAssets().push_back(step_comp_shape)
        step_comp.GetAssets().push_back(beam_texture)
        system.Add(step_comp)

    beams = 5
    h_0 = h-1.06+dy*3+0.12*dec
    d = 3.97
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD((xspan[0]+xspan[1])/2, h_0+dec*d*b, z-0.12-d*b))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD((xspan[1]-xspan[0])/2+0.06, 0.06, 0.06)
        step_comp.GetAssets().push_back(step_comp_shape)
        step_comp.GetAssets().push_back(beam_texture)
        system.Add(step_comp)


    # Roof frame
    wall_texture = chrono.ChTexture()
    wall_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/white concrete.jpg'))
    wall_texture.SetTextureScale(40, 5) 

    # West wall
    wallW = chrono.ChBody()
    wallW.SetBodyFixed(True)
    wallW.SetPos(chrono.ChVectorD(0.5,12.5,5.1))
    
    # Collision shape
    wallW.GetCollisionModel().ClearModel()
    wallW.GetCollisionModel().AddBox(8.1, 0.5, 0.1) # hemi sizes
    wallW.GetCollisionModel().BuildModel()
    wallW.SetCollide(True)
    
    # Visualization shape
    wallW_shape = chrono.ChBoxShape()
    wallW_shape.GetBoxGeometry().Size = chrono.ChVectorD(8.1, 0.5, 0.1)
    wallW.GetAssets().push_back(wallW_shape)
    wallW.GetAssets().push_back(wall_texture)
    
    system.Add(wallW)

    # South wall
    wallS = chrono.ChBody()
    wallS.SetBodyFixed(True)
    wallS.SetPos(chrono.ChVectorD(-7.6,12.5,-3))
    
    # Collision shape
    wallS.GetCollisionModel().ClearModel()
    wallS.GetCollisionModel().AddBox(0.1, 0.5, 8) # hemi sizes
    wallS.GetCollisionModel().BuildModel()
    wallS.SetCollide(True)
    
    # Visualization shape
    wallS_shape = chrono.ChBoxShape()
    wallS_shape.GetBoxGeometry().Size = chrono.ChVectorD(0.1, 0.5, 8)
    wallS.GetAssets().push_back(wallS_shape)
    wallS.GetAssets().push_back(wall_texture)
    
    system.Add(wallS)

    # East wall
    wallE = chrono.ChBody()
    wallE.SetBodyFixed(True)
    wallE.SetPos(chrono.ChVectorD(0.5,12.5,-11.1))
    
    # Collision shape
    wallE.GetCollisionModel().ClearModel()
    wallE.GetCollisionModel().AddBox(8.1, 0.5, 0.1) # hemi sizes
    wallE.GetCollisionModel().BuildModel()
    wallE.SetCollide(True)
    
    # Visualization shape
    wallE_shape = chrono.ChBoxShape()
    wallE_shape.GetBoxGeometry().Size = chrono.ChVectorD(8.1, 0.5, 0.1)
    wallE.GetAssets().push_back(wallE_shape)
    wallE.GetAssets().push_back(wall_texture)
    
    system.Add(wallE)

    # North wall
    wallN = chrono.ChBody()
    wallN.SetBodyFixed(True)
    wallN.SetPos(chrono.ChVectorD(8.5,12.5,-3))
    
    # Collision shape
    wallN.GetCollisionModel().ClearModel()
    wallN.GetCollisionModel().AddBox(0.1, 0.5, 8) # hemi sizes
    wallN.GetCollisionModel().BuildModel()
    wallN.SetCollide(True)
    
    # Visualization shape
    wallN_shape = chrono.ChBoxShape()
    wallN_shape.GetBoxGeometry().Size = chrono.ChVectorD(0.1, 0.5, 8)
    wallN.GetAssets().push_back(wallN_shape)
    wallN.GetAssets().push_back(wall_texture)
    
    system.Add(wallN)

    # MA roof
    roofMA = chrono.ChBody()
    roofMA.SetBodyFixed(True)
    roofMA.SetPos(chrono.ChVectorD(10.56,12.098,-4))
    
    # Collision shape
    roofMA.GetCollisionModel().ClearModel()
    roofMA.GetCollisionModel().AddBox(2.145, 0.1, 13) # hemi sizes
    roofMA.GetCollisionModel().BuildModel()
    roofMA.SetCollide(True)
    
    # Visualization shape
    roofMA_shape = chrono.ChBoxShape()
    roofMA_shape.GetBoxGeometry().Size = chrono.ChVectorD(2.145, 0.1, 13)
    roofMA.GetAssets().push_back(roofMA_shape)
    roofMA_texture = chrono.ChTexture('textures/white concrete.jpg')
    roofMA_texture.SetTextureScale(40, 80) 
    roofMA.GetAssets().push_back(roofMA_texture)
    
    system.Add(roofMA)
    
    # MC roof
    roofMC = chrono.ChBody()
    roofMC.SetBodyFixed(True)
    roofMC.SetPos(chrono.ChVectorD(0.416,12.098,7.1))
    
    # Collision shape
    roofMC.GetCollisionModel().ClearModel()
    roofMC.GetCollisionModel().AddBox(8, 0.1, 2.145) # hemi sizes
    roofMC.GetCollisionModel().BuildModel()
    roofMC.SetCollide(True)
    
    # Visualization shape
    roofMC_shape = chrono.ChBoxShape()
    roofMC_shape.GetBoxGeometry().Size = chrono.ChVectorD(8, 0.1, 1.9)
    roofMC.GetAssets().push_back(roofMC_shape)
    roofMC_texture = chrono.ChTexture('textures/white concrete.jpg')
    roofMC_texture.SetTextureScale(80, 10) 
    roofMC.GetAssets().push_back(roofMC_texture)
    
    system.Add(roofMC)
    
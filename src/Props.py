import pychrono.core as chrono
import numpy as np

from MiroClasses import MiroNotifier as MN
from MiroClasses import MiroComponent as MC

def dartboard(ChSystem, target):
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
    
    ChSystem.Add(targetBox)

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

    ChSystem.Add(targetFrame)

def sodacan(ChSystem, target, text = 'schrodbull.png', angle = 0, SPEEDMODE = False):
    h = 0.22
    r = 0.04
    
    pos_can = chrono.ChVectorD(target[0], target[1]+h/2, target[2])

    # Create Can Hitbox
    can = chrono.ChBodyEasyCylinder(r, h, 50)
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

    if angle != 0:
        can.SetRot(chrono.Q_from_AngAxis(np.deg2rad(angle), chrono.ChVectorD(0,1,0)))

    # can.SetPos_dt(chrono.ChVectorD(0,1,10))

    ChSystem.Add(can)

    if not SPEEDMODE:
        eps = 0.003
        epsvec = chrono.ChVectorD(0,eps/2,0)
        can.Move(epsvec)
        can.Move(epsvec)
        pos_bot = chrono.ChVectorD(target[0], target[1]+eps/2, target[2])
        pos_lid = chrono.ChVectorD(target[0], target[1]+eps*3/2+h, target[2])
        
        # Create top
        lid = chrono.ChBodyEasyCylinder(r, eps, 150)
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
        
        ChSystem.Add(lid)

        # Create bottom
        bot = chrono.ChBodyEasyCylinder(r, eps, 200)
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
        
        ChSystem.Add(bot)
        
        
        rot_lid = can.GetRot() * chrono.Q_from_AngAxis( np.pi/2,chrono.ChVectorD(1,0,0))
        rot_bot = can.GetRot() * chrono.Q_from_AngAxis(-np.pi/2,chrono.ChVectorD(1,0,0))

        lidlink = chrono.ChLinkRevolute()
        mframe_lid = chrono.ChFrameD(pos_lid-epsvec, rot_lid)
        lidlink.Initialize(can, lid, mframe_lid)

        botlink = chrono.ChLinkRevolute()
        mframe_bot = chrono.ChFrameD(pos_bot+epsvec, rot_bot)
        botlink.Initialize(can, bot, mframe_bot)

        ChSystem.Add(lidlink)
        ChSystem.Add(botlink)

def painting(ChSystem, pos, text = 'DemoBengan.png', rot = 0, dims = [1, 0.6]):
    canvas = chrono.ChBody()
    canvas.SetBodyFixed(True)
    canvas.SetCollide(False)
    canvas.SetPos(chrono.ChVectorD(pos[0], pos[1], pos[2]))
    canvas.SetRot(chrono.Q_from_AngAxis(np.deg2rad(rot),chrono.ChVectorD(0,1,0)))

    # Visualization shape
    canvas_shape = chrono.ChBoxShape()
    canvas_shape.GetBoxGeometry().Size = chrono.ChVectorD(dims[0], dims[1], 0.05)
    canvas.GetAssets().push_back(canvas_shape)
    canvas_texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/'+text))
    canvas_texture.SetTextureScale(4, 3)
    canvas.GetAssets().push_back(canvas_texture)
    ChSystem.Add(canvas)

def pokeball(ChSystem, pos, rot = 0):
    r = 0.05

    ball = chrono.ChBodyEasySphere(r, 500)
    ball.SetBodyFixed(False)
    ball.SetPos(chrono.ChVectorD(pos[0], pos[1]+r, pos[2]))
    ball.SetRot(chrono.Q_from_AngAxis(rot,chrono.ChVectorD(0,1,0)))

    # Collision shape
    ball.SetCollide(True)
    ball.GetCollisionModel().ClearModel()
    ball.GetCollisionModel().AddSphere(r)
    ball.GetCollisionModel().BuildModel()

    ball_texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/pokeball.jpg'))
    ball_texture.SetTextureScale(1, 1)
    ball.GetAssets().push_back(ball_texture)
    ChSystem.Add(ball)

def coin(ChSystem, target, angle = 0):
    h = 0.0012
    r = 0.012
    
    pos_coin = chrono.ChVectorD(target[0], target[1]+h/2, target[2])

    # Create Can Hitbox
    coin = chrono.ChBodyEasyCylinder(r, h, 50)
    coin.SetBodyFixed(False)

    # Collision shape
    coin.SetCollide(True)
    coin.GetCollisionModel().ClearModel()
    coin.GetCollisionModel().AddCylinder(r, r, h/2)
    coin.GetCollisionModel().BuildModel()

    # Frame texture
    coin_texture = chrono.ChTexture()
    coin_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/gammal5kr.png'))
    coin_texture.SetTextureScale(1, -1)
    coin.GetAssets().push_back(coin_texture)

    coin.SetPos(chrono.ChVectorD(pos_coin))

    if angle != 0:
        coin.SetRot(chrono.Q_from_AngAxis(np.deg2rad(angle), chrono.ChVectorD(0,1,0)))

    ChSystem.Add(coin)

def MIT_door(ChSystem, pos, rot = 0):
    b = 1.0
    h = 2.1

    door = chrono.ChBody()
    door.SetBodyFixed(True)
    door.SetCollide(False)
    door.SetPos(chrono.ChVectorD(pos[0], pos[1]+h/2, pos[2]))
    door.SetRot(chrono.Q_from_AngAxis(np.deg2rad(rot),chrono.ChVectorD(0,1,0)))

    # Visualization shape
    door_shape = chrono.ChBoxShape()
    door_shape.GetBoxGeometry().Size = chrono.ChVectorD(b/2, h/2, 0.08)
    door.GetAssets().push_back(door_shape)
    door_texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/MIT_door.png'))
    door_texture.SetTextureScale(4, 3)
    door.GetAssets().push_back(door_texture)
    ChSystem.Add(door)

def dino(ChSystem, pos, rot = 0, scale = 0.1):
    dino_comp = MC.MiroComponent()
    dino_comp.SetImportDir('src/')
    dino_comp.ImportObj('tyra.obj',[0.4,0.2,0.6], scale)
    dino = dino_comp.GetBody()
    dino.SetBodyFixed(True)
    dino.SetCollide(False)
    dino.SetPos(chrono.ChVectorD(pos[0], pos[1]+1.35*scale, pos[2]))
    # dino.SetPos_dt(chrono.ChVectorD(0, 2, 5))
    dino.SetRot(chrono.Q_from_AngAxis(np.deg2rad(rot),chrono.ChVectorD(0,1,0))*dino.GetRot())
    
    # dino.SetBodyFixed(False)
    # dino.SetCollide(True)
    # dino.GetCollisionModel().ClearModel()
    # # colmod = chrono.ChCollisionModel()
    # # colmod.AddSphere()
    # # Right leg
    # dino.GetCollisionModel().AddCylinder(0.2*scale, 0.25*scale, 0.5*scale, chrono.ChVectorD(-0.5*scale,-0.8*scale,-0.8*scale))
    # # Left leg
    # dino.GetCollisionModel().AddCylinder(0.2*scale, 0.25*scale, 0.5*scale, chrono.ChVectorD(0.5*scale,-0.8*scale,0.0*scale))
    # # Body
    # rot = 1.4
    # bodmat = chrono.ChMatrix33D(
    #     chrono.ChVectorD( 1,           0, np.sin(rot)),
    #     chrono.ChVectorD( 0, np.cos(rot),-np.sin(rot)),
    #     chrono.ChVectorD( 0, np.sin(rot), np.cos(rot))
    # )
    # dino.GetCollisionModel().AddCylinder(0.4*scale, 0.65*scale, 1*scale, chrono.ChVectorD(-0.1*scale,0.1*scale,-0.25*scale),bodmat)
    # # Head
    # dino.GetCollisionModel().AddSphere(0.4*scale, chrono.ChVectorD(-0.2*scale,0.9*scale,-1.35*scale))
    # dino.GetCollisionModel().BuildModel()
    # dino.SetShowCollisionMesh(True)

    ChSystem.Add(dino)
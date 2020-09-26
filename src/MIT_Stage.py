import pychrono.core as chrono
import numpy as np
import os

from src import Shapes as shp

def build(ChSystem, SPEEDMODE = False):
    stage(ChSystem)
    screen(ChSystem, SPEEDMODE)
    back_stage(ChSystem)

#coner position (-7.5,0,-11)
def stage(system): 
    theta_f = 0 
    theta_b = np.pi/2
    pos_f = chrono.ChVectorD(-4.3, 0, -8.8)
    dir_f = chrono.ChVectorD(np.cos(theta_f), 0, np.sin(theta_f)) 
    pos_b = chrono.ChVectorD(-5.3, 0, -7.8)
    dir_b = chrono.ChVectorD(np.cos(theta_b), 0, np.sin(theta_b))
    step = shp.step(pos_f, dir_f, pos_b, dir_b, 3, 0.3, [0.02,0.02,0.02])
    system.Add(step)


def screen(system, SPEEDMODE = False):
    corner_pos = chrono.ChVectorD(-5.3,3.55,-8.8)
    size_length = 4
    size_width = 0.01
    size_height = size_length/(4/3)
    
    alpha = np.pi/10
    delta_tilt = chrono.ChVectorD(np.sin(alpha)/np.sqrt(2), np.cos(alpha), np.sin(alpha)/np.sqrt(2))*size_height/2
    screen_pos = corner_pos + chrono.ChVectorD(1/np.sqrt(8),0, 1/np.sqrt(8))*size_length + delta_tilt
    pro_screen = chrono.ChBody()
    pro_screen.SetBodyFixed(True)
    pro_screen.SetPos(screen_pos)

    # Collision shape
    pro_screen.GetCollisionModel().ClearModel()
    pro_screen.GetCollisionModel().AddBox(size_length/2, size_height/2, size_width/2) # hemi sizes
    pro_screen.GetCollisionModel().BuildModel()
    pro_screen.SetCollide(True)
    
    # Visualization shape
    pro_screen_shape = chrono.ChBoxShape()
    pro_screen_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_length/2, size_height/2, size_width/2)
    pro_screen_shape.SetColor(chrono.ChColor(255,255,255))
    pro_screen.GetAssets().push_back(pro_screen_shape)
    
    pro_screen_texture = chrono.ChTexture()
    grouplogo_file = 'GroupLogo_local.png'
    if not os.path.isfile(grouplogo_file):
        grouplogo_file = 'GroupLogo.png'
    pro_screen_texture.SetTextureFilename(chrono.GetChronoDataFile(grouplogo_file))
    pro_screen_texture.SetTextureScale(-4, -3)
    pro_screen.GetAssets().push_back(pro_screen_texture)

    rot_x = chrono.ChVectorD(1,0,0)
    rot_y = chrono.ChVectorD(0,1,0)
    alpha = np.pi/10
    beta = np.pi/4
    qr_x = chrono.Q_from_AngAxis(alpha, rot_x.GetNormalized())    # Rotate the screen
    qr_y = chrono.Q_from_AngAxis(beta, rot_y.GetNormalized())
    quaternion = qr_y* qr_x * pro_screen.GetRot()
    pro_screen.SetRot(quaternion)

    system.Add(pro_screen)

    # Top cylinder
    r = 0.08
    roller = chrono.ChBodyEasyCylinder(r, 4.15, 1000)
    roller.SetBodyFixed(True)
    roller.SetCollide(False)
    roller.SetPos(screen_pos + delta_tilt*((1.9*r+size_height)/size_height))
    qr = chrono.Q_from_AngAxis(np.pi/2, chrono.ChVectorD(1,0,1).GetNormalized())
    roller.SetRot(qr * roller.GetRot())

    system.Add(roller)

    if not SPEEDMODE:
        # Hanging bars
        bar_h = 0.1
        dx = chrono.ChVectorD(0.25, 0, 0)  
        dz = chrono.ChVectorD(0, 0, 0.25)  

        barN = chrono.ChBodyEasyBox(bar_h/2, bar_h/2, 2.4/2, 1000)
        barN.SetBodyFixed(True)
        barN.SetCollide(False)
        roller_mid = screen_pos + delta_tilt*((3.9*r+size_height)/size_height) + chrono.ChVectorD(0,bar_h/2,0)
        offset = chrono.ChVectorD(1,0,-1)
        offset.SetLength(1.8)
        barN.SetPos(roller_mid + offset - dz)

        system.Add(barN)

        barS = barN.Clone()
        barS.SetRot(chrono.Q_from_AngAxis(np.pi/2, chrono.ChVectorD(0,1,0)) * barS.GetRot())
        barS.SetPos(roller_mid - offset - dx)

        system.Add(barS)

def back_stage(system):
    coner_pos = chrono.ChVectorD(-5.3,1.55,-8.8) # Real coner -5.3,1.25,-8.8
    length = 1.3
    in_screen_pos = coner_pos + chrono.ChVectorD(1/np.sqrt(2),0, 1/np.sqrt(2))*length
    in_screen = chrono.ChBody()
    in_screen.SetBodyFixed(True)
    in_screen.SetPos(in_screen_pos)

    size_len = 2.5
    size_width = 0.05
    size_height = 2.5
    # Collision shape
    in_screen.GetCollisionModel().ClearModel()
    in_screen.GetCollisionModel().AddBox((size_len)/2, (size_height)/2, size_width/2) # hemi sizes
    in_screen.GetCollisionModel().BuildModel()
    in_screen.SetCollide(True)
    
    # Visualization shape
    in_screen_shape = chrono.ChBoxShape()
    in_screen_shape.GetBoxGeometry().Size = chrono.ChVectorD((size_len)/2, (size_height)/2, size_width/2)
    in_screen_shape.SetColor(chrono.ChColor(0.4,0.4,0.5))
    in_screen.GetAssets().push_back(in_screen_shape)
    system.Add(in_screen)
    in_screen_texture = chrono.ChTexture()
    in_screen_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/tf-logo.jpg'))
    in_screen_texture.SetTextureScale(-4, -3)
    in_screen.GetAssets().push_back(in_screen_texture)

    
    rot_y = chrono.ChVectorD(0,1,0)
    alpha = np.pi/4
    qr_y = chrono.Q_from_AngAxis(alpha, rot_y.GetNormalized())
    quaternion = qr_y * in_screen.GetRot() #rotates the inner screen
    in_screen.SetRot(quaternion)
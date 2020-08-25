import pychrono.core as chrono
import numpy as np

def MIT_Entrance(system, SPEEDMODE = False):
    QuickEntrance(system)
    # if(SPEEDMODE):
    #     QuickEntrance(system)
    #     return
    
def QuickEntrance(system):
    pos_south = [2, 0, 13]
    pos_north = [12.5, 0, 13]
    h = 3.9

    center = chrono.ChVectorD((pos_south[0]+pos_north[0])/2, (pos_south[1]+pos_north[1])/2 + h/2, (pos_south[2]+pos_north[2])/2)
    wid = np.abs(pos_south[0]-pos_north[0])


    door = chrono.ChBody()
    door.SetBodyFixed(True)
    door.SetCollide(True)
    door.SetPos(center)
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
    
    system.Add(door)

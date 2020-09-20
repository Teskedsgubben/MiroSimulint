import pychrono.core as chrono
import numpy as np

from src import Shapes as shp
from src import Environments_Johan
from src import Environments_Marcus
from src import Environments_Franz
from src import MIT_Entrance
from src import MIT_Props

def build_MIT(system, SPEEDMODE = False):
    # Create the room floor: a simple fixed rigid body with a collision shape
    # and a visualization shape
    Environments_Johan.Johan_Components(system, SPEEDMODE)
    Environments_Marcus.Marcus_Components(system, SPEEDMODE)
    Environments_Franz.Franz_Components(system, SPEEDMODE)
    MIT_Entrance.MIT_Entrance(system, SPEEDMODE)

    # Add MIT floor as a box
    MIT_floor_x = (4.5+4.8+4.5)/2
    MIT_floor_z = (4.5+4.8+4.5)/2

    body_floor = chrono.ChBody()
    body_floor.SetBodyFixed(True)
    body_floor.SetPos(chrono.ChVectorD(1.6, -1, -1.9))    #2.5, -1, -1
    
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

    roof(system)
    if not SPEEDMODE:
        MIT_Props.AddProps(system)

def roof(system):
    frame_h = 1.0
    dy = 2/3
    xspan = [-5.25, 8.35]
    yspan = [9.96, 13.96]
    zspan = [-8.9, 5.1]

    dec = -(yspan[1]-yspan[0]-frame_h)/(zspan[1]-zspan[0])
    dy = yspan[1]-yspan[0]-frame_h
    #sides
    p1 = chrono.ChVectorD(-dy/2, 0, 0)
    p2 = chrono.ChVectorD(0.16+dy/2, 0, 0)
    d1 = chrono.ChVectorD(0, 0,-1)
    d2 = chrono.ChVectorD(dec,0,-1)
    s = 0.98
    sideS = shp.step(p1,d1, p2,d2, zspan[1]-zspan[0], 0.2, [s,s,s])
    sideN = shp.step(p1,d1, p2,d2, zspan[1]-zspan[0], 0.2, [s,s,s])
    qr = chrono.Q_from_AngAxis(np.pi/2, chrono.ChVectorD(0,0,1))
    sideS.SetRot(qr)
    sideN.SetRot(qr)
    sideS.SetPos(chrono.ChVectorD(xspan[0]-0.05,  yspan[0]+frame_h + (yspan[1]-yspan[0]-frame_h)/2, zspan[1]+0.1))
    sideN.SetPos(chrono.ChVectorD(xspan[1]+0.25,  yspan[0]+frame_h + (yspan[1]-yspan[0]-frame_h)/2, zspan[1]+0.1))
    system.Add(sideS)
    system.Add(sideN)

    beams = 4
    dx = (xspan[1] - xspan[0])/(beams-1)
    for b in range(beams):
        p1 = chrono.ChVectorD(xspan[0] + dx*b - 0.06, yspan[1]-0.12, zspan[1]-0.06)
        p2 = chrono.ChVectorD(xspan[0] + dx*b + 0.06, yspan[1]-0.12, zspan[1]-0.06)
        d1 = chrono.ChVectorD(0,dec,-1)
        d2 = chrono.ChVectorD(0,dec,-1)
        system.Add(shp.step(p1,d1, p2,d2, (zspan[1]-zspan[0])*(np.sqrt(1+dec**2)), 0.2))
    

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
        step_comp.SetPos(chrono.ChVectorD(xspan[0] + dx*b, (yspan[1] + yspan[0] + frame_h)/2, zspan[1]))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD(0.05, (yspan[1] - yspan[0] - frame_h)/2, 0.05)
        step_comp.GetAssets().push_back(step_comp_shape)
        step_comp.GetAssets().push_back(beam_texture)
        system.Add(step_comp)

    beams = 5
    dy = (yspan[1]-yspan[0]-frame_h)/(beams-1)
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD((xspan[0]+xspan[1])/2, yspan[0]+frame_h+0.06+dy*b, zspan[1]))

        # Visualization shape
        step_comp_shape = chrono.ChBoxShape()
        step_comp_shape.GetBoxGeometry().Size = chrono.ChVectorD((xspan[1]-xspan[0])/2+0.06, 0.06, 0.06)
        step_comp.GetAssets().push_back(step_comp_shape)
        step_comp.GetAssets().push_back(beam_texture)
        system.Add(step_comp)

    beams = 5
    h_0 = yspan[1]+0.12*dec
    dz = (zspan[1]-zspan[0])/(beams-1) - 0.28/beams
    for b in range(beams):
        step_comp = chrono.ChBody()
        step_comp.SetBodyFixed(True)
        step_comp.SetCollide(False)
        step_comp.SetPos(chrono.ChVectorD((xspan[0]+xspan[1])/2, h_0+dec*dz*b, zspan[1]-0.12-dz*b))
        step_comp.SetRot(chrono.Q_from_AngAxis(np.sin(dec), chrono.ChVectorD(1,0,0)))

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
    wallW.SetPos(chrono.ChVectorD((xspan[0]+xspan[1])/2, yspan[0]+frame_h/2, zspan[1]))
    
    # Collision shape
    wallW.GetCollisionModel().ClearModel()
    wallW.GetCollisionModel().AddBox((xspan[1]-xspan[0]+0.5)/2, frame_h/2, 0.1) # hemi sizes
    wallW.GetCollisionModel().BuildModel()
    wallW.SetCollide(True)
    
    # Visualization shape
    wallW_shape = chrono.ChBoxShape()
    wallW_shape.GetBoxGeometry().Size = chrono.ChVectorD((xspan[1]-xspan[0]+0.5)/2, frame_h/2, 0.1)
    wallW.GetAssets().push_back(wallW_shape)
    wallW.GetAssets().push_back(wall_texture)
    
    system.Add(wallW)

    # East wall
    wallE = wallW.Clone()
    wallE.SetPos(chrono.ChVectorD((xspan[0]+xspan[1])/2, yspan[0]+frame_h/2, zspan[0]))
    system.Add(wallE)


    # South wall
    wallS = chrono.ChBody()
    wallS.SetBodyFixed(True)
    wallS.SetPos(chrono.ChVectorD(xspan[0]-0.15,yspan[0]+frame_h/2,(zspan[1]+zspan[0])/2))
    
    # Collision shape
    wallS.GetCollisionModel().ClearModel()
    wallS.GetCollisionModel().AddBox(0.1, frame_h/2, (zspan[1]-zspan[0])/2-0.1) # hemi sizes
    wallS.GetCollisionModel().BuildModel()
    wallS.SetCollide(True)
    
    # Visualization shape
    wallS_shape = chrono.ChBoxShape()
    wallS_shape.GetBoxGeometry().Size = chrono.ChVectorD(0.1, frame_h/2, (zspan[1]-zspan[0])/2-0.1)
    wallS.GetAssets().push_back(wallS_shape)
    wallS.GetAssets().push_back(wall_texture)
    
    system.Add(wallS)

    # North wall
    wallN = wallS.Clone()
    wallN.SetPos(chrono.ChVectorD(xspan[1]+0.15,yspan[0]+frame_h/2,(zspan[1]+zspan[0])/2))  
    system.Add(wallN)

    # MA roof
    roofMA_width = 6.6
    roofMA = chrono.ChBody()
    roofMA.SetBodyFixed(True)
    roofMA.SetPos(chrono.ChVectorD(xspan[1] + roofMA_width/2 + 0.052, yspan[0]+0.098, -0.2))
    
    # Collision shape
    roofMA.GetCollisionModel().ClearModel()
    roofMA.GetCollisionModel().AddBox(roofMA_width/2, 0.1, 12.5) # hemi sizes
    roofMA.GetCollisionModel().BuildModel()
    roofMA.SetCollide(True)
    
    # Visualization shape
    roofMA_shape = chrono.ChBoxShape()
    roofMA_shape.GetBoxGeometry().Size = chrono.ChVectorD(roofMA_width/2, 0.1, 12.55)
    roofMA.GetAssets().push_back(roofMA_shape)
    roofMA_texture = chrono.ChTexture('textures/white concrete.jpg')
    roofMA_texture.SetTextureScale(40, 80) 
    roofMA.GetAssets().push_back(roofMA_texture)
    
    system.Add(roofMA)
    
    # MC roof
    roofMC_width = 3.165
    roofMC = chrono.ChBody()
    roofMC.SetBodyFixed(True)
    roofMC.SetPos(chrono.ChVectorD((xspan[1]+xspan[0])/2,yspan[0]+0.098,zspan[1]+roofMC_width/2+0.1))
    
    # Collision shape
    roofMC.GetCollisionModel().ClearModel()
    roofMC.GetCollisionModel().AddBox((xspan[1]-xspan[0])/2 + 0.052, 0.1, roofMC_width/2) # hemi sizes
    roofMC.GetCollisionModel().BuildModel()
    roofMC.SetCollide(True)
    
    # Visualization shape
    roofMC_shape = chrono.ChBoxShape()
    roofMC_shape.GetBoxGeometry().Size = chrono.ChVectorD((xspan[1]-xspan[0])/2 + 0.052, 0.1, roofMC_width/2)
    roofMC.GetAssets().push_back(roofMC_shape)
    roofMC_texture = chrono.ChTexture('textures/white concrete.jpg')
    roofMC_texture.SetTextureScale(80, 10) 
    roofMC.GetAssets().push_back(roofMC_texture)
    
    system.Add(roofMC)

    # Computer Science roof
    roofCS = chrono.ChBody()
    roofCS.SetBodyFixed(True)
    roofCS.SetPos(chrono.ChVectorD(6.85,yspan[0]+0.098,zspan[1]+roofMC_width+2.092))
    
    # Collision shape
    roofCS.GetCollisionModel().ClearModel()
    roofCS.GetCollisionModel().AddBox(1,1,0.1) # hemi sizes
    roofCS.GetCollisionModel().BuildModel()
    roofCS.SetCollide(True)
    
    # Visualization shape
    roofCS_shape = chrono.ChBoxShape()
    roofCS_shape.GetBoxGeometry().Size = chrono.ChVectorD(1.552,0.1,1.992)
    roofCS.GetAssets().push_back(roofCS_shape)
    roofCS_texture = chrono.ChTexture('textures/white concrete.jpg')
    roofCS_texture.SetTextureScale(80, 10) 
    roofCS.GetAssets().push_back(roofCS_texture)
    
    system.Add(roofCS)



def old_shaketable(system, body_floor):
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
    
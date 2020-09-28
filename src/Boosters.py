import pychrono.core as chrono
import numpy as np

from MiroClasses import MiroComponent as mc

def MCB01(trigger_function, rot = [0,0,0], pos = [0,0,0], Fixed = False):
    '''A booster that emits a pulse when the trigger function returns True.\n
    The trigger function must follow the form:\n
    def trigger_function(position, velocity, acceleration)'''
    size_h = 0.05
    size_r = 0.0075
    density_brick = 0.05/(np.pi*size_r**2*size_h)   # kg/m^3

    body_brick = chrono.ChBodyEasyCylinder(size_r, size_h, density_brick)
    body_brick.SetBodyFixed(False)
    body_brick.SetCollide(True)

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddCylinder(size_r, size_r, size_h/2) # hemi sizes
    body_brick.GetCollisionModel().BuildModel()

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/booster.png'))
    texture.SetTextureScale(1, -1)
    body_brick.AddAsset(texture)

    # Generate MiroComponent with above ChBody
    BOOSTER = mc.MiroBooster(body_brick)
    BOOSTER.SetTrigger(trigger_function)
    BOOSTER.SetConsumption(1000)
    BOOSTER.SetForce(0.5, 0.4, [0,-size_h/2,0])

    BOOSTER.AddLinkPoint('A', [ 1, 0, 0], chrono.ChVectorD( size_r, size_h/2-0.01, 0))
    BOOSTER.AddLinkPoint('B', [ 1, 0, 0], chrono.ChVectorD( size_r,-size_h/2+0.01, 0))
    BOOSTER.AddLinkPoint('C', [ 0, 0, 1], chrono.ChVectorD( 0, size_h/2-0.01, size_r))
    BOOSTER.AddLinkPoint('D', [ 0, 0, 1], chrono.ChVectorD( 0,-size_h/2+0.01, size_r))
    
    BOOSTER.Rotate(rot)
    BOOSTER.MoveToPosition(pos)

    return BOOSTER
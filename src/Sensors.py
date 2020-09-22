import pychrono.core as chrono
import numpy as np

from MiroClasses import MiroComponent as mc

def MSA01(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_x * size_y * size_z

    inertia_brick_xx = (size_y**2 + size_z**2)*mass_brick/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass_brick/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(False)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))     

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MSA01.png'))
    texture.SetTextureScale(4, 3)
    body_brick.AddAsset(texture)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Accelerometer(body_brick)
    SENSOR.SetPollingRate(120)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], chrono.ChVectorD(0, size_y/2, 0))
    SENSOR.Rotate(rot)

    return SENSOR

def MSA02(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_x * size_y * size_z

    inertia_brick_xx = (size_y**2 + size_z**2)*mass_brick/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass_brick/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(False)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))     

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MSA02.png'))
    texture.SetTextureScale(4, 3)
    body_brick.AddAsset(texture)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Accelerometer(body_brick)
    SENSOR.SetPollingRate(300)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], chrono.ChVectorD(0, size_y/2, 0))
    SENSOR.Rotate(rot)

    return SENSOR

def MSV01(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_x * size_y * size_z

    inertia_brick_xx = (size_y**2 + size_z**2)*mass_brick/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass_brick/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(False)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))     

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MSV01.png'))
    texture.SetTextureScale(4, 3)
    body_brick.AddAsset(texture)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Speedometer(body_brick)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], chrono.ChVectorD(0, size_y/2, 0))
    SENSOR.Rotate(rot)

    return SENSOR

def MSO01(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    density_brick = 1000   # kg/m^3
    mass_brick = density_brick * size_x * size_y * size_z

    inertia_brick_xx = (size_y**2 + size_z**2)*mass_brick/3
    inertia_brick_yy = (size_x**2 + size_z**2)*mass_brick/3
    inertia_brick_zz = (size_x**2 + size_y**2)*mass_brick/3

    body_brick = chrono.ChBody()
    body_brick.SetBodyFixed(False)
    body_brick.SetCollide(True)
    # set mass properties
    body_brick.SetMass(mass_brick)
    body_brick.SetInertiaXX(chrono.ChVectorD(inertia_brick_xx, inertia_brick_yy, inertia_brick_zz))     

    # Collision shape
    body_brick.GetCollisionModel().ClearModel()
    body_brick.GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2) # must set half sizes
    body_brick.GetCollisionModel().BuildModel()

    # Visualization shape, for rendering animation
    body_brick_shape = chrono.ChBoxShape()
    body_brick_shape.GetBoxGeometry().Size = chrono.ChVectorD(size_x/2, size_y/2, size_z/2)
    body_brick.AddAsset(body_brick_shape)

    # Apply texture
    texture = chrono.ChTexture()
    texture.SetTextureFilename(chrono.GetChronoDataFile('textures/MSO01.png'))
    texture.SetTextureScale(4, 3)
    body_brick.AddAsset(texture)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Odometer(body_brick)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], chrono.ChVectorD(0, size_y/2, 0))
    SENSOR.Rotate(rot)

    return SENSOR
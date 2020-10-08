from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

from MiroClasses import MiroComponent as mc

def MSA01(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    # density_brick = 868   # kg/m^3
    mass_brick = 0.010
    sensor_body = MiroAPI.add_boxShape(False, size_x, size_y, size_z, [0,0,0], texture='MSA01.png', Fixed=False, mass=mass_brick)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Accelerometer(sensor_body)
    SENSOR.SetPollingRate(120)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], [0, size_y/2, 0])
    SENSOR.Rotate(rot)

    return SENSOR

def MSA02(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    # density_brick = 1000   # kg/m^3
    mass_brick = 0.010
    sensor_body = MiroAPI.add_boxShape(False, size_x, size_y, size_z, [0,0,0], texture='MSA02.png', Fixed=False, mass=mass_brick)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Accelerometer(sensor_body)
    SENSOR.SetPollingRate(300)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], [0, size_y/2, 0])
    SENSOR.Rotate(rot)

    return SENSOR

def MSV01(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    # density_brick = 1000   # kg/m^3
    mass_brick = 0.020
    sensor_body = MiroAPI.add_boxShape(False, size_x, size_y, size_z, [0,0,0], texture='MSV01.png', Fixed=False, mass=mass_brick)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Speedometer(sensor_body)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], [0, size_y/2, 0])
    SENSOR.Rotate(rot)

    return SENSOR

def MSO01(rot = [0,0,0]):
    size_x = 0.04
    size_y = 0.012
    size_z = 0.024
    # density_brick = 1000   # kg/m^3
    mass_brick = 0.040
    sensor_body = MiroAPI.add_boxShape(False, size_x, size_y, size_z, [0,0,0], texture='MSO01.png', Fixed=False, mass=mass_brick)

    # Generate MiroComponent based MiroSensor with above ChBody
    SENSOR = mc.MiroSensor_Odometer(sensor_body)

    # Top
    SENSOR.AddLinkPoint('Linkpoint', [0, 1, 0], [0, size_y/2, 0])
    SENSOR.Rotate(rot)

    return SENSOR
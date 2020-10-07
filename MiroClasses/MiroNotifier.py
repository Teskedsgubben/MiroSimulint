from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np

class MiroNotifier():
    def __init__(self, pos, angle = 0, tilt = 0):
        self.width = 4
        self.height = 1.5
        self.radius = 0.35
        self.turn_angle = np.deg2rad(angle)
        self.tilt_angle = np.deg2rad(tilt)
        self.position = np.array(pos)

        bulb_pos_hrz = np.array([np.cos(self.turn_angle ), 0, -np.sin(self.turn_angle)]) * (self.width/2 - 1.6*self.radius)
        bulb_pos_vrt = np.array([np.cos(self.turn_angle +np.pi/2)*np.sin(self.tilt_angle), np.cos(self.tilt_angle), -np.sin(self.turn_angle +np.pi/2)*np.sin(self.tilt_angle)]) * (self.height/2 - 1.6*self.radius)
        self.bulb_pos = bulb_pos_hrz + bulb_pos_vrt

    def AddToSystem(self, system):
        MiroAPI.add_boxShape(system, self.width, self.height, 0.05, self.position, 'textures/notifboard.png', rotX=self.tilt_angle, rotY=self.turn_angle, rotDegrees=False)
        self.bulb = MiroAPI.add_sphereShape(system, self.radius, self.position+self.bulb_pos, 'textures/notifbulb.png', rotX=self.tilt_angle+np.pi/2, rotY=self.turn_angle, rotDegrees=False)


    def Set_Idle(self):
        MiroAPI.rotateBody(self.bulb, rotAngle=180, rotAxis=self.bulb_pos)
    def Set_Ready(self):
        MiroAPI.rotateBody(self.bulb, rotAngle=-180, rotAxis=self.bulb_pos)
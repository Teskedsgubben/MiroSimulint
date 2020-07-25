import pychrono.core as chrono
import numpy as np

class MiroComponent():
    def __init__(self, body):
        self.linkpoints = {}
        self.body = body

    def AddToSystem(self, system):
        system.Add_Object(self.body)

    def AddLinkPoint(self, name, coord):
        self.linkpoints.update({name: coord})

    def GetLinkPoint(self, name):
        return self.body.GetPos() + self.linkpoints[name]
    
    def GetBody(self):
        return self.body

    def MoveBy(self, delta_pos):
        pos_x = delta_pos[0]
        pos_y = delta_pos[1]
        pos_z = delta_pos[2]

        posvec = chrono.ChVectorD(pos_x, pos_y, pos_z)
        self.body.Move(posvec)

    def MoveToPosition(self, pos):
        pos_x = pos[0]
        pos_y = pos[1]
        pos_z = pos[2]

        posvec = chrono.ChVectorD(pos_x, pos_y, pos_z)
        
        self.body.Move(posvec - self.body.GetPos())
    def MoveToMatch(self, pointname, other_component, other_pointname):
        self.body.Move(other_component.GetLinkPoint(other_pointname) - self.GetLinkPoint(pointname))

    def Rotate(self, rotation):
        rot_x = np.pi/180 * rotation[0]
        rot_y = np.pi/180 * rotation[1]
        rot_z = np.pi/180 * rotation[2]

        qr = chrono.Q_from_Euler123(chrono.ChVectorD(rot_x, rot_y, rot_z))
        quaternion = qr * self.body.GetRot()

        self.body.SetRot(quaternion)

        for name, link in self.linkpoints.items():
            self.linkpoints.update({name: quaternion.Rotate(link)})


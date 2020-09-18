import pychrono.core as chrono
import numpy as np

class MiroComponent():
    def __init__(self, body):
        self.linkpoints = {}
        self.linkdirs = {}
        self.body = body

    def GetMass(self):
        return self.body.GetMass()
        
    def AddToSystem(self, system):
        system.Add_Object(self.body)

    def AddLinkPoint(self, name, normal, coord):
        self.linkpoints.update({name: coord})
        self.linkdirs.update({name: chrono.ChVectorD(normal[0], normal[1], normal[2]).GetNormalized()})

    def GetPosition(self):
        return self.body.GetPos()

    def GetLinkPoint(self, name):
        return self.body.GetPos() + self.linkpoints[name]

    def GetLinkDir(self, name):
        return self.body.GetRot().Rotate(self.linkdirs[name])
        
    def GetLinkPointXYZ(self, name):
        lp = self.body.GetPos() + self.linkpoints[name]
        return [lp.x, lp.y, lp.z]
    
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
    def MoveToMatch(self, pointname, other_component, other_pointname, dist = 0):
        marg = other_component.GetLinkDir(other_pointname).GetNormalized()
        marg.SetLength(dist)
        self.body.Move(other_component.GetLinkPoint(other_pointname) - self.GetLinkPoint(pointname) + marg)

    def Rotate(self, rotation, quaternion = False):
        if not quaternion:
            rot_x = np.pi/180 * rotation[0]
            rot_y = np.pi/180 * rotation[1]
            rot_z = np.pi/180 * rotation[2]

            quaternion = chrono.Q_from_Euler123(chrono.ChVectorD(rot_x, rot_y, rot_z))
        
        q_rotation = quaternion * self.body.GetRot()
        self.body.SetRot(q_rotation)

        for name, link in self.linkpoints.items():
            self.linkpoints.update({name: quaternion.Rotate(link)})

    def SetVelocity(self, vel):
        vel_x = vel[0]
        vel_y = vel[1]
        vel_z = vel[2]

        self.body.SetPos_dt(chrono.ChVectorD(vel_x, vel_y, vel_z))


# Sensor class extends component class
class MiroSensor(MiroComponent):
    def Initialize(self, output_file_name):
        self.printed = False
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
    def LogData(self):
        return


class MiroSensor_Accelerometer(MiroSensor):
    def LogData(self):
        if not self.printed:
            acc = self.GetBody().GetPos_dtdt()
            data = str(acc.x)+' '+str(acc.y + 9.8)+' '+str(acc.z)+'\n'
            self.filestream.write(data)


import pychrono.core as chrono
import numpy as np
import os.path

class MiroComponent():
    def __init__(self, body = False):
        self.linkpoints = {}
        self.linkdirs = {}
        self.importdir = 'object_files/'
        if body:
            self.body = body

    def SetImportDir(self, dirname):
        self.importdir = dirname

    def ImportObj(self, filename, color = [0.8, 0.8, 0.8], scale = 0.001):
        filename = self.importdir+filename
        if not os.path.isfile(filename):
            print('Could not locate file: '+filename)
            return
        loadfile = filename[0:filename.find('.obj')]+'_scale'+str(scale)+'.obj'
        if not os.path.isfile(loadfile):
            self.ScaleObjFile(filename, loadfile, scale)
        self.body = chrono.ChBodyEasyMesh(loadfile, 1000, True, True)
        self.body.AddAsset(chrono.ChColorAsset(chrono.ChColor(color[0], color[1], color[2])))

    def ScaleObjFile(self, filename_to_scale, output_name, scale = 0.001):
        '''Rescales a .obj, default is from mm to m'''

        print('Rescaling '+filename_to_scale+' into '+output_name+'...')
        filereader = open(filename_to_scale, "r")
        text = filereader.readlines()
        iend = len(text) - 1

        filestream = open(output_name, "w")
        filestream.truncate(0)

        xdim = {'min': float('inf'), 'max': float('-inf')}
        ydim = {'min': float('inf'), 'max': float('-inf')}
        zdim = {'min': float('inf'), 'max': float('-inf')}
        
        for i in range(iend):
            if text[i][0] == 'v' and text[i][1] == ' ':
                v = text[i].split()
                x = float(v[1])*scale
                y = float(v[2])*scale
                z = float(v[3])*scale
                if x < xdim['min']:
                    xdim['min'] = x
                if x > xdim['max']:
                    xdim['max'] = x
                if y < ydim['min']:
                    ydim['min'] = y
                if y > ydim['max']:
                    ydim['max'] = y
                if z < zdim['min']:
                    zdim['min'] = z
                if z > zdim['max']:
                    zdim['max'] = z
                data = str(v[0])+' '+format(x,'.6f')+' '+format(y,'.6f')+' '+format(z,'.6f')+'\n'
                filestream.write(data)
            else:
                filestream.write(text[i])
        print('Object scaled, sizes:\n   x: '+str(xdim['max']-xdim['min'])+', y: '+str(ydim['max']-ydim['min'])+', z: '+str(zdim['max']-zdim['min']))

    def GetMass(self):
        return self.body.GetMass()
        
    def AddToSystem(self, system):
        system.Add_Object(self.body)

    def AddLinkPoint(self, name, normal, coord):
        if type(coord) == type([]):
            coord = chrono.ChVectorD(coord[0], coord[1], coord[2])
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
        '''Rotates from Euler angles or provided quaterion. The functions RotateX, RotateY, RotateZ or RotateAxis are easier to use.'''
        if not quaternion:
            rot_x = np.pi/180 * rotation[0]
            rot_y = np.pi/180 * rotation[1]
            rot_z = np.pi/180 * rotation[2]

            quaternion = chrono.Q_from_Euler123(chrono.ChVectorD(rot_x, rot_y, rot_z))
        
        q_rotation = quaternion * self.body.GetRot()
        self.body.SetRot(q_rotation)

        for name, link in self.linkpoints.items():
            self.linkpoints.update({name: quaternion.Rotate(link)})
    
    def RotateAxis(self, theta, axis):
        '''Rotates the component an angle theta degrees around axis in global coordinates.'''
        angle = theta/180*np.pi
        ax = chrono.ChVectorD(axis[0], axis[1], axis[2])
        qr = chrono.Q_from_AngAxis(angle, ax.GetNormalized())
        self.Rotate(False, qr)

    def RotateX(self, theta):
        self.RotateAxis(theta, [1,0,0])
    def RotateY(self, theta):
        self.RotateAxis(theta, [0,1,0])
    def RotateZ(self, theta):
        self.RotateAxis(theta, [0,0,1])

    def SetVelocity(self, vel):
        vel_x = vel[0]
        vel_y = vel[1]
        vel_z = vel[2]

        self.body.SetPos_dt(chrono.ChVectorD(vel_x, vel_y, vel_z))


# Sensor class extends component class
class MiroSensor(MiroComponent):
    def Initialize(self, output_file_name):
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
    def LogData(self):
        return


class MiroSensor_Accelerometer(MiroSensor):
    def LogData(self):
        acc = self.GetBody().GetPos_dtdt()
        data = str(acc.x)+' '+str(acc.y + 9.8)+' '+str(acc.z)+'\n'
        self.filestream.write(data)


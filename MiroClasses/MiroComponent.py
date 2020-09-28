import pychrono.core as chrono
import numpy as np
import os.path

class MiroComponent():
    def __init__(self, body = False):
        self.linkpoints = {}
        self.linkdirs = {}
        self.importdir = 'object_files/'
        self.msystem = False
        if body:
            self.body = body

    def SetImportDir(self, dirname):
        self.importdir = dirname

    def ImportObj(self, filename, color = [0.8, 0.8, 0.8], scale = 0.001, density = 1000):
        filename = self.importdir+filename
        if not os.path.isfile(filename):
            print('Could not locate file: '+filename)
            return
        loadfile = filename[0:filename.find('.obj')]+'_scale'+str(scale)+'.obj'
        if not os.path.isfile(loadfile):
            self.ScaleObjFile(filename, loadfile, scale)
        self.body = chrono.ChBodyEasyMesh(loadfile, density, True, True)
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

        m=[0,0,0]
        num_vs = 0
        for i in range(iend):
            if text[i][0] == 'v' and text[i][1] == ' ':
                v = text[i].split()
                num_vs = num_vs + 1
                m[0] = float(v[1])*scale
                m[1] = float(v[2])*scale
                m[2] = float(v[3])*scale
        m[0] = m[0]/num_vs
        m[1] = m[2]/num_vs
        m[2] = m[2]/num_vs

        for i in range(iend):
            if text[i][0] == 'v' and text[i][1] == ' ':
                v = text[i].split()
                x = float(v[1])*scale-m[0]
                y = float(v[2])*scale-m[1]
                z = float(v[3])*scale-m[2]
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
        
    def AddToSystem(self, Miro_System):
        self.msystem = Miro_System
        Miro_System.Add_Object(self.body)

    def AddLinkPoint(self, name, normal, coord):
        if type(coord) == type([]):
            coord = chrono.ChVectorD(coord[0], coord[1], coord[2])
        self.linkpoints.update({name: coord})
        linkdir = chrono.ChVectorD(normal[0], normal[1], normal[2])
        if linkdir.Length() > 0:
            linkdir.Normalize()
        self.linkdirs.update({name: linkdir})

    def GetPosition(self):
        return self.body.GetPos()

    def GetLinkPoint(self, name):
        return self.body.GetPos() + self.linkpoints[name]

    def GetLinkDir(self, name):
        return self.linkdirs[name]
        
    def GetLinkPointXYZ(self, name):
        lp = self.body.GetPos() + self.linkpoints[name]
        return [lp.x, lp.y, lp.z]
    
    def GetBody(self):
        return self.body

    def MoveBy(self, delta_pos):
        if type(delta_pos) == type([]):
            delta_pos = chrono.ChVectorD(delta_pos[0], delta_pos[1], delta_pos[2])
        self.body.Move(delta_pos)

    def MoveToPosition(self, pos):
        if type(pos) == type([]):
            pos = chrono.ChVectorD(pos[0], pos[1], pos[2])
        self.body.Move(pos - self.body.GetPos())

    def MoveToMatch(self, pointname, other_component, other_pointname, dist = 0):
        '''Moves the component to match the provided linkpoint position with the position of a 
        linkpoint on the other component. Distance is calculated in the direction of the 
        linkpoint on the other, non-moving component.'''
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
        for name, link in self.linkdirs.items():
            self.linkdirs.update({name: quaternion.Rotate(link)})
    
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

    def SetCollisionAsBox(self, size_x, size_y, size_z, offset = [0,0,0]):
        mass = self.GetBody().GetMass()
        dr = chrono.ChVectorD(offset[0], offset[1], offset[2])
        
        inertia_brick_xx = (size_y**2 + size_z**2)*mass/3
        inertia_brick_yy = (size_x**2 + size_z**2)*mass/3
        inertia_brick_zz = (size_x**2 + size_y**2)*mass/3
        self.GetBody().SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))   
        self.GetBody().GetCollisionModel().ClearModel()
        self.GetBody().GetCollisionModel().AddBox(size_x/2, size_y/2, size_z/2, dr)
        self.GetBody().GetCollisionModel().BuildModel()

    def SetCollisionAsEllipsoid(self, radius_x, radius_y, radius_z, offset = [0,0,0]):
        mass = self.GetBody().GetMass()
        dr = chrono.ChVectorD(offset[0], offset[1], offset[2])
        
        inertia_brick_xx = (radius_y**2 + radius_z**2)*mass/5
        inertia_brick_yy = (radius_x**2 + radius_z**2)*mass/5
        inertia_brick_zz = (radius_x**2 + radius_y**2)*mass/5
        self.GetBody().SetInertiaXX(chrono.ChVectorD(inertia_brick_xx,inertia_brick_yy,inertia_brick_zz))   
        self.GetBody().GetCollisionModel().ClearModel()
        self.GetBody().GetCollisionModel().AddEllipsoid(radius_x/2, radius_y/2, radius_z/2, dr)
        self.GetBody().GetCollisionModel().BuildModel()

    def SetCollisionAsSphere(self, radius, offset = [0,0,0]):
        mass = self.GetBody().GetMass()
        dr = chrono.ChVectorD(offset[0], offset[1], offset[2])
        
        inertia_brick = radius**2*mass*2/5
        self.GetBody().SetInertiaXX(chrono.ChVectorD(inertia_brick, inertia_brick, inertia_brick))   
        self.GetBody().GetCollisionModel().ClearModel()
        self.GetBody().GetCollisionModel().AddSphere(radius, dr)
        self.GetBody().GetCollisionModel().BuildModel()

# Sensor class extends component class
class MiroSensor(MiroComponent):
    def Initialize(self, output_file_name, simulation):
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
    
    def LogData(self):
        return


class MiroSensor_Accelerometer(MiroSensor):
    def Initialize(self, output_file_name, simulation):
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
        self.dt = simulation.GetTimestep()

    def SetPollingRate(self, Hz):
        self.Hz = Hz

    def LogData(self):
        acc = self.GetBody().GetPos_dtdt()
        g = - 9.8
        # Rescales so all instances of momentary acceleration act under 1/300 seconds
        if hasattr(self, 'Hz'):
            acc.Scale(self.Hz * self.dt)
            g = g*(self.Hz * self.dt)
        data = str(acc.x)+' '+str(acc.y - g)+' '+str(acc.z)+'\n'
        self.filestream.write(data)

class MiroSensor_Speedometer(MiroSensor):
    def LogData(self):
        vel = self.GetBody().GetPos_dt()
        data = str(vel.x)+' '+str(vel.y)+' '+str(vel.z)+'\n'
        self.filestream.write(data)

class MiroSensor_Odometer(MiroSensor):
    def Initialize(self, output_file_name, simulation):
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
        self.start = chrono.ChVectorD(self.body.GetPos())

    def LogData(self):
        pos = self.GetBody().GetPos() - self.start
        data = str(pos.x)+' '+str(pos.y)+' '+str(pos.z)+'\n'
        self.filestream.write(data)

# Booster class extends Sensor class
class MiroBooster(MiroSensor):
    def Initialize(self, output_file_name, simulation):
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
        self.dt = simulation.GetTimestep()
        if not hasattr(self, 'fuel'):
            self.fuel = 400
        if not hasattr(self, 'cons'):
            self.cons = 1
        if not hasattr(self, 'trigger'):
            self.trigger = False
        self.triggered = False
        self.expended = False

    def SetTrigger(self, trigger_function):
        self.trigger = trigger_function

    def SetConsumption(self, consumption):
        '''Fuel consumption per simulated second '''
        self.cons = consumption

    def SetForce(self, force, duration=1, point = [0,0,0]):
        self.force = force
        self.duration = duration
        if type(point) == type([]):
            point = chrono.ChVectorD(point[0], point[1], point[2])
        self.relpoint = point

    def SetFuelCap(self, total_fuel):
        self.fuel = total_fuel

    def CheckTrigger(self):
        if not self.triggered:
            if not self.trigger:
                self.triggered = True
            else:
                pos = self.body.GetPos()
                vel = self.body.GetPos_dt()
                acc = self.body.GetPos_dtdt()
                position = [pos.x, pos.y, pos.z]
                velocity = [vel.x, vel.y, vel.z]
                acceleration = [acc.x, acc.y, acc.z]
                if self.trigger(position, velocity, acceleration):
                    self.triggered = True
                    self.F = chrono.ChForce()
                    self.F.SetMode(1)
                    self.F.SetF_y(chrono.ChFunction_Const(self.force))
                    # F.SetVrelpoint(self.body.GetRot().Rotate(self.relpoint))
                    # self.F.SetRelDir(chrono.ChVectorD(0,-1,0))
                    self.body.AddForce(self.F)
        elif self.fuel > 0:
            self.fuel = self.fuel - self.cons*self.dt
        elif not self.expended:
            self.body.RemoveForce(self.F)
            self.expended = True
            
    def LogData(self):
        self.CheckTrigger()
        f = self.force
        if not self.triggered or self.fuel <= 0:
            f = 0
        self.filestream.write(str(f)+' '+str(self.fuel)+'\n')
        return


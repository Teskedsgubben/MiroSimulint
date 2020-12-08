from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
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
        self.body = MiroAPI.LoadFromObj(loadfile, density=density, color=color)

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
        return MiroAPI.GetMass(self.body)
        
    def AddToSystem(self, MiroSystem):
        self.msystem = MiroSystem
        MiroSystem.Add(self.body)

    def AddLinkPoint(self, name, normal, coord):
        self.linkpoints.update({name: np.array(coord)})
        linkdir = np.array(normal)
        if np.linalg.norm(linkdir) > 0:
            linkdir = linkdir/np.linalg.norm(linkdir)
        self.linkdirs.update({name: linkdir})

    def GetPosition(self):
        return MiroAPI.GetBodyPosition(self.body)
    
    def GetVelocity(self):
        return MiroAPI.GetBodyVelocity(self.body)

    def GetLinkPoint(self, name):
        return self.GetPosition() + self.linkpoints[name]

    def GetLinkDir(self, name):
        return self.linkdirs[name]
        
    def GetLinkPointXYZ(self, name):
        lp = self.GetPosition() + self.linkpoints[name]
        return lp
    
    def GetBody(self):
        return self.body

    def MoveBy(self, delta_pos):
        MiroAPI.MoveBodyBy(self.body, delta_pos)

    def MoveToPosition(self, pos):
        MiroAPI.MoveBodyBy(self.body, pos - self.GetPosition())

    def MoveToMatch(self, pointname, other_component, other_pointname, dist = 0):
        '''Moves the component to match the provided linkpoint position with the position of a 
        linkpoint on the other component. Distance is calculated in the direction of the 
        linkpoint on the other, non-moving component.'''
        marg = other_component.GetLinkDir(other_pointname)
        marg = marg*dist
        move = other_component.GetLinkPoint(other_pointname) - self.GetLinkPoint(pointname) + marg
        MiroAPI.MoveBodyBy(self.body, move)

    def Rotate(self, rotation):
        '''Shorthand for rotating X,Y,Z that rotates in that specific order. The functions RotateX, RotateY, RotateZ or RotateAxis are easier to use.'''
        if rotation[0]:
            self.RotateX(rotation[0])
        if rotation[1]:
            self.RotateY(rotation[1])
        if rotation[2]:
            self.RotateZ(rotation[2])
    
    def RotateAxis(self, theta, axis):
        '''Rotates the component an angle theta degrees around axis in global coordinates.'''
        MiroAPI.rotateBody(self.body, rotAngle=theta, rotAxis=axis)
        for name, linkp in self.linkpoints.items():
            linkp_new = MiroAPI.rotateVector(linkp, rotAngle=theta, rotAxis=axis)
            self.linkpoints.update({name: MiroAPI.rotateVector(linkp, rotAngle=theta, rotAxis=axis)})
        for name, linkd in self.linkdirs.items():
            linkd_new = MiroAPI.rotateVector(linkd, rotAngle=theta, rotAxis=axis)
            self.linkdirs.update({name: MiroAPI.rotateVector(linkd, rotAngle=theta, rotAxis=axis)})

    def RotateX(self, theta):
        self.RotateAxis(theta, [1,0,0])
    def RotateY(self, theta):
        self.RotateAxis(theta, [0,1,0])
    def RotateZ(self, theta):
        self.RotateAxis(theta, [0,0,1])

    def SetVelocity(self, vel):
        MiroAPI.SetBodyVelocity(self.body, vel)

    def SetTexture(self, texture_file, scale=[4,3]):
        MiroAPI.ChangeBodyTexture(self.body, texture_file, scale)

    def SetCollisionAsBox(self, size_x, size_y, size_z, offset = [0,0,0]):
        mass = self.GetMass()
        dims = [size_x, size_y, size_z]
        MiroAPI.SetCollisionModel_Box(self.GetBody(), dims, mass, offset)

    def SetCollisionAsEllipsoid(self, radius_x, radius_y, radius_z, offset = [0,0,0]):
        mass = self.GetMass()
        dims = [radius_x, radius_y, radius_z]
        MiroAPI.SetCollisionModel_Ellipsoid(self.GetBody(), dims, mass, offset)

    def SetCollisionAsSphere(self, radius, offset = [0,0,0]):
        mass = self.GetMass()
        dims = [radius, radius, radius]
        MiroAPI.SetCollisionModel_Ellipsoid(self.GetBody(), dims, mass, offset)

# Sensor class extends component class
class MiroSensor(MiroComponent):
    def Initialize(self, output_file_name, MiroSystem):
        self.filename = output_file_name
        self.filestream = open(self.filename, "w")
        self.filestream.truncate(0)
        self.logging = MiroSystem.log
    
    def LogData(self):
        return


class MiroSensor_Accelerometer(MiroSensor):
    def Initialize(self, output_file_name, MiroSystem):
        super().Initialize(output_file_name, MiroSystem)
        self.dt = 1/(MiroSystem.fps * MiroSystem.subframes)

    def SetPollingRate(self, Hz):
        self.Hz = Hz

    def LogData(self):
        if(self.logging):
            acc = MiroAPI.GetBodyAcceleration(self.GetBody())
            g = - 9.8
            # Rescales so all instances of momentary acceleration act under 1/300 seconds
            if hasattr(self, 'Hz'):
                acc = acc*(self.Hz * self.dt)
                g = g*(self.Hz * self.dt)
            data = str(acc[0])+' '+str(acc[1] - g)+' '+str(acc[2])+'\n'
            self.filestream.write(data)

class MiroSensor_Speedometer(MiroSensor):
    def LogData(self):
        if(self.logging):
            vel = MiroAPI.GetBodyVelocity(self.GetBody())
            data = str(vel[0])+' '+str(vel[1])+' '+str(vel[2])+'\n'
            self.filestream.write(data)

class MiroSensor_Odometer(MiroSensor):
    def Initialize(self, output_file_name, MiroSystem):
        super().Initialize(output_file_name, MiroSystem)
        self.start = MiroAPI.GetBodyPosition(self.GetBody())

    def LogData(self):
        if(self.logging):
            pos = MiroAPI.GetBodyPosition(self.GetBody()) - self.start
            data = str(pos[0])+' '+str(pos[1])+' '+str(pos[2])+'\n'
            self.filestream.write(data)

# Booster class extends Sensor class
class MiroBooster(MiroSensor):
    def Initialize(self, output_file_name, MiroSystem):
        super().Initialize(output_file_name, MiroSystem)
        self.dt = 1/(MiroSystem.fps * MiroSystem.subframes)
        if not hasattr(self, 'fuel'):
            self.fuel = 100
        if not hasattr(self, 'cons'):
            self.cons = 1000
        if not hasattr(self, 'trigger'):
            self.trigger = False
        self.triggered = False
        self.expended = False

    def SetTrigger(self, trigger_function):
        self.trigger = trigger_function

    def SetConsumption(self, consumption):
        '''Fuel consumption per simulated second '''
        self.cons = consumption

    def SetForce(self, force_strength):
        self.force = force_strength

    def SetFuel(self, total_fuel):
        '''Total fuel is duration in ms if consumption is not modified'''
        self.fuel = total_fuel

    def CheckTrigger(self):
        if not self.triggered:
            if not self.trigger:
                self.triggered = True
            else:
                position = MiroAPI.GetBodyPosition(self.GetBody())
                velocity = MiroAPI.GetBodyVelocity(self.GetBody())
                acceleration = MiroAPI.GetBodyAcceleration(self.GetBody())
                if self.trigger(position, velocity, acceleration):
                    self.triggered = True
                    self.F = MiroAPI.AddBodyForce(self.GetBody(), self.force, [0,1,0], new=True)
        elif self.fuel > 0:
            MiroAPI.AddBodyForce(self.GetBody(), self.force, [0,1,0], new=False)
            self.fuel = self.fuel - self.cons*self.dt
        elif not self.expended:
            MiroAPI.RemoveBodyForce(self.GetBody(), self.F)
            self.expended = True
            
    def LogData(self):
        self.CheckTrigger()
        if(self.logging):
            f = self.force
            if not self.triggered or self.fuel <= 0:
                f = 0
            self.filestream.write(str(f)+'\n')
        return


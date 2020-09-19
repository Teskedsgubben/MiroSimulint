import pychrono.core as chrono
import numpy as np

class Module():
    def __init__(self):
        self.components = {}
        self.sensors = {}
        self.links = {}
        self.nonames_comp = 0
        self.nonames_sens = 0
        self.fixed = []
        self.refpoint = False
        self.base = False

    def PrintInfo(self):
        print('  Sensors: '+str(len(self.sensors.keys())))
        if len(self.sensors.keys()) > 0:
            for sensor_name in self.sensors.keys():
                print('    - '+sensor_name)
        print('  Components: '+str(len(self.components.keys()) - len(self.sensors.keys())))
        print('  Connections: '+str(len(self.links.keys())))
        print('  Mass: %.3f kg' % (round(self.GetMass(),2)))
    
    def AddComponent(self, comp, name='unnamed'):
        if not self.base:
            self.base = comp
        if(name == 'unnamed'):
            self.nonames_comp = self.nonames_comp + 1
            name = 'unnamed'+str(self.nonames_comp)
        self.components.update({name: comp})
    
    def GetBasePosition(self):
        if self.base:
            return self.base.GetPosition()
        else:
            return chrono.ChVectorD(0,0,0)

    def GetMass(self):
        M = 0
        for _, comp in self.components.items():
            M = M + comp.GetMass()
        return M
    
    def GetComponent(self, name='unnamed'):
        return self.components[name]
    
    def AddSensor(self, sensor, name='unnamed'):
        if(name == 'unnamed'):
            self.nonames_sens = self.nonames_sens + 1
            name = 'unnamed_sensor'+str(self.nonames_sens)
        self.sensors.update({name: sensor})
        self.AddComponent(sensor, name)

    def GetSensor(self, name='unnamed'):
        return self.sensors[name]
    def GetSensorList(self):
        return self.sensors

    def GetLinks(self):
        return self.links
    
    def SetReferencePoint(self, position):
        '''Stores a coordinate relative the module.'''
        self.refpoint = chrono.ChVectorD(position[0], position[1], position[2])
    def GetReferencePoint(self):
        return self.refpoint

    
    def Fixate(self, name, permanent = False):
        ''' Locks a component in place. Component is then set loose upon calling Release on the modulem, unless True is passed for permanent fixation.'''
        if name in self.components:
            self.components[name].GetBody().SetBodyFixed(True)
            if not permanent:
                self.fixed.append(name)
    
    def Release(self):
        for name in self.fixed:
            self.components[name].GetBody().SetBodyFixed(False)
        self.fixed = []
    
    def MarkComponent(self, component_name, color = 'red'):
        '''Change the color of a component to identify it during simulation. \nUse 'red', 'blue' or 'green'.'''
        texture = chrono.ChTexture()
        if color != 'blue' and color != 'green':
            color = 'red'
        texture.SetTextureFilename(chrono.GetChronoDataFile('textures/markpattern_'+color+'.png'))
        texture.SetTextureScale(4, 3)
        self.components[component_name].GetBody().AddAsset(texture)
    
    def ConnectComponents(self, name_A, point_A, name_B, point_B, dist = 0, move = True):
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"."+point_A + "_TO_" + name_B+"."+point_B

        if(move):
            self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A, dist)


        linkpos = chrono.ChVectorD()
        linkpos.Mul(comp_A.GetLinkPoint(point_A) + comp_B.GetLinkPoint(point_B), 1/2)

        # Create a universal link constraint
        mlink = chrono.ChLinkRevolute()
        # the coordinate system of the constraint reference in abs. space:
        mframe = chrono.ChFrameD(linkpos, comp_A.GetBody().GetRot())
        # mframe = chrono.ChCoordsysD(comp_B.GetLinkPoint(point_B), comp_B.GetBody().GetRot())
        # initialize the constraint telling which part must be connected, and where:
        mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), mframe)

        # mlink = chrono.ChLinkMateSpherical()
        # mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), False, comp_A.GetLinkPoint(point_A), comp_B.GetLinkPoint(point_B))
        
        # mlink = chrono.ChLinkTSDA()
        # mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), False, comp_A.GetLinkPoint(point_A), comp_B.GetLinkPoint(point_B))
        # mlink.SetSpringCoefficient(100)
        
        self.links.update({name: mlink})

    def SetSpring(self, name_A, point_A, name_B, point_B, L, K):
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"_"+point_A + "_TO_" + name_B+"_"+point_B

        mlink = chrono.ChLinkTSDA()
        mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), False, comp_A.GetLinkPoint(point_A), comp_B.GetLinkPoint(point_B))
        mlink.SetSpringCoefficient(K)
        mlink.SetDampingCoefficient(K/200)
        mlink.SetRestLength(L)

        self.links.update({name: mlink})

    def AddToSystem(self, system):
        for _, comp in self.components.items():
            comp.AddToSystem(system)
        for _, link in self.links.items():
            system.Add_Object(link)

    def Move(self, distance):
        if(self.refpoint):
            self.refpoint.Add(self.refpoint, chrono.ChVectorD(distance[0], distance[1], distance[2]))
        for _, comp in self.components.items():
            comp.MoveBy(distance)

    def SetPosition(self, pos):
        p = self.base.GetPosition()
        self.Move([pos.x-p.x, pos.y-p.y, pos.z-p.z])    
    
    def MovetoMatch(self, name_A, point_A, name_B, point_B):
        self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A)

    def SetVelocity(self, vel):
        for _, comp in self.components.items():
            comp.SetVelocity(vel)

    def RotateComponents(self, theta, axis):
        angle = theta/180*np.pi
        ax = chrono.ChVectorD(axis[0], axis[1], axis[2])
        qr = chrono.Q_from_AngAxis(angle, ax.GetNormalized())
        for _, comp in self.components.items():
            comp.Rotate(False, qr)
        if self.refpoint:
            vec = qr.Rotate(self.refpoint)
            self.refpoint = vec

    def RotateComponentsX(self, theta):
        self.RotateComponents(theta, [1,0,0])
    def RotateComponentsY(self, theta):
        self.RotateComponents(theta, [0,1,0])
    def RotateComponentsZ(self, theta):
        self.RotateComponents(theta, [0,0,1])
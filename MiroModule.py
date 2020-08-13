import pychrono.core as chrono
import numpy as np

class Module():
    def __init__(self):
        self.components = {}
        self.links = {}
        self.nonames = 0
        self.fixed = []
        self.refpoint = False
        self.base = False
    
    def AddComponent(self, comp, name='unnamed'):
        if not self.base:
            self.base = comp
        if(name == 'unnamed'):
            self.nonames = self.nonames + 1
            name = 'unnamed'+str(self.nonames)
        self.components.update({name: comp})

    def GetComponent(self, name='unnamed'):
        return self.components[name]

    def GetLinks(self):
        return self.links
    
    def SetReferencePoint(self, position):
        self.refpoint = chrono.ChVectorD(position[0], position[1], position[2])
    def GetReferencePoint(self):
        return self.refpoint

    
    def Fixate(self, name, permanent = False):
        if name in self.components:
            self.components[name].GetBody().SetBodyFixed(True)
            if not permanent:
                self.fixed.append(name)
    
    def Release(self):
        for name in self.fixed:
            self.components[name].GetBody().SetBodyFixed(False)
        self.fixed = []
    
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

    def ChuteUp(self, name_A, point_A, name_chute):
        comp_A = self.components[name_A]
        comp_chute = self.components[name_chute]

        name = name_A+"_"+point_A + "_TO_" + name_chute

        self.GetComponent(name_chute).MoveToMatch('A', self.GetComponent(name_A), point_A)
        
        mlink = chrono.ChLinkTSDA()
        # the coordinate system of the constraint reference in abs. space:
        # mframe = chrono.ChFrameD(comp_B.GetLinkPoint(point_B), comp_B.GetBody().GetRot())
        # mframe = chrono.ChCoordsysD(comp_B.GetLinkPoint(point_B), comp_B.GetBody().GetRot())
        # initialize the constraint telling which part must be connected, and where:
        mlink.Initialize(comp_A.GetBody(), comp_chute.GetBody(), False, comp_A.GetLinkPoint(point_A), comp_chute.GetLinkPoint('B'))
        # mlink.RegisterForceFunctor()
        # chrono.ForceFunctor()
        mlink.SetSpringCoefficient(0.02)
        mlink.SetDampingCoefficient(0.001)
        mlink.SetRestLength(1)

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
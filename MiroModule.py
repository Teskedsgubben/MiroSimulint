import pychrono.core as chrono

class Module():
    def __init__(self):
        self.components = {}
        self.links = {}
        self.nonames = 0
        self.fixed = []
    
    def AddComponent(self, comp, name='unnamed'):
        if(name == 'unnamed'):
            self.nonames = self.nonames + 1
            name = 'unnamed'+str(self.nonames)
        self.components.update({name: comp})

    def GetComponent(self, name='unnamed'):
        return self.components[name]

    def GetLinks(self):
        return self.links
    
    def Fixate(self, name, permanent = False):
        self.perm = permanent
        if name in self.components:
            self.fixed.append(name)
            self.components[name].GetBody().SetBodyFixed(True)
    
    def Release(self):
        for name in self.fixed:
            if not self.perm:
                self.components[name].GetBody().SetBodyFixed(False)
        self.fixed = []
    
    def ConnectComponents(self, name_A, point_A, name_B, point_B, move = True):
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"_"+point_A + "_TO_" + name_B+"_"+point_B

        if(move):
            self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A)

        
        # Create a universal link constraint
        mlink = chrono.ChLinkRevolute()
        # the coordinate system of the constraint reference in abs. space:
        mframe = chrono.ChFrameD(comp_B.GetLinkPoint(point_B), comp_B.GetBody().GetRot())
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
        for _, comp in self.components.items():
            comp.MoveBy(distance)
    
    def SetVelocity(self, vel):
        for _, comp in self.components.items():
            comp.SetVelocity(vel)
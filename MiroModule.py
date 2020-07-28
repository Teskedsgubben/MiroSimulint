import pychrono.core as chrono

class Module():
    def __init__(self):
        self.components = {}
        self.links = {}
        self.nonames = 0
    
    def AddComponent(self, comp, name='unnamed'):
        if(name == 'unnamed'):
            self.nonames = self.nonames + 1
            name = 'unnamed'+str(self.nonames)
        self.components.update({name: comp})

    def GetComponent(self, name='unnamed'):
        return self.components[name]
    
    def ConnectComponents(self, name_A, point_A, name_B, point_B, move = True):
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"_"+point_A + "_TO_" + name_B+"_"+point_B

        if(move):
            self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A)

        # Create a revolute constraint
        mlink = chrono.ChLinkRevolute()
        
        # the coordinate system of the constraint reference in abs. space:
        mframe = chrono.ChFrameD(comp_B.GetLinkPoint(point_B), comp_B.GetBody().GetRot())

        # initialize the constraint telling which part must be connected, and where:
        mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), mframe)
        
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
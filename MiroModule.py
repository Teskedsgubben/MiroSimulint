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



######### NOTES

def PendulumLander(system):

    pos = chrono.ChVectorD(1,2,-0.4)
    size_brick_x = 0.2
    size_brick_y = 0.5
    size_brick_z = 0.1
    
    # Create a fixed rigid body
    
    mbody1 = chrono.ChBody()
    mbody1.SetBodyFixed(False)
    mbody1.SetCollide(True)
    mbody1.SetPos( pos )
    
    # Collision shape
    mass_brick = 1000 * size_brick_x * size_brick_y * size_brick_z
    inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    mbody1.SetMass(mass_brick)
    mbody1.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))  
    mbody1.GetCollisionModel().ClearModel()
    mbody1.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    mbody1.GetCollisionModel().BuildModel()

    system.Add(mbody1)

    mboxasset = chrono.ChBoxShape()
    mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(size_brick_x, size_brick_y, size_brick_z)
    mbody1.AddAsset(mboxasset)

    
    # Create a swinging rigid body
    
    mbody2 = chrono.ChBody()
    mbody2.SetBodyFixed(False)
    mbody2.SetCollide(True)
    mbody2.SetPos( pos - chrono.ChVectorD(0,0,0.2))

    # Collision shape
    mass_brick = 1000 * size_brick_x * size_brick_y * size_brick_z
    inertia_brick = 2/5*(pow(size_brick_x,2))*mass_brick # to do: compute separate xx,yy,zz inertias
    mbody2.SetMass(mass_brick)
    mbody2.SetInertiaXX(chrono.ChVectorD(inertia_brick,inertia_brick,inertia_brick))  
    mbody2.GetCollisionModel().ClearModel()
    mbody2.GetCollisionModel().AddBox(size_brick_x/2, size_brick_y/2, size_brick_z/2) # must set half sizes
    mbody2.GetCollisionModel().BuildModel()

    system.Add(mbody2)
    
    mboxasset = chrono.ChBoxShape()
    mboxasset.GetBoxGeometry().Size = chrono.ChVectorD(0.2,0.5,0.1)
    mbody2.AddAsset(mboxasset)
    
    mboxtexture = chrono.ChTexture()
    mboxtexture.SetTextureFilename(chrono.GetChronoDataFile('textures/wood_floor.jpg'))
    mbody2.GetAssets().push_back(mboxtexture)
    
    
    # Create a revolute constraint
    
    mlink = chrono.ChLinkRevolute()
    
        # the coordinate system of the constraint reference in abs. space:
    mframe = chrono.ChFrameD(pos + chrono.ChVectorD(0.1,0.3,0))
    
        # initialize the constraint telling which part must be connected, and where:
    mlink.Initialize(mbody1,mbody2, mframe)
    
    system.Add(mlink)
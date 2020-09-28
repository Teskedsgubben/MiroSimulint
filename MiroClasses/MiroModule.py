import pychrono.core as chrono
import numpy as np

class Module():
    def __init__(self):
        self.components = {}
        self.sensors = {}
        self.links = {}
        self.nonames_comp = 0
        self.nonames_sens = 0
        self.nonames_boos = 0
        self.fixed = []
        self.refpoint = False
        self.refcomp = False
        self.base = False
        self.mass = 0

        # Extra bodies or links for props, not to be counted into module
        self.hidden_bodies = []
        self.hidden_links = []

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
        self.mass = self.mass + comp.GetMass()

    def AddBooster(self, booster, name='unnamed'):
        if(name == 'unnamed'):
            self.nonames_boos = self.nonames_boos + 1
            name = 'unnamed_booster'+str(self.nonames_boos)
        self.AddSensor(booster, name)
    
    def AddSensor(self, sensor, name='unnamed'):
        if(name == 'unnamed'):
            self.nonames_sens = self.nonames_sens + 1
            name = 'unnamed_sensor'+str(self.nonames_sens)
        self.sensors.update({name: sensor})
        self.AddComponent(sensor, name)

    def GetBasePosition(self):
        if self.base:
            return self.base.GetPosition()
        else:
            return chrono.ChVectorD(0,0,0)

    def GetMass(self):
        return self.mass
    
    def GetCenterOfMass(self):
        mass_center = chrono.ChVectorD(0,0,0)
        M = self.GetMass()
        for _, comp in self.components.items():
            addpos = chrono.ChVectorD(comp.GetPosition())
            addpos.Scale(comp.GetMass()/M)
            mass_center.Add(mass_center, addpos)
        return mass_center        

    def GetComponent(self, name='unnamed'):
        return self.components[name]

    def GetSensor(self, name='unnamed'):
        return self.sensors[name]
    def GetSensorList(self):
        return self.sensors

    def GetLinks(self):
        return self.links
    
    def SetReferencePoint(self, position):
        '''Stores a coordinate relative the module. Is overriden if a reference component is set.'''
        self.refpoint = chrono.ChVectorD(position[0], position[1], position[2])

    def GetReferencePoint(self):
        '''Returns the reference point stored in the module. If both a reference component is set, it is used. Otherwise returns the manually set reference point. If neither are set, returns the base position.'''
        if self.refcomp:
            return self.components[self.refcomp].GetBody().GetPos() + self.refcomp_relpos
        elif self.refpoint:
            return self.refpoint
        else:
            return self.GetBasePosition()

    def SetReferenceComponent(self, component_name, relative_position):
        '''Stores a component of the module to use as a basis for the reference point. Set a relative position as [x, y, z] to put the reference point somewhere relative to the component. 
        This vector does not rotate with the component. This method overrides SetReferencePoint.'''
        if component_name in self.components:
            if type(relative_position) == type([]):
                relative_position = chrono.ChVectorD(relative_position[0], relative_position[1], relative_position[2])
            self.refcomp = component_name
            self.refcomp_relpos = relative_position

    def Fixate(self, name, permanent = False):
        ''' Locks a component in place. Component is then set loose upon calling Release on the modulem, unless True is passed for permanent fixation.'''
        if name in self.components:
            self.components[name].GetBody().SetBodyFixed(True)
            if not permanent:
                self.fixed.append(name)
    
    def Release(self):
        '''Changes the state of any non permanently fixed components to non-fixed.'''
        for name in self.fixed:
            self.components[name].GetBody().SetBodyFixed(False)
        self.fixed = []

    def GetLinkPointXYZ(self, component_name, linkpoint_name):
        return self.GetComponent(component_name).GetLinkPointXYZ(linkpoint_name)
    
    def MarkLinkpoint(self, component_name, linkpoint_name, color = 'red', marking_radius = 0.01):
        '''Add a colored sphere to the linkpoint of a component to identify it during simulation. \nUse 'red', 'blue' or 'green'.'''
        texture = chrono.ChTexture()
        if color != 'blue' and color != 'green':
            color = 'red'
        texture.SetTextureFilename(chrono.GetChronoDataFile('textures/markpattern_'+color+'.png'))
        texture.SetTextureScale(1, 1)

        comp = self.components[component_name]

        ball = chrono.ChBody()
        ball.SetBodyFixed(False)
        ball.SetCollide(False)  
        ball_shape = chrono.ChSphereShape(chrono.ChSphere(chrono.ChVectorD(0, 0, 0), marking_radius))
        ball.AddAsset(ball_shape)
        ball.AddAsset(texture)
        ball.SetPos(comp.GetLinkPoint(linkpoint_name))

        mlink = chrono.ChLinkRevolute()
        mlink.Initialize(comp.GetBody(), ball, chrono.ChFrameD(ball.GetPos()))

        self.hidden_bodies.append(ball)
        self.hidden_links.append(mlink)

    def MarkComponent(self, component_name, color = 'red'):
        '''Change the color of a component to identify it during simulation. \nUse 'red', 'blue' or 'green'.'''
        texture = chrono.ChTexture()
        if color != 'blue' and color != 'green':
            color = 'red'
        texture.SetTextureFilename(chrono.GetChronoDataFile('textures/markpattern_'+color+'.png'))
        texture.SetTextureScale(4, 3)
        self.components[component_name].GetBody().AddAsset(texture)

    def ConnectComponents(self, name_A, point_A, name_B, point_B, dist = 0, move = True, show_warning = True):
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"."+point_A + "_TO_" + name_B+"."+point_B

        if(move):
            self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A, dist)

        # Set Link position to the midpoint between the linkpoints
        linkpos = chrono.ChVectorD()
        linkpos.Mul(comp_A.GetLinkPoint(point_A) + comp_B.GetLinkPoint(point_B), 1/2)
        
        # Get both link directions from the components
        linkdirA = chrono.ChVectorD(comp_A.GetLinkDir(point_A))
        linkdirB = chrono.ChVectorD(comp_B.GetLinkDir(point_B))

        # If the dot product is negative, then the angle between the links is > 180 degrees and the links are at least somewhat facing
        if linkdirA.Length() == 0:
            linkdir = linkdirB
        elif linkdirB.Length() == 0:
            linkdir = linkdirA
        elif linkdirA.Dot(linkdirB) < 0:
            linkdir = (linkdirA - linkdirB).GetNormalized()
        else: 
            linkdir = (linkdirA + linkdirB).GetNormalized()
            if show_warning:
                print('Warning: Non-facing links. The links between '+name_A+'.'+point_A+' and '+name_B+'.'+point_B+' are not facing eachother, check linkpoint and object orientation.')            

        # Get the quaternion that represents the rotation of the global z-axis to the link direction
        z_ax = chrono.ChVectorD(0,0,1)
        q = chrono.ChQuaternionD(1 + z_ax.Dot(linkdir), z_ax.Cross(linkdir))
        q.Normalize()

        # # Print link direction and the linkframe's z-direction for debugging
        # mframe_zax = q.GetZaxis().GetNormalized()
        # print('     linkdirection: ', [format(linkdir.x, '.2f'), format(linkdir.y, '.2f'), format(linkdir.z, '.2f')])
        # print('      mframe z-dir: ', [format(mframe_zax.x, '.2f'), format(mframe_zax.y, '.2f'), format(mframe_zax.z, '.2f')])
        
        # Create a new ChFrame coordinate system at the link position and with the global_z-to-linkdir rotation
        mframe = chrono.ChFrameD(linkpos, q)

        # Create a revolute link between the components at the coordinate system
        mlink = chrono.ChLinkRevolute()
        mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), mframe)
        
        # Add the link to the module's dictionary of links
        self.links.update({name: mlink})

    def ConnectComponents_old(self, name_A, point_A, name_B, point_B, dist = 0, move = True):
        '''This function sets improper link constraints, but remains accessible in case any 
        modules where based on improper links holding it in place. This function will be removed 
        once the project week of 2020 has concluded.'''
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

    def SetSpring(self, name_A, point_A, name_B, point_B, L, K, marking_color = [0.5, 0.1, 0.1], marking_radius = 0.005, draw_spring = False, spring_radius = 0.005, spring_turns = 40):
        '''Sets a spring of rest length L and spring constant K between the points on components A and B in the module. 
        Marks the connection points with a non-interactive sphere on each end. To remove marking spheres, set marking radius to 0.''' 
        
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"_"+point_A + "_TO_" + name_B+"_"+point_B

        mlink = chrono.ChLinkTSDA()
        mlink.Initialize(comp_A.GetBody(), comp_B.GetBody(), False, comp_A.GetLinkPoint(point_A), comp_B.GetLinkPoint(point_B))
        mlink.SetSpringCoefficient(K)
        mlink.SetDampingCoefficient(K/200)
        if draw_spring:
            mlink.AddAsset(chrono.ChPointPointSpring(spring_radius, 15*spring_turns, spring_turns))
        mlink.SetRestLength(L)

        self.links.update({name: mlink})

        if marking_radius > 0:
            ball_A = chrono.ChBody()
            ball_A.SetBodyFixed(False)
            ball_A.SetCollide(False)  
            ball_shape = chrono.ChSphereShape(chrono.ChSphere(chrono.ChVectorD(0, 0, 0), marking_radius))
            ball_A.AddAsset(ball_shape)
            ball_A.AddAsset(chrono.ChColorAsset(chrono.ChColor(marking_color[0], marking_color[1], marking_color[2])))
            ball_A.SetPos(comp_A.GetLinkPoint(point_A))

            ball_B = chrono.ChBody(ball_A)
            ball_B.SetPos(comp_B.GetLinkPoint(point_B))

            mlinkA = chrono.ChLinkRevolute()
            mlinkA.Initialize(comp_A.GetBody(), ball_A, chrono.ChFrameD(ball_A.GetPos()))

            mlinkB = chrono.ChLinkRevolute()
            mlinkB.Initialize(comp_B.GetBody(), ball_B, chrono.ChFrameD(ball_B.GetPos()))

            # This adds the ball markers to the system
            self.hidden_bodies.append(ball_A)
            self.hidden_links.append(mlinkA)
            self.hidden_bodies.append(ball_B)
            self.hidden_links.append(mlinkB)

    def AddToSystem(self, system):
        for _, comp in self.components.items():
            comp.AddToSystem(system)
        for _, link in self.links.items():
            system.Add_Object(link)
        for hidbod in self.hidden_bodies:
            system.Add_Object(hidbod)
        for hidlink in self.hidden_links:
            system.Add_Object(hidlink)

    def Move(self, displacement):
        if(self.refpoint):
            self.refpoint.Add(self.refpoint, chrono.ChVectorD(displacement[0], displacement[1], displacement[2]))
        for _, comp in self.components.items():
            comp.MoveBy(displacement)
        for hidbod in self.hidden_bodies:
            hidbod.Move(chrono.ChVectorD(displacement[0], displacement[1], displacement[2]))

    def SetPosition(self, pos):
        '''Set the position of the entire module. Base component position gets the provided position as its coordinate.'''
        p = self.base.GetPosition()
        self.Move([pos.x-p.x, pos.y-p.y, pos.z-p.z])    
    
    def MovetoMatch(self, name_A, point_A, name_B, point_B, dist = 0):
        '''Moves the second component (component B) to match a linkpoint position with the position of a 
        linkpoint on the first component (component A). Distance is calculated in the direction of the 
        linkpoint on the non-moving component (component A).'''
        self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A, dist)

    def MoveComponentBy(self, component_name, displacement = [0,0,0]):
        '''Moves the component from its current position by the specified displacement.'''
        if component_name not in self.components:
            return
        if type(displacement) == type([]):
            displacement = chrono.ChVectorD(displacement[0], displacement[1], displacement[2])
        comp = self.components[component_name]
        comp.MoveBy(displacement)

    def MoveComponentTo(self, component_name, position = [0,0,0]):
        '''Moves the component to the specified position.'''
        if component_name not in self.components:
            return
        if type(position) == type([]):
            position = chrono.ChVectorD(position[0], position[1], position[2])
        comp = self.components[component_name]
        comp.MoveToPosition(position)
        
    def SetVelocity(self, vel):
        '''Sets the velocity of all components in the module'''
        for _, comp in self.components.items():
            comp.SetVelocity(vel)

    def Rotate(self, component_name, theta, axis):
        '''Rotates a specific component in the module theta degrees about the provided axis.'''
        if not component_name in self.components:
            print('Cannot rotate '+component_name+', component not found.')
            return
        comp = self.components[component_name]
        angle = theta/180*np.pi
        ax = chrono.ChVectorD(axis[0], axis[1], axis[2])
        qr = chrono.Q_from_AngAxis(angle, ax.GetNormalized())
        comp.Rotate(False, qr)

    def RotateX(self, component_name, theta):
        '''Rotates a specific component in the module theta degrees about the X-axis.'''
        self.Rotate(component_name, theta, [1,0,0])
    def RotateY(self, component_name, theta):
        '''Rotates a specific component in the module theta degrees about the Y-axis.'''
        self.Rotate(component_name, theta, [0,1,0])
    def RotateZ(self, component_name, theta):
        '''Rotates a specific component in the module theta degrees about the Z-axis.'''
        self.Rotate(component_name, theta, [0,0,1])

    def RotateComponents(self, theta, axis):
        '''Rotates all components in the module theta degrees about the provided axis.'''
        angle = theta/180*np.pi
        ax = chrono.ChVectorD(axis[0], axis[1], axis[2])
        qr = chrono.Q_from_AngAxis(angle, ax.GetNormalized())
        for _, comp in self.components.items():
            comp.Rotate(False, qr)
        if self.refpoint:
            vec = qr.Rotate(self.refpoint)
            self.refpoint = vec

    def RotateComponentsX(self, theta):
        '''Rotates all components in the module theta degrees about the X-axis.'''
        self.RotateComponents(theta, [1,0,0])
    def RotateComponentsY(self, theta):
        '''Rotates all components in the module theta degrees about the Y-axis.'''
        self.RotateComponents(theta, [0,1,0])
    def RotateComponentsZ(self, theta):
        '''Rotates all components in the module theta degrees about the Z-axis.'''
        self.RotateComponents(theta, [0,0,1])
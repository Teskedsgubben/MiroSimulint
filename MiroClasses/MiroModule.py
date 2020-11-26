from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np
from NodeMap import NodeMap

class Module():
    def __init__(self, name=False):
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
        self.name = name
        self.graph_nodes=[]
        self.graph_links=[]

        # Extra bodies or links for props, not to be counted into module
        self.hidden_bodies = []
        self.hidden_links = []
        self.use_helpers = True
        self.warning_print = True

    def PrintInfo(self):
        print('  Sensors: '+str(len(self.sensors.keys())))
        if len(self.sensors.keys()) > 0:
            for sensor_name in self.sensors.keys():
                print('    - '+sensor_name)
        print('  Components: '+str(len(self.components.keys()) - len(self.sensors.keys())))
        print('  Connections: '+str(len(self.links.keys())))
        print('  Mass: %.3f kg' % (round(self.GetMass(),2)))
        
    def CreateModuleMap(self):
        NodeMap.WriteGraph(self.graph_links)
    
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
            return np.array([0,0,0])

    def GetMass(self):
        return self.mass
    
    def GetCenterOfMass(self):
        mass_center = np.array([0,0,0])
        M = self.GetMass()
        for _, comp in self.components.items():
            addpos = np.array(comp.GetPosition())*comp.GetMass()/M
            mass_center = mass_center + addpos
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
        self.refpoint = np.array(position)

    def SetReferenceComponent(self, component_name, relative_position):
        '''Stores a component of the module to use as a basis for the reference point. Set a relative position as [x, y, z] to put the reference point somewhere relative to the component. 
        This vector does not rotate with the component. This method overrides SetReferencePoint.'''
        if component_name in self.components:
            self.refcomp = component_name
            self.refcomp_relpos = np.array(relative_position)

    def GetReferencePoint(self):
        '''Returns the reference point stored in the module. If both a reference component is set, it is used. Otherwise returns the manually set reference point. If neither are set, returns the base position.'''
        if self.refcomp:
            return self.components[self.refcomp].GetPosition() + self.refcomp_relpos
        elif self.refpoint:
            return self.refpoint
        else:
            return self.GetBasePosition()

    def Fixate(self, name, permanent = False):
        ''' Locks a component in place. Component is then set loose upon calling Release on the modulem, unless True is passed for permanent fixation.'''
        if name in self.components:
            MiroAPI.SetBodyFixed(self.components[name].GetBody())
            if not permanent:
                self.fixed.append(name)
    
    def Release(self):
        '''Changes the state of any non permanently fixed components to non-fixed.'''
        for name in self.fixed:
            MiroAPI.SetBodyFixed(self.components[name].GetBody(), False)
        self.fixed = []

    def GetLinkPointXYZ(self, component_name, linkpoint_name):
        return self.GetComponent(component_name).GetLinkPointXYZ(linkpoint_name)
    
    def MarkLinkpoint(self, component_name, linkpoint_name, color = 'red', marking_radius = 0.01):
        '''Add a colored sphere to the linkpoint of a component to identify it during simulation. \nUse 'red', 'blue' or 'green'.'''
        if not self.use_helpers:
            return

        if color != 'blue' and color != 'green':
            color = 'red'
        
        if MiroAPI.API == 'AGX' and self.warning_print:
            print('Warning: MiroModule.MarkLinkPoint is not stable in the AGX api, may cause unstable systems. Consider using MiroModule.DisableHelpers().')
        
        texture = 'textures/markpattern_'+color+'.png'
        backup_color = [(color=='red')*1, (color=='green')*1, (color=='blue')*1]

        comp = self.components[component_name]
        pos = comp.GetLinkPoint(linkpoint_name)
        ball = MiroAPI.add_sphereShape(False, marking_radius, pos, texture=texture, Collide=False, Fixed=False, color=backup_color)
        link = MiroAPI.LinkBodies_Hinge(comp.GetBody(), ball, pos, [0,1,0])

        self.hidden_bodies.append(ball)
        self.hidden_links.append(link)

    def MarkComponent(self, component_name, color = 'red'):
        '''Change the color of a component to identify it during simulation. \nUse 'red', 'blue' or 'green'.'''
        if MiroAPI.API == 'PyChrono':
            if color != 'blue' and color != 'green':
                color = 'red'
            MiroAPI.ChangeBodyTexture(self.components[component_name].GetBody(), 'textures/markpattern_'+color+'.png')
        else:
            print('MarkComponent is currently only supported in the chrono API')

    def ConnectComponents(self, name_A, point_A, name_B, point_B, dist = 0, move = True, show_warning = True):
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"."+point_A + "_TO_" + name_B+"."+point_B

        if(move):
            self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A, dist)

        # Set Link position to the midpoint between the linkpoints
        linkpos = (comp_A.GetLinkPoint(point_A) + comp_B.GetLinkPoint(point_B))/2
        
        # Get both link directions from the components
        linkdirA = comp_A.GetLinkDir(point_A)
        linkdirB = comp_B.GetLinkDir(point_B)

        # If the dot product is negative, then the angle between the links is > 180 degrees and the links are at least somewhat facing
        if np.linalg.norm(linkdirA) == 0:
            linkdir = linkdirB
        elif np.linalg.norm(linkdirB) == 0:
            linkdir = linkdirA
        elif np.dot(linkdirA, linkdirB) < 0:
            linkdir = linkdirA - linkdirB
            linkdir = linkdir/np.linalg.norm(linkdir)
        else: 
            linkdir = linkdirA + linkdirB
            linkdir = linkdir/np.linalg.norm(linkdir)
            if show_warning:
                print('Warning: Non-facing links. The links between '+name_A+'.'+point_A+' and '+name_B+'.'+point_B+' are not facing eachother, check linkpoint and object orientation. Consider removing with MiroModule.RemoveHelpers() before running.')            

        hinge_link = MiroAPI.LinkBodies_Hinge(comp_A.GetBody(), comp_B.GetBody(), linkpos, linkdir)
        
        # Add the link to the module's dictionary of links
        self.links.update({name: hinge_link})
        self.graph_links.append({'Source': name_A, 'Target': name_B, 'Weight': 1})

    def SetSpring(self, name_A, point_A, name_B, point_B, L, K, marking_radius = 0.005, draw_spring = False, spring_radius = 0.005, spring_turns = 40):
        '''Sets a spring of rest length L and spring constant K between the points on components A and B in the module. 
        Marks the connection points with a non-interactive sphere on each end. To remove marking spheres, set marking radius to 0.''' 
        
        comp_A = self.components[name_A]
        comp_B = self.components[name_B]

        name = name_A+"_"+point_A + "_TO_" + name_B+"_"+point_B

        bodA = comp_A.GetBody()
        posA = comp_A.GetLinkPoint(point_A)
        bodB = comp_B.GetBody()
        posB = comp_B.GetLinkPoint(point_B)

        if(MiroAPI.API == 'AGX' and draw_spring and self.warning_print):
            print('Drawing springs is currently only supported in the chrono API')
        spring_link = MiroAPI.LinkBodies_Spring(bodA, posA, bodB, posB, L, K, K/200, visible=draw_spring, spring_radius = spring_radius, spring_turns = spring_turns)
        
        self.links.update({name: spring_link})

        if marking_radius > 0 and self.use_helpers:
            self.MarkLinkpoint(name_A, point_A, marking_radius=marking_radius)
            self.MarkLinkpoint(name_B, point_B, marking_radius=marking_radius)

    def AddToSystem(self, MiroSystem):
        for _, comp in self.components.items():
            comp.AddToSystem(MiroSystem)
        for _, link in self.links.items():
            MiroSystem.Add(link)
        for hidbod in self.hidden_bodies:
            MiroSystem.Add(hidbod)
        for hidlink in self.hidden_links:
            MiroSystem.Add(hidlink)

    def Move(self, displacement):
        if(self.refpoint):
            self.refpoint = self.refpoint + np.array(displacement)
        for _, comp in self.components.items():
            comp.MoveBy(displacement)
        for hidbod in self.hidden_bodies:
            MiroAPI.MoveBodyBy(hidbod, displacement)

    def SetPosition(self, pos):
        '''Set the position of the entire module. Base component position gets the provided position as its coordinate.'''
        new_pos = np.array(pos)
        curr_pos = self.GetBasePosition()
        self.Move(new_pos - curr_pos)    
    
    def MovetoMatch(self, name_A, point_A, name_B, point_B, dist = 0):
        '''Moves the second component (component B) to match a linkpoint position with the position of a 
        linkpoint on the first component (component A). Distance is calculated in the direction of the 
        linkpoint on the non-moving component (component A).'''
        self.GetComponent(name_B).MoveToMatch(point_B, self.GetComponent(name_A), point_A, dist)

    def MoveComponentBy(self, component_name, displacement = [0,0,0]):
        '''Moves the component from its current position by the specified displacement.'''
        if component_name not in self.components:
            return
        comp = self.components[component_name]
        comp.MoveBy(displacement)

    def MoveComponentTo(self, component_name, position = [0,0,0]):
        '''Moves the component to the specified position.'''
        if component_name not in self.components:
            return
        comp = self.components[component_name]
        comp.MoveToPosition(position)
        
    def SetVelocity(self, vel):
        '''Sets the velocity of all components in the module'''
        for _, comp in self.components.items():
            comp.SetVelocity(vel)

    def Rotate(self, component_name, theta, axis):
        '''Rotates a specific component in the module theta degrees about the provided axis.'''
        if type(component_name) == type([]):
            component_list = component_name
        else:
            component_list = [component_name]
        for comp_name in component_list:
            if not comp_name in self.components:
                print('Cannot rotate '+comp_name+', component not found.')
            else:
                comp = self.components[comp_name]
                comp.RotateAxis(theta, axis)

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
        for _, comp in self.components.items():
            comp.RotateAxis(theta, axis)
        if self.refpoint:
            self.refpoint = MiroAPI.rotateVector(self.refpoint, theta, axis)
        if self.refcomp:
            self.refcomp_relpos = MiroAPI.rotateVector(self.refcomp_relpos, theta, axis)

    def RotateComponentsX(self, theta):
        '''Rotates all components in the module theta degrees about the X-axis.'''
        self.RotateComponents(theta, [1,0,0])
    def RotateComponentsY(self, theta):
        '''Rotates all components in the module theta degrees about the Y-axis.'''
        self.RotateComponents(theta, [0,1,0])
    def RotateComponentsZ(self, theta):
        '''Rotates all components in the module theta degrees about the Z-axis.'''
        self.RotateComponents(theta, [0,0,1])

    def SetTexture(self, component_name, texture_file, scale=[4,3]):
        if type(component_name) == type([]):
            component_list = component_name
        else:
            component_list = [component_name]
        for comp_name in component_list:
            if not comp_name in self.components:
                print('Cannot texturize '+comp_name+', component not found.')
            else:
                comp = self.components[comp_name]
                comp.SetTexture(texture_file, scale)

    def DisableHelpers(self, only_suppress_warning = False, remove_existing=True, remove_future=True):
        '''This removes all visual help objects, including marked linkpoints and spring attachments.\n
        Set only_suppress_warnings=True as input to turn off the warning print but keep the helper objects.\n
        You can also control if you do not want to remove existing helpers, or only stop adding future helpers
        after this command is executed.'''
        self.warning_print = False
        if not only_suppress_warning:
            if remove_existing:
                self.hidden_bodies = []
                self.hidden_links = []
            if remove_future:
                self.use_helpers = False
        
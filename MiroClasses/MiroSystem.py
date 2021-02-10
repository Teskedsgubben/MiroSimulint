from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
import numpy as np
import sys
import time
import os

def MiroSetup(SetupFunction):
    MiroAPI.PreSetup(sys.argv, SetupFunction)

class MiroSystem():
    def __init__(self): 
        # The path to the Chrono data directory containing various assets (meshes, textures, data files)
        # is automatically set, relative to the default location of this demo.
        # If running from a different directory, you must change the path to the data directory with: 
        #chrono.SetChronoDataPath('path/to/data')
        
        # ---------------------------------------------------------------------
        #
        #  Create the simulation system and add items
        #
        self.system_list = MiroAPI.SetupSystem()
        self.modules = {}
        self.sensors = {}
        self.links = {}

        self.SPEEDMODE = False
        self.notifier = False
        self.released = False
        
        # Camera properties
        self.follow = False
        self.cycle = False
        self.fps = 300
        self.camera_sweep = False
        self.sweep_cam = []
        self.sweep_obs = []
        self.sweepstep = 0
        self.sweepnr = 0

        #tests camera properties
        self.follow_distance = 3
        self.follow_height = 0.5
        self.follow_default = False
        self.camviews = {
            'default': {
                'pos': [0, 3, 0],
                'dir': [1,0,0],
                'lah': 3
            }
        }
        
    def Set_Speedmode(self, SPEEDMODE = True):
        '''Sets if speedmode is to be used. This removes many visual items to speed up the simulation.'''
        self.SPEEDMODE = SPEEDMODE

    def Set_Environment(self, Environment):
        
        self.Environment = Environment
        self.Environment.Initialize(self, self.SPEEDMODE)
        self.camviews.update(self.Environment.Get_Camviews())

        if self.Environment.Has_Notifier():
            self.notifier = True
            self.Environment.Get_Notifier().AddToSystem(self)
            self.Environment.Get_Notifier().Set_Idle()

        cam = self.camviews['default']
        self.cam_pos = np.array(cam['pos'])
        self.cam_to_obs = np.array(cam['dir'])/np.linalg.norm(np.array(cam['dir']))
        self.cam_to_obs = self.cam_to_obs*cam['lah']
        self.obs_pos = self.cam_pos + self.cam_to_obs
    
    def Get_Environment(self):
        return self.Environment

    def Get_Target(self):
        return self.Environment.Get_Target()

    def Get_APIsystem(self):
        return self.system_list
    
    def Set_Perspective(self, camname, follow_module_name = False, follow_position = [1.5, 0.75, 0], follow_distance = 0, cycle = False, cycle_laptime = 4, follow_height=0.5):
        '''Sets the camera perspective configuration for the simulation. Available perspectives depend on the MiroEnvironment used.'''
        self.follow_distance = follow_distance
        self.follow_height = follow_height
        if cycle:
            self.cycle = True
            self.cycle_angle = -2*np.pi/cycle_laptime
        if camname == 'follow_default':
            if not follow_module_name:
                print('Camera Error: Input a module name to use follow perspective, using default')
            else:
                if follow_module_name in self.modules:
                    self.follow_default = True
                    self.followmod = self.modules[follow_module_name]
                    self.cam_to_obs = -np.array(follow_position)
                    self.obs_pos = self.followmod.GetCenterOfMass()
                    self.cam_pos = self.obs_pos - self.cam_to_obs
                    if follow_distance > 0:
                        self.cam_to_obs = self.cam_to_obs/np.linalg.norm(self.cam_to_obs)*follow_distance
                else:
                    print('Camera Error: "'+follow_module_name+'" is not a recognized module and cannot be followed, using default')
        elif camname in self.camviews:
            cam = self.camviews[camname]
            self.cam_pos = np.array(cam['pos'])
            self.cam_to_obs = np.array(cam['dir'])/np.linalg.norm(np.array(cam['dir']))
            self.cam_to_obs = self.cam_to_obs*cam['lah']
            self.obs_pos = self.cam_pos + self.cam_to_obs
        else:
            if cycle:
                print('Camera Error: "'+camname+'" is not a recognized camera position, cycling default')
            else:
                print('Camera Error: "'+camname+'" is not a recognized camera position, using default')
        
        MiroAPI.SetCamera(self.system_list, self.cam_pos, self.obs_pos)


    def Add_Camview(self, name, position = [0,0,0], direction = [1,0,0], distance = 1, look_at_point = False):
        '''Add your own camera perspective to the environment. \n
        name: string 'perspective name'\n
        position: camera coordinates in [x,y,z]\n
        direction: aim of the camera in [x,y,z]\n
        distance: number of how far away the camera should look\n
        look_at_point: can be used to override direction and distance to set a specific viewing point\n
        Use Set_Perspective('your name') to use the camera position.'''
        if look_at_point:
            pos = np.array(position)
            point = np.array(look_at_point)
            diff = point - pos
            direction = [diff[0], diff[1], diff[2]]
            distance = np.linalg.norm(diff)
        
        self.camviews.update({
            name: {
                'pos': position,
                'dir': direction,
                'lah': distance
            }
        })

    def Set_Camera(self):
        '''This sets the camera during simulation. For internal usage when the simulation is being run, 
        use SetPerspective to configure the camera before running the simulation.'''
        if self.cycle:
            self.cam_to_obs = MiroAPI.rotateVector(self.cam_to_obs, self.cycle_angle/self.fps, [0,1,0], rotDegrees=False)
            self.cam_to_obs = (49*self.cam_to_obs + self.followmod.GetCenterOfMassVelocity())/50
            self.cam_to_obs = self.cam_to_obs/np.linalg.norm(self.cam_to_obs)
            self.cam_pos = self.obs_pos - self.cam_to_obs
            MiroAPI.SetCamera(self.system_list, self.cam_pos, self.obs_pos)

        
        if self.follow_default:
            
            if np.linalg.norm(self.followmod.GetCenterOfMassVelocity()) > 1e-2:
                
                #oldest working
                #cam_to_obs[0] = cam_to_obs[0] * np.cos(self.follow_angle)
                #cam_to_obs[1] = cam_to_obs[0] * np.sin(self.follow_angle)
                #cam_to_obs[2] = cam_to_obs[2] * np.cos(self.follow_angle)
                self.obs_pos = self.followmod.GetCenterOfMass()
                
                
                cam_to_obs = (self.followmod.GetCenterOfMassVelocity()/np.linalg.norm(self.followmod.GetCenterOfMassVelocity()))
                cam_to_obs *= self.follow_distance
                self.cam_pos = self.obs_pos - self.cam_to_obs
                self.cam_pos[1] += self.follow_height             # good val = 1/2
                MiroAPI.SetCamera(self.system_list, self.cam_pos, self.obs_pos)

                cam_to_obs = (49 * self.cam_to_obs + cam_to_obs)/(49 + 1)

                self.cam_to_obs = cam_to_obs
        
        if self.camera_sweep:
            i = self.sweepstep
            sweep_divs = 100
            self.cam_pos = ((sweep_divs-i)*self.sweep_cam[self.sweepnr-1]+(i)*self.sweep_cam[self.sweepnr])/sweep_divs
            self.obs_pos = ((sweep_divs-i)*self.sweep_obs[self.sweepnr-1]+(i)*self.sweep_obs[self.sweepnr])/sweep_divs
            MiroAPI.SetCamera(self.system_list, self.cam_pos, self.obs_pos) 
            self.sweepstep += 1
            if self.sweepstep > sweep_divs:
                self.sweepstep = 0
                self.sweepnr += 1
            if self.sweepnr >= self.sweepsteps:
                self.camera_sweep = False

        if not self.cycle and not self.follow:
            return

    def Set_CameraSweep(self, cam_positions, obs_positions):
           
        self.sweepsteps = min(len(cam_positions)+1, len(obs_positions)+1)
        self.sweep_cam = [np.array(cam_positions[i]) for i in range(len(cam_positions))]
        self.sweep_obs = [np.array(obs_positions[i]) for i in range(len(obs_positions))]
        self.sweep_obs.append(np.array(self.obs_pos))
        self.sweep_cam.append(np.array(self.cam_pos))
        self.camera_sweep = True
        self.sweepnr = 1
        self.sweepstep = 0

    def Add_MiroComponent(self, component, position = False, vel = False):
        component.AddToSystem(self)

    def Add_MiroModule(self, module, name, position = False, vel = False):
        '''Adds a MiroModule to the MiroSystem with a custom name. Can set an initial position and velocity.'''
        if(position):
            module.Move(position)
        if vel:
            module.SetVelocity(vel)
        module.AddToSystem(self)
        self.links.update(module.GetLinks())
        self.modules.update({name: module})
        for s_name, sensor in module.GetSensorList().items():
            sensor_ID = name+'_'+s_name
            self.sensors.update({sensor_ID: sensor})

    def Get_MiroModule(self, name):
        return self.modules[name]

    def Release_MiroModules(self):
        if not self.released:
            for _, module in self.modules.items():
                module.Release()
        self.released = True
    
    def PrintModuleInfo(self):
        print('\n--- Module Information ---')
        for name, module in self.modules.items():
            print('Module '+name+':')
            module.PrintInfo()

    def MoveToReference(self, move_module, ref_module):
        '''Moves the first module to the reference point of the second module.'''
        moveMod = self.modules[move_module]
        refMod = self.modules[ref_module]
        moveMod.SetPosition(refMod.GetReferencePoint())

    def Add(self, Object):
        '''Adds a ChBody/agxRigidBody or similar to the underlying system.'''
        MiroAPI.AddObjectByAPI(self.system_list, Object)

    def Initialize_Config(self, config):
        if "resolution" in config:
            self.res = config['resolution']
        else:
            self.res = [1280, 720]

        if "delay" in config:
            self.delay = config['delay']
        else:
            self.delay = 4

        if "fps" in config:
            self.fps = config['fps']
        else:
            self.fps = 300

        if "subframes" in config:
            self.subframes = config['subframes']
        else:
            self.subframes = 1

        if "datalog" in config:
            self.log = config['datalog']
        else:
            self.log = False

        if "pause_before_launch" in config:
            self.pre_pause = config['pause_before_launch']
        else:
            self.pre_pause = True

        if "print module info" in config:
            self.print = config['print module info']
        else:
            self.print = False
        
        if "start paused" in config:
            self.start_paused = config['start paused']
        else:
            self.start_paused = False

        if "frame save interval" in config:
            self.framesave_interval = config['frame save interval']
        else:
            self.framesave_interval = 1
            
        if "record" in config:
            self.record = config['record']
        else:
            self.record = False
    
    def Run(self, config = {}):
        '''Runs the simulation. Configuration options and their default values are:\n
        "resolution": [1280, 720]\n
        "delay":  4\n
        "fps":  300\n
        "subframes":  1\n
        "datalog": False\n
        "pause_before_launch": True\n
        "print module info": False\n
        "start paused" = False\n
        "frame save interval" = 1\n
        "record": False\n
        '''
        self.Initialize_Config(config)
        MiroAPI.RunSimulation(self)


    
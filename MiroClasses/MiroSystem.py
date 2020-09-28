import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import numpy as np
import time
import os
 
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
        
        self.ChSystem = chrono.ChSystemNSC()
        chrono.SetChronoDataPath(os.getcwd() + "/")
        self.modules = {}
        self.sensors = {}
        self.links = {}

        self.SPEEDMODE = False
        self.notifier = False
        
        # Camera properties
        self.follow = False
        self.cycle = False
        self.fps = 300
        
        # Set the default outward/inward shape margins for collision detection,
        # this is epecially important for very large or very small objects.
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.0000001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.0001)
        
        # Maybe you want to change some settings for the solver. For example you
        # might want to use SetSolverMaxIterations to set the number of iterations
        # per timestep, etc.
        
        #self.ChSystem.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
        self.ChSystem.SetSolverMaxIterations(70)
        
    def Set_Speedmode(self, SPEEDMODE = True):
        '''Sets is speedmode is to be used. This removes many visual items to speed up the simulation.'''
        self.SPEEDMODE = SPEEDMODE

    def Set_Environment(self, Environment):
        
        self.Environment = Environment
        self.Environment.Initialize(self.ChSystem, self.SPEEDMODE)
        self.camviews = self.Environment.Get_Camviews()

        if self.Environment.Has_Notifier():
            self.notifier = True
            self.Environment.Get_Notifier().AddToSystem(self)
            self.Environment.Get_Notifier().Set_Idle()

        cam = self.camviews['default']
        self.cam_pos = chrono.ChVectorD(cam['pos'][0], cam['pos'][1], cam['pos'][2])
        self.cam_to_obs = chrono.ChVectorD(cam['dir'][0], cam['dir'][1], cam['dir'][2])
        self.cam_to_obs.SetLength(cam['lah'])
        self.obs_pos = self.cam_pos + self.cam_to_obs
    
    def Get_Environment(self):
        return self.Environment

    def Get_Target(self):
        return self.Environment.Get_Target()

    def Get_ChSystem(self):
        return self.ChSystem
    
    def Set_Perspective(self, camname, follow_module_name = False, follow_position = [1.5, 0.75, 0], follow_distance = 0, cycle = False, cycle_laptime = 4):
        '''Sets the camera perspective configuration for the simulation. Available perspectives depend on the MiroEnvironment used.'''
        if cycle:
            self.cycle = True
            self.cycle_angle = -2*np.pi/cycle_laptime
        if camname == 'follow':
            if not follow_module_name:
                print('Camera Error: Input a module name to use follow perspective, using default')
            else:
                if follow_module_name in self.modules:
                    self.follow = True
                    self.followmod = self.modules[follow_module_name]
                    self.cam_to_obs = -chrono.ChVectorD(follow_position[0], follow_position[1], follow_position[2])
                    self.obs_pos = self.followmod.GetCenterOfMass()
                    self.cam_pos = self.obs_pos - self.cam_to_obs
                    if follow_distance > 0:
                        self.cam_to_obs.SetLength(follow_distance)
                else:
                    print('Camera Error: "'+follow_module_name+'" is not a recognized module and cannot be followed, using default')
        elif camname in self.camviews:
            cam = self.camviews[camname]
            self.cam_pos = chrono.ChVectorD(cam['pos'][0], cam['pos'][1], cam['pos'][2])
            self.cam_to_obs = chrono.ChVectorD(cam['dir'][0], cam['dir'][1], cam['dir'][2])
            self.cam_to_obs.SetLength(cam['lah'])
            self.obs_pos = self.cam_pos + self.cam_to_obs
        else:
            if cycle:
                print('Camera Error: "'+camname+'" is not a recognized camera position, cycling default')
            else:
                print('Camera Error: "'+camname+'" is not a recognized camera position, using default')
        

    def Add_Camview(self, name, position = [0,0,0], direction = [1,0,0], distance = 1):
        '''Add your own camera perspective to the environment. \n
        name: string 'perspective name'\n
        position: camera coordinates in [x,y,z]\n
        direction: aim of the camera in [x,y,z]\n
        distance: number of how far away the camera should look\n
        Use Set_Perspective('your name') to use the camera position.'''
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
            q = chrono.Q_from_AngAxis(self.cycle_angle/self.fps, chrono.ChVectorD(0,1,0))
            self.cam_to_obs = q.Rotate(self.cam_to_obs)
        if self.follow:
            self.obs_pos = self.followmod.GetCenterOfMass()
        self.cam_pos = self.obs_pos - self.cam_to_obs
        position = chronoirr.vector3df(self.cam_pos.x, self.cam_pos.y, self.cam_pos.z)
        looker = chronoirr.vector3df(self.obs_pos.x, self.obs_pos.y, self.obs_pos.z)
        self.simulation.AddTypicalCamera(position, looker)

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

    def Add_Object(self, Object):
        '''Adds a ChBody or similar object to the ChSystem under the MiroSystem.'''
        self.ChSystem.Add(Object)

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
            self.record = 1
    
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
        # ---------------------------------------------------------------------
        #
        #  Create an Irrlicht application to visualize the system
        #
        self.Initialize_Config(config)
        
        self.simulation = chronoirr.ChIrrApp(self.ChSystem, 'MiroSimulation', chronoirr.dimension2du(self.res[0], self.res[1]))
        self.simulation.SetVideoframeSave(self.record)
        self.simulation.AddTypicalSky()
        self.Set_Camera()
        self.Set_Lights(True)
        
                    # ==IMPORTANT!== Use this function for adding a ChIrrNodeAsset to all items
                    # in the system. These ChIrrNodeAsset assets are 'proxies' to the Irrlicht meshes.
                    # If you need a finer control on which item really needs a visualization proxy in
                    # Irrlicht, just use application.AssetBind(myitem); on a per-item basis.
        
        self.simulation.AssetBindAll()
        
                    # ==IMPORTANT!== Use this function for 'converting' into Irrlicht meshes the assets
                    # that you added to the bodies into 3D shapes, they can be visualized by Irrlicht!
        
        self.simulation.AssetUpdateAll()
        
                    # If you want to show shadows because you used "AddLightWithShadow()'
                    # you must remember this:
        self.simulation.AddShadowAll() 
        # ---------------------------------------------------------------------
        #
        #  Run the simulation
        #
        
        dt = 1/self.fps # per frame
        substeps = self.subframes

        self.simulation.SetTimestep(dt/substeps)
        self.simulation.SetTryRealtime(True)
        self.simulation.SetVideoframeSaveInterval(self.framesave_interval)
        
        if self.start_paused:
            self.simulation.SetPaused(True)
            paused = True
        else:
            paused = False

        

        if self.log:
            for sensor_ID, sensor in self.sensors.items():
                sensor.Initialize(sensor_ID+'.txt', self.simulation)

        self.simulation.GetDevice().run()
        self.simulation.BeginScene()
        self.simulation.DrawAll()
        self.simulation.DoStep()
        self.simulation.EndScene()

        if self.print:
            self.PrintModuleInfo()
        
        start = time.time()
        
        while(self.simulation.GetDevice().run() and start + self.delay > time.time()):
            self.simulation.BeginScene()
            self.simulation.DrawAll()
            for _ in range(0,substeps):
                self.simulation.DoStep()
            self.simulation.EndScene()

            if self.follow and not self.simulation.GetPaused():
                self.Set_Camera()
        
        for _, module in self.modules.items():
            module.Release()
        
        
        if self.pre_pause:
            print('\n--- Press SPACE to release! ---')
            self.simulation.SetPaused(True)
            paused = True
            if self.notifier:
                self.Environment.Get_Notifier().Set_Ready()

        while(self.simulation.GetDevice().run()):
            # for _, link in self.links.items():
            #     if abs(link.Get_react_force().Length()) > 30000:
            #         link.SetBroken(True)

            self.simulation.BeginScene()
            self.simulation.DrawAll()
            for _ in range(0,substeps):
                self.simulation.DoStep()
                if self.log and not paused:
                    for _, sensor in self.sensors.items():
                        sensor.LogData()
            self.simulation.EndScene()

            if (self.follow or self.cycle) and not paused:
                self.Set_Camera()
        
            if self.notifier and not paused and self.simulation.GetPaused():
                paused = True
                self.Environment.Get_Notifier().Set_Ready()
            if self.notifier and paused and not self.simulation.GetPaused():
                paused = False
                self.Environment.Get_Notifier().Set_Idle()


    def Set_Lights(self, ambients = True):
        for light in self.Environment.Get_Lightsources():
            add_light = True
            if light[6] and not ambients: # if light is Ambient but ambients are off
                add_light = False
            if add_light:
                pos = chronoirr.vector3df(light[0][0], light[0][1], light[0][2])
                if light[7]:
                    aim = chronoirr.vector3df(light[1][0], light[1][1], light[1][2])
                    self.simulation.AddLightWithShadow(pos, aim, light[2], light[3], light[4], light[5])
                else:
                    self.simulation.AddLight(pos, light[2])
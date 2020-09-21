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
        
        self.camname = 'default'
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
        self.SPEEDMODE = SPEEDMODE

    def Set_Environment(self, Environment):
        
        self.Environment = Environment
        self.Environment.Initialize(self.ChSystem, self.SPEEDMODE)
        self.camviews = self.Environment.Get_Camviews()

        if self.Environment.Has_Notifier():
            self.notifier = True
            self.Environment.Get_Notifier().AddToSystem(self)
            self.Environment.Get_Notifier().Set_Idle()
    
    def Get_Environment(self):
        return self.Environment

    def Get_Target(self):
        return self.Environment.Get_Target()

    def Get_ChSystem(self):
        return self.ChSystem
    
    def Set_Perspective(self, camname, input_name = False, follow_position = [1.5, 0.75, 0], cycle_laptime = 4):
        if camname == 'follow':
            if not input_name:
                print('Camera Error: Input a module name to use follow perspective, using default')
            else:
                if input_name in self.modules:
                    self.follow = True
                    self.followmod = self.modules[input_name]
                    self.followpos = chronoirr.vector3df(follow_position[0], follow_position[1], follow_position[2])
                else:
                    print('Camera Error: "'+input_name+'" is not a recognized module and cannot be followed, using default')
        if camname == 'cycle':
            if not input_name:
                print('Camera Error: Input a valid perspective name to use cycle perspective, using default')
            else:
                if input_name in self.Environment.Get_Camviews():
                    self.cycle = True
                    self.camname = input_name
                    cam = self.Environment.Get_Camviews()[self.camname]
                    position = chrono.ChVectorD(cam['pos'][0], cam['pos'][1], cam['pos'][2])
                    dp = chrono.ChVectorD(cam['dir'][0], cam['dir'][1], cam['dir'][2])
                    dp.SetLength(cam['lah'])
                    looker = position + dp
                    self.cycle_point = looker
                    self.cycle_vector = position - looker
                    self.cycle_angle = -2*np.pi/cycle_laptime
                else:
                    print('Camera Error: "'+input_name+'" is not a recognized perspective and cannot be cycled, using default')

        elif camname in self.Environment.Get_Camviews():
            self.camname = camname
        else:
            print('Camera Error: "'+camname+'" is not a recognized camera position, using default')

    def Add_Camview(self, name, position = [0,0,0], direction = [1,0,0], distance = 1):
        '''Add your own camera perspective to the environment. \n
        name: string 'perspective name'\n
        position: camera coordinates in [x,y,z]\n
        direction: aim of the camera in [x,y,z]\n
        distance: number of how far away the camera should look\n
        Use Set_Perspective('your name') to use the camera position.'''
        self.Environment.Add_Camview({
            name: {
                'pos': position,
                'dir': direction,
                'lah': distance
            }
        })

    def Add_MiroModule(self, module, name, position = False, vel = False):
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
        moveMod = self.modules[move_module]
        refMod = self.modules[ref_module]
        moveMod.SetPosition(refMod.GetReferencePoint())

    def Add_Object(self, Object):
        self.ChSystem.Add(Object)

    def Set_Camera(self):
        if self.follow:
            pos = self.followmod.GetBasePosition()
            looker = chronoirr.vector3df(pos.x, pos.y, pos.z)
            self.simulation.AddTypicalCamera(looker + self.followpos, looker)
        elif self.cycle:
            p = self.cycle_point + self.cycle_vector
            position = chronoirr.vector3df(p.x, p.y, p.z)
            looker = chronoirr.vector3df(self.cycle_point.x, self.cycle_point.y, self.cycle_point.z)
            self.simulation.AddTypicalCamera(position, looker)
            q = chrono.Q_from_AngAxis(self.cycle_angle/self.fps, chrono.ChVectorD(0,1,0))
            self.cycle_vector = q.Rotate(self.cycle_vector)
        else:
            cam = self.Environment.Get_Camviews()[self.camname]
            position = chronoirr.vector3df(cam['pos'][0], cam['pos'][1], cam['pos'][2])
            looker = position + chronoirr.vector3df(cam['dir'][0], cam['dir'][1], cam['dir'][2]).setLength(cam['lah'])
            self.simulation.AddTypicalCamera(position, looker)

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

        if "print module info" in config:
            self.print = config['print module info']
        else:
            self.print = False
    
    def Run(self, config):
        # ---------------------------------------------------------------------
        #
        #  Create an Irrlicht application to visualize the system
        #
        self.Initialize_Config(config)
        
        self.simulation = chronoirr.ChIrrApp(self.ChSystem, 'MiroSimulation', chronoirr.dimension2du(self.res[0], self.res[1]))
        
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

        if self.log:
            for sensor_ID, sensor in self.sensors.items():
                sensor.Initialize(sensor_ID+'.txt')

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

            if self.follow:
                self.Set_Camera()
        
        for _, module in self.modules.items():
            module.Release()
        
        
        
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
            self.simulation.EndScene()

            if self.log and not paused:
                for _, sensor in self.sensors.items():
                    sensor.LogData()

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
                aim = chronoirr.vector3df(light[1][0], light[1][1], light[1][2])
                self.simulation.AddLightWithShadow(pos, aim, light[2], light[3], light[4], light[5])
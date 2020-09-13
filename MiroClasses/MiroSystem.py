import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
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
        
        self.system = chrono.ChSystemNSC()
        chrono.SetChronoDataPath(os.getcwd() + "/")
        self.modules = {}
        self.links = {}

        self.SPEEDMODE = False
        self.notifier = False
        
        self.camname = 'default'
        
        # Set the default outward/inward shape margins for collision detection,
        # this is epecially important for very large or very small objects.
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.00001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.00001)
        
        # Maybe you want to change some settings for the solver. For example you
        # might want to use SetSolverMaxIterations to set the number of iterations
        # per timestep, etc.
        
        #self.system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
        self.system.SetSolverMaxIterations(70)
        
    def Set_Speedmode(self, SPEEDMODE = True):
        self.SPEEDMODE = SPEEDMODE

    def Set_Environment(self, Environment):
        
        self.Environment = Environment
        self.Environment.Initialize(self.system, self.SPEEDMODE)
        self.camviews = self.Environment.Get_Camviews()

        if self.Environment.Has_Notifier():
            self.notifier = True
            self.Environment.Get_Notifier().AddToSystem(self)
            self.Environment.Get_Notifier().Set_Idle()

    def Get_Target(self):
        return self.Environment.Get_Target()
    
    def Set_Perspective(self, camname):
        if camname in self.Environment.Get_Camviews():
            self.camname = camname
        else:
            print('Error: "'+camname+'" is not a recognized camera position, using default')
    
    def Add_MiroModule(self, module, name, position = False, vel = False):
        if(position):
            module.Move(position)
        if vel:
            module.SetVelocity(vel)
        module.AddToSystem(self)
        self.links.update(module.GetLinks())
        self.modules.update({name: module})

    def MoveToReference(self, move_module, ref_module):
        moveMod = self.modules[move_module]
        refMod = self.modules[ref_module]
        moveMod.SetPosition(refMod.GetReferencePoint())

    def Add_Object(self, Object):
        self.system.Add(Object)

    def Set_Camera(self):
        cam = self.Environment.Get_Camviews()[self.camname]
        position = chronoirr.vector3df(cam['pos'][0], cam['pos'][1], cam['pos'][2])
        looker = position + chronoirr.vector3df(cam['dir'][0], cam['dir'][1], cam['dir'][2]).setLength(cam['lah'])
        self.simulation.AddTypicalCamera(position, looker)
    
    def Run(self, resolution = [1280, 720], delay = 5):
        # ---------------------------------------------------------------------
        #
        #  Create an Irrlicht application to visualize the system
        #
        
        self.simulation = chronoirr.ChIrrApp(self.system, 'MiroSimulation', chronoirr.dimension2du(resolution[0], resolution[1]))
        
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
        
        dt = 1/300 # per frame
        substeps = 1

        self.simulation.SetTimestep(dt/substeps)
        self.simulation.SetTryRealtime(True)

        start = time.time()
        
        while(self.simulation.GetDevice().run() and start + delay > time.time()):
            self.simulation.BeginScene()
            self.simulation.DrawAll()
            for _ in range(0,substeps):
                self.simulation.DoStep()
            self.simulation.EndScene()
        
        for _, module in self.modules.items():
            module.Release()
        
        
        
        print('\n-- Press SPACE to release! ---')
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
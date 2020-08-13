import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import time

import Environments as env
import Landers as landers
 
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
        self.modules = {}
        self.links = {}
        
        self.camname = 'default'
        self.camviews = {
            'default': {
                'pos': [-7, 4, 0],
                'dir': [1,0,0],
                'lah': 10
            },
            '3rd floor staircase': {
                'pos': [3, 6, 7.5],
                'dir': [0.4,-0.2,-1],
                'lah': 0.05
            },
            '4th floor behind lander': {
                'pos': [11.75,10.25,-1],
                'dir': [-1,-0.4,0.1],
                'lah': 0.05
            },
            '2nd (ground) floor front view': {
                'pos': [-3,1.8,-1.5],
                'dir': [1,0.1,0.1],
                'lah': 0.05
            },
            '2nd (ground) floor side view': {
                'pos': [1,1.35,-10.15],
                'dir': [0.25,0.3,1],
                'lah': 0.05
            },
            'maccans': {
                'pos': [1,15,-1.15],
                'dir': [0,-1,0],
                'lah': 0.05
            },
            '4th floor observing launcher': {
                'pos': [10.5,9.5,3],
                'dir': [-0.2,-0.1,-1],
                'lah': 3
            }
        }
        
        # Set the default outward/inward shape margins for collision detection,
        # this is epecially important for very large or very small objects.
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.00001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.00001)
        
        # Maybe you want to change some settings for the solver. For example you
        # might want to use SetSolverMaxIterations to set the number of iterations
        # per timestep, etc.
        
        #self.system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
        self.system.SetSolverMaxIterations(70)
        
        
    def Set_Environment(self, Environment):
        self.target = Environment(self.system)

    def Get_Target(self):
        return self.target
    
    def Set_Perspective(self, camname):
        if camname in self.camviews:
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

    def Add_Object(self, object):
        self.system.Add(object)
    
    def Set_Camera(self):
        cam = self.camviews[self.camname]
        position = chronoirr.vector3df(cam['pos'][0], cam['pos'][1], cam['pos'][2])
        looker = position + chronoirr.vector3df(cam['dir'][0], cam['dir'][1], cam['dir'][2]).setLength(cam['lah'])
        self.simulation.AddTypicalCamera(position, looker)
    
    def Run(self, resolution = [1280, 720]):
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
        
        dt = 0.004 # per frame
        substeps = 1

        self.simulation.SetTimestep(dt/substeps)
        self.simulation.SetTryRealtime(True)

        delay = 5
        start = time.time()
        
        self.simulation.BeginScene()
        self.simulation.DrawAll()
        self.simulation.EndScene()
        time.sleep(1)
        
        while(self.simulation.GetDevice().run() and start + delay > time.time()):
            self.simulation.BeginScene()
            self.simulation.DrawAll()
            for _ in range(0,substeps):
                self.simulation.DoStep()
            self.simulation.EndScene()
        
        for _, module in self.modules.items():
            module.Release()

        while(self.simulation.GetDevice().run()):
            # for _, link in self.links.items():
            #     if abs(link.Get_react_force().Length()) > 22000:
            #         link.SetBroken(True)

            self.simulation.BeginScene()
            self.simulation.DrawAll()
            for _ in range(0,substeps):
                self.simulation.DoStep()
            self.simulation.EndScene()

    def Set_Lights(self, ambients = True):
        lightpos = [5,25,20]
        # lightpos[0], lightpos[1], lightpos[2]

        # Sky lighting
        # self.simulation.AddLightWithShadow(chronoirr.vector3df(2,25,-1),    # point
        #                                 chronoirr.vector3df(2,0,-1),    # aimpoint
        #                                 100,                 # radius (power)
        #                                 7,30,               # near, far
        #                                 50)                # angle of FOV

        # Sun lighting
        self.simulation.AddLightWithShadow(chronoirr.vector3df(lightpos[0], lightpos[1], lightpos[2]),    # point
                                        chronoirr.vector3df(3,0,-5),    # aimpoint
                                        100,                 # radius (power)
                                        15,40,               # near, far
                                        40)                # angle of FOV
        self.lightsource(lightpos)

        
        # Ambient from sides
        if(ambients):
            self.simulation.AddLightWithShadow(chronoirr.vector3df(-20,1,0),    # point
                                        chronoirr.vector3df(0,0,0),    # aimpoint
                                        24,                 # radius (power)
                                        7,40,               # near, far
                                        70)                # angle of FOV
            self.simulation.AddLightWithShadow(chronoirr.vector3df(0,1,-20),    # point
                                        chronoirr.vector3df(0,0,0),    # aimpoint
                                        24,                 # radius (power)
                                        7,40,               # near, far
                                        70)                # angle of FOV


    def lightsource(self, pos):
        sun = chrono.ChBody()
        sun.SetBodyFixed(True)
        sun.SetCollide(False)
        sun.SetPos(chrono.ChVectorD(pos[0], pos[1], pos[2]))

        # Visualization shape
        sun_box = chrono.ChBoxShape()
        sun_box.GetBoxGeometry().Size = chrono.ChVectorD(0.2,0.2,0.2)
        sun_box.SetColor(chrono.ChColor(1,1,0.1))
        sun.GetAssets().push_back(sun_box)
        self.system.Add(sun)

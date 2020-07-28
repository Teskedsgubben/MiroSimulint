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

        self.start_position = [0,0,0]
        self.throw_velocity = [0,0,0]
        
        
        # Set the default outward/inward shape margins for collision detection,
        # this is epecially important for very large or very small objects.
        chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
        chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)
        
        # Maybe you want to change some settings for the solver. For example you
        # might want to use SetSolverMaxIterations to set the number of iterations
        # per timestep, etc.
        
        #self.system.SetSolverType(chrono.ChSolver.Type_BARZILAIBORWEIN) # precise, more slow
        self.system.SetSolverMaxIterations(70)
        
        
    def Set_Environment(self, Environment):
        [self.start_position, self.throw_velocity] = Environment(self.system)
    
    def Add_MiroModule(self, module):
        module.Move(self.start_position)
        module.SetVelocity(self.throw_velocity)
        module.AddToSystem(self)

    def Add_Object(self, object):
        self.system.Add(object)
        
    
    def Run(self):
        # ---------------------------------------------------------------------
        #
        #  Create an Irrlicht application to visualize the system
        #
        
        self.simulation = chronoirr.ChIrrApp(self.system, 'MiroSimulatuion', chronoirr.dimension2du(1728,972))
        
        self.simulation.AddTypicalSky()
        position = chronoirr.vector3df(3,5,7.5)
        looker = chronoirr.vector3df(0.4,-0.2,-1).setLength(2)
        self.simulation.AddTypicalCamera(position, position + looker)
        self.simulation.AddLightWithShadow(chronoirr.vector3df(2,12,2),    # point
                                        chronoirr.vector3df(0,0,0),    # aimpoint
                                        255,                 # radius (power)
                                        1,9,               # near, far
                                        70)                # angle of FOV
        
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
        
        self.simulation.SetTimestep(0.002)
        self.simulation.SetTryRealtime(True)


        self.simulation.BeginScene()
        self.simulation.DrawAll()
        self.simulation.EndScene()
        time.sleep(2)

        while(self.simulation.GetDevice().run()):
            self.simulation.BeginScene()
            self.simulation.DrawAll()
            for substep in range(0,3):
                self.simulation.DoStep()
            self.simulation.EndScene()
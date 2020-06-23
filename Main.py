#------------------------------------------------------------------------------
# Name:        Miro Simulint 
# Purpose:
#
# Authors:     Felix Djuphammar,  
#
#-------------------------------------------------------------------------------
 
 
import pychrono.core as chrono
import pychrono.irrlicht as chronoirr

import Environments as env
import Landers as landers
import MiroSystem as ms


simulation_system  = ms.MiroSystem()

simulation_system.Set_Environment(env.DemoTable)

simulation_system.Add_Lander(landers.DemoLander)

simulation_system.Run()
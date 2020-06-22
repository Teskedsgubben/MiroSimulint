#------------------------------------------------------------------------------
# Name:        pychrono example
# Purpose:
#
# Author:      Alessandro Tasora
#
# Created:     1/01/2019
# Copyright:   (c) ProjectChrono 2019
#
#
# This file shows how to
#   - create a small stack of bricks,
#   - create a support that shakes like an earthquake, with motion function
#   - simulate the bricks that fall
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
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

import Shapes as shp
import numpy as np


simulation_system  = ms.MiroSystem()

simulation_system.Set_Environment(env.DemoTable)

simulation_system.Add_Lander(landers.DemoLander)

pos_f = chrono.ChVectorD(2, 2, 2)
pos_b = chrono.ChVectorD(2.5, 2, 1.5)
dir_f = chrono.ChVectorD(np.cos(1), 0, np.sin(1))
dir_b = chrono.ChVectorD(np.cos(1.2), 0, np.sin(1.2))
w = 2
h = 0.25

my_step = shp.step(pos_f, dir_f, pos_b, dir_b, w, h)
simulation_system.Add_Object(my_step)

simulation_system.Run()
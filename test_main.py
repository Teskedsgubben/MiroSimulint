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



################# TRAPPSTEG ###############
Tetra_pos =  chrono.ChVectorD(2,2,1)

Tetra_O = Tetra_pos + chrono.ChVectorD(0,0,0) # 0,0,0
Tetra_X = Tetra_pos + chrono.ChVectorD(1,0,0) # 1,0,0
Tetra_Y = Tetra_pos + chrono.ChVectorD(0,0.25,0) # 0,1,0
Tetra_XY = Tetra_pos + chrono.ChVectorD(1,0.25,0) # 1,1,0

Tetra_Z = Tetra_pos + chrono.ChVectorD(-0.15,0,2) # 0,0,1
Tetra_ZX = Tetra_pos + chrono.ChVectorD(1.15,0,2) # 0,0,1
Tetra_ZY = Tetra_pos + chrono.ChVectorD(-0.15,0.25,2) # 0,0,1
Tetra_ZXY = Tetra_pos + chrono.ChVectorD(1.15,0.25,2) # 0,0,1

Tetra_mesh = chrono.ChTriangleMeshConnected()

# inner side
Tetra_mesh.addTriangle(Tetra_O, Tetra_Y, Tetra_X)
Tetra_mesh.addTriangle(Tetra_XY, Tetra_X, Tetra_Y)

# outer side
Tetra_mesh.addTriangle(Tetra_Z, Tetra_ZX, Tetra_ZXY)
Tetra_mesh.addTriangle(Tetra_Z, Tetra_ZXY, Tetra_ZY)

# top side
Tetra_mesh.addTriangle(Tetra_Y, Tetra_ZY, Tetra_ZXY)
Tetra_mesh.addTriangle(Tetra_Y, Tetra_ZXY, Tetra_XY)

# bottom side
Tetra_mesh.addTriangle(Tetra_O, Tetra_X, Tetra_Z)
Tetra_mesh.addTriangle(Tetra_X, Tetra_ZX, Tetra_Z)

# left side
Tetra_mesh.addTriangle(Tetra_X, Tetra_XY, Tetra_ZX)
Tetra_mesh.addTriangle(Tetra_ZXY, Tetra_ZX, Tetra_XY)

# right side
Tetra_mesh.addTriangle(Tetra_O, Tetra_Z, Tetra_Y)
Tetra_mesh.addTriangle(Tetra_ZY, Tetra_Y, Tetra_Z)

Tetra_mesh.RepairDuplicateVertexes()

Tetra = chrono.ChBody()
Tetra.SetCollide(True)
Tetra.SetBodyFixed(True)

Tetra_shape = chrono.ChTriangleMeshShape()
Tetra_shape.SetMesh(Tetra_mesh)
Tetra_shape.SetColor(chrono.ChColor(0.9, 0.1, 0.1))

Tetra.GetAssets().push_back(Tetra_shape)

simulation_system.Add_Object(Tetra)
################# TRAPPSTEG ###############



simulation_system.Run()
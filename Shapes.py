import pychrono.core as chrono

################# TRAPPSTEG ###############
# position_front:  chrono.ChVectorD, the position of the inner lower front corner
# direction_front: chrono.ChVectorD, normal direction to staircase center that aligns with front of the step
# position_back:   chrono.ChVectorD, the position of the inner lower front corner
# direction_back:  chrono.ChVectorD, normal direction that aligns with back of the step
# width:  double, Width of the step as seen when walking in the staircase
# height: double, Thickness of the step
def step(position_front, direction_front, position_back, direction_back, width, height):
  direction_front.SetLength(width)
  direction_back.SetLength(width)
  
  # Notation: I = Inner/O = Outer, U = Upper/L = Lower, F = Front/B = Back
  # Ex: Step_ILF is the Inner Lower Front corner of the step
  Step_ILF = position_front
  Step_IUF = position_front + chrono.ChVectorD(0, height, 0)
  Step_ILB = position_back
  Step_IUB = position_back  + chrono.ChVectorD(0, height, 0)

  Step_OLF = position_front + direction_front
  Step_OUF = position_front + direction_front + chrono.ChVectorD(0, height, 0)
  Step_OLB = position_back  + direction_back  
  Step_OUB = position_back  + direction_back + chrono.ChVectorD(0, height, 0)

  Step_mesh = chrono.ChTriangleMeshConnected()

  # inner side
  Step_mesh.addTriangle(Step_ILF, Step_ILB, Step_IUF)
  Step_mesh.addTriangle(Step_IUB, Step_IUF, Step_ILB)

  # outer side
  Step_mesh.addTriangle(Step_OLF, Step_OUB, Step_OLB)
  Step_mesh.addTriangle(Step_OLF, Step_OUF, Step_OUB)

  # top side
  Step_mesh.addTriangle(Step_IUF, Step_OUB, Step_OUF)
  Step_mesh.addTriangle(Step_IUF, Step_IUB, Step_OUB)

  # bottom side
  Step_mesh.addTriangle(Step_ILF, Step_OLF, Step_OLB)
  Step_mesh.addTriangle(Step_ILF, Step_OLB, Step_ILB)

  # back side
  Step_mesh.addTriangle(Step_ILB, Step_OLB, Step_IUB)
  Step_mesh.addTriangle(Step_OUB, Step_IUB, Step_OLB)

  # front side
  Step_mesh.addTriangle(Step_ILF, Step_IUF, Step_OLF)
  Step_mesh.addTriangle(Step_OUF, Step_OLF, Step_IUF)

  Step_mesh.RepairDuplicateVertexes()

  Step = chrono.ChBody()
  Step.SetBodyFixed(True)

  Step_shape = chrono.ChTriangleMeshShape()
  Step_shape.SetMesh(Step_mesh)
  # Step_shape.SetColor(chrono.ChColor(0.9, 0.9, 0.9))


  Step.GetCollisionModel().ClearModel()	
  Step.GetCollisionModel().AddTriangleMesh(Step_mesh, True, False)
  Step.GetCollisionModel().BuildModel()
  Step.SetCollide(True)
      
  Step_texture = chrono.ChTexture()
  Step_texture.SetTextureFilename(chrono.GetChronoDataFile('textures/stone_floor.jpg'))
  Step_texture.SetTextureScale(10, 10)
  Step.GetAssets().push_back(Step_texture)
        

  Step.GetAssets().push_back(Step_shape)

  return Step
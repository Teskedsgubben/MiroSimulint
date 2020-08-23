import pychrono.core as chrono
import numpy as np

class MiroNotifier():
    def __init__(self, pos, angle = 0, tilt = 0):
        x = 4
        y = 1.5
        r = 0.35

        self.tilt_Q = chrono.Q_from_AngAxis(np.deg2rad(tilt), chrono.ChVectorD(1,0,0))
        self.angle_Q = chrono.Q_from_AngAxis(np.deg2rad(angle), chrono.ChVectorD(0,1,0))

        bulbvec = self.angle_Q.Rotate(self.tilt_Q.Rotate(chrono.ChVectorD(x/2 - 1.6*r, y/2 - 1.6*r, 0)))

        self.board = chrono.ChBody()
        self.board.SetBodyFixed(True)
        self.board.SetCollide(False)
        self.board.SetPos(chrono.ChVectorD(pos[0], pos[1], pos[2]))
        self.board.SetRot(self.angle_Q * self.tilt_Q)

        # Visualization shape
        board_shape = chrono.ChBoxShape()
        board_shape.GetBoxGeometry().Size = chrono.ChVectorD(x/2, y/2, 0.05)
        self.board.GetAssets().push_back(board_shape)

        self.signalbulb = chrono.ChBodyEasySphere(r, 500)
        self.signalbulb.SetBodyFixed(True)
        self.signalbulb.SetPos(chrono.ChVectorD(pos[0], pos[1], pos[2]) + bulbvec)
        self.signalbulb.SetRot(self.angle_Q * self.tilt_Q * chrono.Q_from_AngAxis(np.deg2rad(90), chrono.ChVectorD(1,0,0)))

        # Collision shape
        self.signalbulb.SetCollide(True)
        self.signalbulb.GetCollisionModel().ClearModel()
        self.signalbulb.GetCollisionModel().AddSphere(r)
        self.signalbulb.GetCollisionModel().BuildModel()


    def AddToSystem(self, system):
        board_texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/notifboard.png'))
        board_texture.SetTextureScale(4, 3)
        self.board.GetAssets().push_back(board_texture)
        system.Add_Object(self.board)
        
        bulb_texture = chrono.ChTexture(chrono.GetChronoDataFile('textures/notifbulb.png'))
        bulb_texture.SetTextureScale(1, 1)
        self.signalbulb.GetAssets().push_back(bulb_texture)
        system.Add_Object(self.signalbulb)


    def Set_Idle(self):
        self.signalbulb.SetRot(self.angle_Q * self.tilt_Q * chrono.Q_from_AngAxis(np.deg2rad(90), chrono.ChVectorD(1,0,0)))
    def Set_Ready(self):
        self.signalbulb.SetRot(self.angle_Q * self.tilt_Q * chrono.Q_from_AngAxis(np.deg2rad(-90), chrono.ChVectorD(1,0,0)))
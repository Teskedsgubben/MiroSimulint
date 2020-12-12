import agx
import agxSDK

def AddDummController(MiroSystem, Module_Name):
    [sim, app, root] = MiroSystem.Get_APIsystem()
    MiroModule = MiroSystem.Get_MiroModule(Module_Name)
    sim.add(DummyController(MiroModule.GetBaseComponent().GetBody()))


class DummyController(agxSDK.GuiEventListener):
    '''Wheels must be in a list and in pairs L & R, i.e. [wheel_left, wheel_right]'''
    def __init__(self, body):
        super().__init__(agxSDK.GuiEventListener.KEYBOARD)
        self.body = body
        self.max_speed = 5

    # Steering function
    def keyboard(self, key, x, y, alt, keydown):
        if keydown and key == agxSDK.GuiEventListener.KEY_Up:
            new_vel = agx.Vec3(1,0,0)
            new_vel.setLength(self.max_speed)
            self.body.setVelocity(new_vel)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Down:
            new_vel = agx.Vec3(-1,0,0)
            new_vel.setLength(self.max_speed)
            self.body.setVelocity(new_vel)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Right:
            new_vel = agx.Vec3(0,-1,0)
            new_vel.setLength(self.max_speed)
            self.body.setVelocity(new_vel)

        elif keydown and key == agxSDK.GuiEventListener.KEY_Left:
            new_vel = agx.Vec3(0,1,0)
            new_vel.setLength(self.max_speed)
            self.body.setVelocity(new_vel)
        else:
            self.body.setVelocity(agx.Vec3(0,0,0))
            return False
        return True
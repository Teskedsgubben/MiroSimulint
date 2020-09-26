class MiroEnvironment():
    def __init__(self):
        self.init = False
        self.target = False
        self.notifier = False
        self.camviews = {}
        self.lights = []

    def Add_Camview(self, camviews):
        self.camviews.update(camviews)
    
    def Get_Camviews(self):
        return self.camviews

    def Set_Target(self, target, target_prop):
        self.target = target
        self.target_prop = target_prop
        self.camviews.update({
            'target': {
                'pos': [self.target[0]-4, self.target[1]+3, self.target[2]],
                'dir': [4,-3,0],
                'lah': 5
            }
        })
    
    def Get_Target(self):
        return self.target
    
    def Set_Initializer(self, init_function):
        self.init = init_function

    def Set_Notifier(self, notifier):
        self.notifier = notifier

    def Get_Notifier(self):
        return self.notifier

    def Has_Notifier(self):
        if self.notifier:
            return True
        else:
            return False

    def Add_Lightsource(self, point, target = [0,0,0], power = 50, near = 1, far = 25, angle = 90, isAmbient = True, shadows = True):
        self.lights.append([point, target, power, near, far, angle, isAmbient, shadows])

    def Get_Lightsources(self):
        return self.lights

    def Initialize(self, system, SPEEDMODE):
        if(self.init):
            self.init(system, SPEEDMODE)
        if(self.target):
            self.target_prop(system, self.target)

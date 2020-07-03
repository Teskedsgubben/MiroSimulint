

class Module():
    def __init__(self, name):
        self.name = name
        self.components = {}
        self.links = {}
        self.nonames = 0
    
    def AddComponent(self, comp, name='unnamed'):
        if(name == 'unnamed'):
            self.nonames = self.nonames + 1
            name = 'unnamed'+str(self.nonames)
        self.components.update({name: comp})

    def AddToSystem(self, system):
        for name, comp in self.components.items():
            system.Add(comp)
from MiroClasses.MiroModule import Module as MiroModule
from src import Components

def DemoRobot1():
    MyRobot = MiroModule('MyRobot')

    # Add body components
    MyRobot.AddComponent(Components.MC035(), 'Base')
    MyRobot.AddComponent(Components.MC093(), 'Top')
    MyRobot.RotateX('Top', 180)
    
    # Connect the components. The first remains in position, and the second component is moved to match
    MyRobot.ConnectComponents('Base', 'A', 'Top', 'A')
    MyRobot.ConnectComponents('Base', 'C', 'Top', 'B')

    # Add left wheel components
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Left, Back')
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Left, Front')
    MyRobot.RotateX(['Wheel: Left, Front', 'Wheel: Left, Back'], 90)
 
    # Attach the left wheels
    MyRobot.ConnectComponents('Base', 'G', 'Wheel: Left, Back', 'A')
    MyRobot.ConnectComponents('Base', 'F', 'Wheel: Left, Front', 'A')

    # # Add right wheel components
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Right, Back')
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Right, Front')
    MyRobot.RotateX(['Wheel: Right, Front', 'Wheel: Right, Back'], -90)

    # Attach the right wheels
    MyRobot.ConnectComponents('Base', 'I', 'Wheel: Right, Back', 'A')
    MyRobot.ConnectComponents('Base', 'H', 'Wheel: Right, Front', 'A')
    
    # Set custom textures
    # MyRobot.SetTexture(['Base', 'Top'], 'mirobooster.png', [1,1])
    # MyRobot.SetTexture(['Wheel: Left, Back', 'Wheel: Left, Back', 'Wheel: Left, Back', 'Wheel: Left, Back'], 'woodwheel.png', [1,1])

    # Show the layout of the build before simulation
    MyRobot.CreateModuleMap()

    return MyRobot



def DemoRobot2():
    MyRobot = MiroModule()

    # Build a base frame
    MyRobot.AddComponent(Components.MC124(), 'Left Frame')
    MyRobot.AddComponent(Components.MC124(), 'Right Frame')
    MyRobot.RotateX('Left Frame', 90)
    MyRobot.RotateX('Right Frame', -90)
    MyRobot.AddComponent(Components.MC122(), 'Back Frame')
    MyRobot.RotateX('Back Frame', 90)
    MyRobot.RotateY('Back Frame', 90)
    
    # Connect the components. The first remains in position, and the second component is moved to match
    MyRobot.ConnectComponents('Back Frame', 'E', 'Right Frame', 'B')
    MyRobot.ConnectComponents('Back Frame', 'F', 'Left Frame', 'B')

    # Build the body
    MyRobot.AddComponent(Components.MC015(), 'Left Body')
    MyRobot.AddComponent(Components.MC015(), 'Right Body')
    MyRobot.RotateX('Left Body', 90)
    MyRobot.RotateX('Right Body', -90)
    MyRobot.AddComponent(Components.MC013(), 'Back Body')
    MyRobot.RotateX('Back Body', 90)
    MyRobot.RotateY('Back Body', -90)
    MyRobot.AddComponent(Components.MC035(), 'Top Body')
    MyRobot.RotateX('Top Body', 180)

    # Connect body to frame
    MyRobot.ConnectComponents('Right Frame', 'D', 'Right Body', 'F')
    MyRobot.ConnectComponents('Left Frame', 'C', 'Left Body', 'H')
    MyRobot.ConnectComponents('Back Body', 'C', 'Right Body', 'K')
    MyRobot.ConnectComponents('Back Body', 'D', 'Left Body', 'K')
    
    MyRobot.ConnectComponents('Right Body', 'H', 'Top Body', 'D')
    MyRobot.ConnectComponents('Left Body', 'F', 'Top Body', 'B')

    # Add left wheel
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Left')
    MyRobot.RotateX('Wheel: Left', 90)
    MyRobot.ConnectComponents('Back Frame', 'B', 'Wheel: Left', 'A')

    # Add right wheel
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Right')
    MyRobot.RotateX('Wheel: Right', -90)
    MyRobot.ConnectComponents('Back Frame', 'A', 'Wheel: Right', 'A')

    # Add front wheel
    MyRobot.AddComponent(Components.MC242(), 'Wheel: Front')
    MyRobot.AddComponent(Components.MC211(), 'Wheelaxis: Left')
    MyRobot.AddComponent(Components.MC211(), 'Wheelaxis: Right')
    MyRobot.RotateX(['Wheel: Front', 'Wheelaxis: Right', 'Wheelaxis: Left'], 90)

    # Attach the wheels
    MyRobot.ConnectComponents('Left Frame', 'G', 'Wheelaxis: Left', 'B')
    MyRobot.ConnectComponents('Right Frame', 'G', 'Wheelaxis: Right', 'A')
    MyRobot.ConnectComponents('Wheelaxis: Left', 'A', 'Wheel: Front', 'B')
    MyRobot.ConnectComponents('Wheelaxis: Right', 'B', 'Wheel: Front', 'A')

    # MyRobot.SetTexture(
    MyRobot.CreateModuleMap()
    
    return MyRobot
# Example controller

# An example controller for a robot. It has a very basic setup, 
# and is meant to function as a prototype for how a controller 
# can be implemented. 


import agx
import agxCollide
import agxOSG
import agxSDK
import agxPython
import agxIO
import agxModel
import agxRender


from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI
from MiroClasses import MiroAPI_agx as agxAPI 


#Setup for keys that will be used
controls = {
    'KEY_UP': agxSDK.GuiEventListener.KEY_Up,
    'KEY_DOWN': agxSDK.GuiEventListener.KEY_Down,
    'KEY_LEFT': agxSDK.GuiEventListener.KEY_Left,
    'KEY_RIGHT': agxSDK.GuiEventListener.KEY_Right,
    'SPACE': agxSDK.GuiEventListener.KEY_Space,
    'DELETE': agxSDK.GuiEventListener.KEY_Delete,
    'HOME': agxSDK.GuiEventListener.KEY_Home,
    'PAGE_UP': agxSDK.GuiEventListener.KEY_Page_Down,
    'PAGW_DOWN': agxSDK.GuiEventListener.KEY_Page_Up,
    'INSERT': agxSDK.GuiEventListener.KEY_Insert,
    'END': agxSDK.GuiEventListener.KEY_End
}


#Controller requires these input arguments to function, removing arguments or changing order will result in errors
def MyController(module, keydown, key, alt):

    #Input arguments
    #module: Module to control
    #keydown: Boolean, true when key is pressed, false when released
    #key: Key pressed, latest key pressed if multiple keys are pressed simultaniously
    #alt: Alternative key pressed, 'alt', 'shift' etc.  

    #Arguments in module.SetMotorSpeed('LINK_NAME', SPEED)
    #Link needs to have motor enabled

    if not keydown:
        
        module.SetMotorSpeed('FL_tire', 0)
        module.SetMotorSpeed('FR_tire', 0)
    else:
        if key == module.controls['KEY_UP']:
            module.SetMotorSpeed('FL_tire', -50)
            module.SetMotorSpeed('FR_tire', 50)
                
        elif key == module.controls['KEY_DOWN']:
            module.SetMotorSpeed('FL_tire', 15)
            module.SetMotorSpeed('FR_tire', -15)

        elif key == module.controls['KEY_LEFT']:
            module.SetMotorSpeed('FL_tire', -3)
            module.SetMotorSpeed('FR_tire', 25)
    
        elif key == module.controls['KEY_RIGHT']:
            module.SetMotorSpeed('FL_tire', -25)
            module.SetMotorSpeed('FR_tire', 3)

        elif key == module.controls['SPACE']:
            module.SetMotorSpeed('FL_tire', 0)
            module.SetMotorSpeed('FR_tire', 0)

def SensorController(module):    
    # Get sensor that we called 'Lidar1' when building the bot
    Front_Sensor=module.GetSensor('Lidar1')

    # Get measurements from sensor as list
    d = Front_Sensor.GetDistances()

    # Prints distances for debugging:
    print("print distances: d =", d)
    
    # Check if obstacle straight ahead
    if d[1] > 0.35: 
        front_clear=True
    else:
        front_clear=False

    # If obstacle straight ahead, back up and turn
    if not front_clear:     
        # positive valued turn if left is more clear
        turn = 12
        
        # turn changed to negative value if right is more clear
        if d[0] < d[2]:
            turn=-turn
        
        # back up and turn slightly
        module.SetMotorSpeed('FL_tire', 15+turn)
        module.SetMotorSpeed('FR_tire', -15+turn)
        return
    
    # Controls when left is clear
    if d[0] > 0.35:
        left_clear=True
    else:
        left_clear=False 
    
    # Controls when right is clear
    if d[2] > 0.35:
        right_clear=True
    else:
        right_clear=False

    # If no obstacle move forward
    if left_clear and right_clear:
        module.SetMotorSpeed('FL_tire', -50)
        module.SetMotorSpeed('FR_tire', 50)
        return

    # Narrow path 
    if not left_clear and not right_clear:
        if d[0]>d[2]:
            left_clear = True
        else:
            right_clear = True    

    # If obstacle on the right        
    if not right_clear:
        module.SetMotorSpeed('FL_tire', -3)
        module.SetMotorSpeed('FR_tire', 25)

    # If obstacle on the left 
    if not left_clear:
        module.SetMotorSpeed('FL_tire', -25)
        module.SetMotorSpeed('FR_tire', 3)














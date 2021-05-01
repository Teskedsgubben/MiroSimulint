# An example controller for a robot. It has a very basic setup, 
# and is meant to function as a prototype for how a controller 
# can be implemented. 
from MiroClasses.MiroAPI_selector import SelectedAPI as MiroAPI


# Setup for keys that will be used. This is stored in the module in the main function, 
# so you can easily create different control layouts to try out.
controls_arrows = {
    'Forward': MiroAPI.Keyboard('KEY_UP'),
    'Backward': MiroAPI.Keyboard('KEY_DOWN'),
    'Left': MiroAPI.Keyboard('KEY_LEFT'),
    'Right': MiroAPI.Keyboard('KEY_RIGHT'),
    'Brake': MiroAPI.Keyboard('SPACE'),
    'Print_Example': MiroAPI.Keyboard('HOME')
}

# You can use letter keys as well, but keep in mind they may collide with other commands
# In this WASD example, the 'w' key overlaps with built in functions in agxViewer
controls_wasd = {
    # Tip: Using upper case letters like 'W' will bind Shift + 'w'
    'Forward': MiroAPI.Keyboard('w'),
    'Backward': MiroAPI.Keyboard('s'),
    'Left': MiroAPI.Keyboard('a'),
    'Right': MiroAPI.Keyboard('d'),
    'Brake': MiroAPI.Keyboard('SPACE'),
    'Print_Example': MiroAPI.Keyboard('HOME')
}


###################################################
############## GUI BASED CONTROLLER ###############
###################################################
#
# The controller function will recieve these input arguments when called
# Removing arguments or changing order will result in errors
def MyController(module, keydown, key, alt):
    # Input arguments
    # module: Module to control
    # keydown: Boolean, true when key is pressed, false when released
    # key: Key pressed, latest key pressed if multiple keys are pressed simultaniously
    # alt: Alternative key pressed, 'alt', 'shift' etc.  

    if not keydown:
        # Do not apply force if no key is pressed by setting speed=None
        module.SetMotorSpeed('FL_tire', None)
        module.SetMotorSpeed('FR_tire', None)
    else:
        # The controls you choose when adding the controller to the module will be accessible 
        # through module.controls['CONTROL_NAME']
        if key == module.controls['Print_Example']:
            print("You pressed the 'Print_Example' button!")

        elif key == module.controls['Forward']:
            # Set arguments in module.SetMotorSpeed('LINK_NAME', SPEED)
            # Link needs to have motor enabled. The speed values have 
            # opposing signs due to left and right orientetions.
            module.SetMotorSpeed('FL_tire', -50)
            module.SetMotorSpeed('FR_tire', 50)
                
        elif key == module.controls['Backward']:
            module.SetMotorSpeed('FL_tire', 15)
            module.SetMotorSpeed('FR_tire', -15)

        elif key == module.controls['Left']:
            module.SetMotorSpeed('FL_tire', -3)
            module.SetMotorSpeed('FR_tire', 25)
    
        elif key == module.controls['Right']:
            module.SetMotorSpeed('FL_tire', -25)
            module.SetMotorSpeed('FR_tire', 3)

        elif key == module.controls['Brake']:
            # Brake by forcing 0 speed
            module.SetMotorSpeed('FL_tire', 0)
            module.SetMotorSpeed('FR_tire', 0)

###################################################
############# SELF DRIVING CONTROLLER #############
###################################################
#
# The self driving function only recieves the module itself as an input
# You can access motors, sensors etc from their names in the module
def SensorController(module):    
    # Get sensor that we called 'Lidar1' when building the bot
    Front_Sensor=module.GetSensor('Lidar1')

    # Get measurements from sensor as list
    d = Front_Sensor.GetDistances()

    # You can print distances for debugging:
    # print("print distances: d =", d)
    
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
        module.SetMotorSpeed('FL_tire', -25)
        module.SetMotorSpeed('FR_tire', 25)
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














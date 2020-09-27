from src import Props as props
import numpy as np


def AddProps(system):
    wall_angle = 90 + np.rad2deg(-np.arctan(211/1380-0.05))

    props.MIT_door(system, [-5, 3.3, 8.22])

    props.MIT_door(system, [13.49,3.3, 1.2], wall_angle)
    props.MIT_door(system, [14.48, 3.3, -8.5], wall_angle)
    
    props.MIT_door(system, [13.04, 6.6, 5.5], wall_angle)
    props.MIT_door(system, [14.48, 6.6, -8.5], wall_angle)

    props.MIT_door(system, [7.25, 3.3, 12.22])
    props.MIT_door(system, [7.25, 6.6, 12.22])

    props.MIT_door(system, [13.6, 3.3, 12.22])
    props.MIT_door(system, [17.6, 3.3, 12.22])

    # Marks global origin
    props.sodacan(system, [0,0,0], 'schrodbull.png')

    props.painting(system, [13.8,2.0,-2], 'DemoBengan.png', wall_angle)
    props.painting(system, [13.94,1.8,-3.35], 'bungeebengan_notes.png', wall_angle, [0.2,0.27])

    props.painting(system, [6.46,5.0,10], 'infoboard.jpg', -90, [0.85/2, 1.46/2])
    props.painting(system, [13.34,2.0,2.2], 'floorinfo2.jpg', wall_angle, [0.6,0.66])

    props.painting(system, [12.84,5.1,7.1], 'corkboard.jpg', wall_angle, [1.0,0.5])
    props.painting(system, [13.047,5.1,5.1], 'corkboard.jpg', wall_angle, [1.0,0.5])
    
    props.painting(system, [13.77,5.1,-1.9], 'corkboard.jpg', wall_angle, [1.0,0.5])
    props.painting(system, [13.977,5.1,-3.9], 'corkboard.jpg', wall_angle, [1.0,0.5])

    props.painting(system, [-3.5,2.1,5], 'walkplanck.png', 0, [0.8,0.6])
    props.pokeball(system, [1.75,0.85,-7.15], 0)
    props.sodacan(system, [1.25,0.85,-7.05], 'schrodbull.png', 180)
    props.sodacan(system, [4.25,0.85,-7.25], 'joultcola.png')
    # props.coin(system, [1.65,0.85,-7.25])

    s = 1.15 # scale due to high roof
    props.painting(system, [1.0, 5.0, 8.18], 'black_painting_1.png', 0, [s*1.17/2, s*0.91/2])
    props.painting(system, [3.1, 5.0, 8.18], 'black_painting_2.png', 0, [s*1.17/2, s*0.91/2])
    props.painting(system, [5.2, 5.0, 8.18], 'black_painting_3.png', 0, [s*1.17/2, s*0.91/2])

    # East wall floor vents
    props.floorvent(system, [-0.55, 0.0, -8.85])
    props.floorvent(system, [ 3.85, 0.0, -8.85])

    # South wall floor vents
    props.floorvent(system, [-5.3, 0.0, -4.15])
    props.floorvent(system, [-5.3, 0.0, 0.3])

    # In the staircase
    # props.pokeball(system, [7.35,4.85,2.5], 0)
    # props.pokeball(system, [7.355,5.05,2.55], 0)

    # On the dartboard
    # props.pokeball(system, [1.95,1.501,-3.4], -45)
    # props.sodacan(system, [2.02,1.501,-3.5], 'schrodbull.png')
    # props.sodacan(system, [1.7,1.501,-3.3], 'joultcola.png')

    # Pink dinosaur
    # props.dino(system, [5.75,0.85,-9.75], 210, .15)
